import os,sys,time
os.system('source /afs/cern.ch/cms/PPD/PdmV/tools/McM/getCookie.sh')
os.system('cern-get-sso-cookie -u https://cms-pdmv.cern.ch/mcm/ -o ~/private/prod-cookie.txt --krb --reprocess')
sys.path.append('/afs/cern.ch/cms/PPD/PdmV/tools/McM/')

from rest import *
from json import dumps

mcm = restful(dev=False)

# example to search  ALL requesst which are member of a campaign
# it uses a generic search for specified columns: query='status=submitted'
# queries can be combined: query='status=submitted&member_of_campaign=Summer12'

#PhaseIISummer17wmLHEGENOnly, RunIISummer15wmLHEGS
#page = 0
#tot_exo = 0
#res = mcm.getA('requests',query='member_of_campaign=RunIIFall17wmLHEGS&dataset_name=*&status=*', page=page)

res = mcm.getA('requests', query='prepid=TOP-RunIISummer15wmLHEGS-00023')
#print res
for r in res:
    pi = r['prepid']
    dn = r['dataset_name']
    print ("'"+r['prepid']+"',",r['dataset_name'])
    print (pi)
    os.system('wget -q https://cms-pdmv.cern.ch/mcm/public/restapi/requests/get_fragment/'+pi+' -O '+pi)
    if "powheg" in dn or "Powheg" in dn or "POWHEG" in dn :
        powheg_check = os.popen('grep -c pythia8PowhegEmissionVetoSettings '+pi).read()
        print powheg_check
        powheg_check = int(powheg_check)
        if powheg_check == 0 :
            print "Wrong fragment: powheg in dataset name but MCatNLO settings in fragment"
