from subprocess import check_output
import json
import sys
import datetime
import xml.etree.ElementTree as ET
import redis 

hostname=sys.argv[1]
xml_result_file=sys.argv[2]                                               #the resulting oval file fetched from the target host 
pkgs_installed_file=sys.argv[3]                                           #A list of pks already installed on the target host
tmpresult=sys.argv[4]                                                     #the results file containing only the main packages (without dependencies) 
depresult=sys.argv[5]                                                     #the results file containing the main pkgs + their dependencies
vstats_file=sys.argv[6]                                                   #the statistics file
updatescript=sys.argv[7]                                                  #the generated script based on result file

with open(pkgs_installed_file,'r') as f:
    pkgs_data=f.read().split()                                            #list of the pkgs already present on the host in order not to search for what isnt there 

tree=ET.parse(xml_result_file)                                            #input file for parsing
root=tree.getroot()
ns=root.tag                                                               #namespaces are used in the xml document

i=root.tag.index('}')
ns=ns[0:i+1]                                                              #base namespace

resultsroot=root.find(ns+"results")                                       #go to the results

defarray=[]                                                               #defarray will contain all "positive" definitions
for res in resultsroot[0][0].findall(ns+"definition"):                
    defid=res.get('definition_id')
    result=res.get('result')
    if (result=="true"):
        defarray.append(defid)

ons_l=ns.replace('-',' ').split()                                         #the ns changes as we move to the details of the definitions
j=ons_l.index('results')
ons_l[j]='-definitions-'
ns=''.join(ons_l)

ovaldef=root.find(ns+"oval_definitions")

severity_list=[]                                                          #will gather the severities
pkg_list=[]                                                               #the corresponding affected & matched pkgs
dict_oval_positive={}                                                     #will form a dictionnary with definition id as keys
mypkgdep={}                                                               #dict that will contain this host pkg and its dependencies 

for item in defarray:
 list_oval_positive=[]
 element=ovaldef[1].findall(".//"+ns+"definition[@id='%s']" % item)
 title=element[0].find(".//"+ns+"title").text
 list_oval_positive.append(title)
 sev=element[0].find(".//"+ns+"severity").text
 list_oval_positive.append(sev)
 severity_list.append(sev)
 cve_list={}
 for cve in element[0].iter(ns+"cve"):
     cve_id=cve.text
     cwe=cve.get('cwe') #cve.get('cvss3')[:3]
     cve_list.update({cve_id:cwe})
 list_oval_positive.append(cve_list)
 dict_oval_positive[item]=list_oval_positive

for item in defarray:                                                     #we work on the stuff only if there is a match between the installed pkg and the affected
    element=root[2][1].find(".//"+ns+"definition[@id='%s']" % item)
    criterion_list=element[1][1].findall(".//"+ns+"criterion")
    for i in range(1,len(criterion_list),2):
      for rpm in pkgs_data:
          if (rpm==criterion_list[i].get('comment').split()[0]):
                pkg_list.append(rpm)
      

#the stats

total_vuln=0
count_crit_vuln=0
count_imp_vuln=0
count_mod_vuln=0
count_low_vuln=0

total_vuln+=len(severity_list)
count_crit_vuln+=severity_list.count('Critical')
count_imp_vuln+=severity_list.count('Important')
count_mod_vuln+=severity_list.count('Moderate')
count_low_vuln+=severity_list.count('Low')

#redirect stdout to a file for writing

f = open(vstats_file,'w')
sys.stdout=f
print(datetime.date.today(),"|",hostname,"|",count_crit_vuln,"|",count_imp_vuln,"|",count_mod_vuln,"|",count_low_vuln)

#restore stdout

sys.stdout = sys.__stdout__
print("Total:",total_vuln,"| Critical:",count_crit_vuln,"| Important:",count_imp_vuln,"| Moderate:",count_mod_vuln,"| Low:",count_low_vuln)
print("----------------------------------------------------------------")
for key in dict_oval_positive:
    print(dict_oval_positive[key][0])
    for cve in dict_oval_positive[key][2]:
        print("-->",cve,"/",dict_oval_positive[key][2][cve])

#search for dependencies

conn = redis.Redis('localhost')
data = conn.get("rhel7_dep_dict")

#deserialization
pkg_dep_dict = json.loads(data)

#with open('./pkg_dep.json','r+') as cachefile:                                   #pkg_dep.json is a file serving as cache (should be prepopulated per OS)
    #pkg_dep_dict=json.load(cachefile)
    
for item in pkg_list:
      if item in pkg_dep_dict:
          print(item)
          mypkgdep[item]=pkg_dep_dict[item]
      else:
          print('resolving ',item,' ...')
          deplist=check_output(["repoquery","-R","--resolve","--recursive","--qf='%{name}'",item])
          deplist=deplist.decode('utf-8').split("\n")
          del deplist[-1]                                                        #THERE IS A TRAILING BLANK SPACE TO REMOVE here
          for i in range(len(deplist)):
            deplist[i] = deplist[i].strip("\'")
          pkg_dep_dict[item]=deplist
          mypkgdep[item]=pkg_dep_dict[item]

    #cachefile.seek(0)                                                            #overwrite the cache file with the new content of the dictionnary
    #json.dump(pkg_dep_dict,cachefile)

#serialization
conn.set("rhel7_dep_dict",json.dumps(pkg_dep_dict))


#redirect stdout to a file for writing

f = open(tmpresult,'w')
sys.stdout=f

for item in mypkgdep:
    print(item)

#redirect stdout to a file for writing
    
f = open(depresult,'w')
sys.stdout=f

for item in mypkgdep:
    print(item)
    for x in mypkgdep[item]:
        print(x)

#redirect stdout to a file for writing

f = open(updatescript,'w')
sys.stdout=f

print("#!/bin/bash")
print("yum --enablerepo=wrepo*7 clean all | tee yupdate.log")
print("yum --enablerepo=wrepo*7 repolist all | tee -a yupdate.log")
print("yum --disablerepo=* --enablerepo=wrepo*7 -y update $(cat resultat-$(hostname | cut -d. -f1).txt) &>>./yupdate.log")
print('if [ "$?" -ne 0 ];then')
print("yum --disablerepo=* --enablerepo=wrepo*7 -y update $(cat resultat-$(hostname | cut -d. -f1).txt) --skip-broken &>>./yupdate.log")
print("fi")
print('if [ "$?" -ne 0 ];then')
print("yum --disablerepo=* --enablerepo=wrepo*7 -y update $(cat resultat-$(hostname | cut -d. -f1).txt)  --skip-broken --setopt=protected_multilib=false &>>./yupdate.log")
print("fi")


#restore stdout

sys.stdout = sys.__stdout__
print("----------------------------------------------------------------")
print("Total:",total_vuln,"| Critical:",count_crit_vuln,"| Important:",count_imp_vuln,"| Moderate:",count_mod_vuln,"| Low:",count_low_vuln)
print("----------------------------------------------------------------")


