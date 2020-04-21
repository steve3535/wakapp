from subprocess import check_output
item="vim-minimal"
deplist=check_output(["repoquery","-R","--resolve","--recursive","--qf='%{name}'",item])
deplist=deplist.decode('utf-8').split("\n")
del deplist[-1]
for item in deplist:
 item = item.strip("\'")
 print(item)




