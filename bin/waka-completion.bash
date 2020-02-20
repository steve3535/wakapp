#!/bin/bash
_waka_completions()
{

#COMPREPLY=("hostgroup")
opts="hostgroup scan_summary scan_details"

cur="${COMP_WORDS[COMP_CWORD]}"
prev1="${COMP_WORDS[COMP_CWORD-1]}"
prev2="${COMP_WORDS[COMP_CWORD-2]}"
prev3="${COMP_WORDS[COMP_CWORD-3]}"

COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )

if [[ ${#COMP_WORDS[@]} -gt 4 && "${prev3}" == "hostgroup" ]];then
  COMPREPLY=()
fi

if [[ ${#COMP_WORDS[@]} -gt 3 && "${prev2}" == "scan_details" ]];then
  COMPREPLY=()
fi

if [[ ${#COMP_WORDS[@]} -gt 3 && "${prev2}" == "scan_summary" ]];then
  COMPREPLY=()
fi


case "${prev1}" in
     "scan_summary")
                 opts="all "
                 opts+=$(find /home/wakausr/inventory/ -print | xargs -n 1 basename | grep -Evw "app_proxy|inventory" 2>/dev/null)
                 COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                 ;;
     "scan_details")
                 opts=$(grep -v "^\[" inventory/* | cut -d: -f2) 
                 COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                 ;;
     "hostgroup")
                 opts="del edit new list show ping rename scan setup patch"
                 COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                 ;;
     "show"|"ping"|"edit"|"del"|"rename"|"scan"|"setup"|"patch")        
                 opts=$(find /home/wakausr/inventory/ -print | xargs -n 1 basename | grep -Evw "app_proxy|inventory" 2>/dev/null)
                 COMPREPLY=( $(compgen -W "${opts}" -- ${cur}) )
                 ;;
     "new")
                 COMPREPLY=()
                 ;;           
     "list")
                 COMPREPLY=()
                 ;;   
       
esac

}

complete -F _waka_completions waka
