#Quick and dirty to be used on the command line for nasty conversions

import os
import glob
import subprocess
import sys
import pickle

for root,subdir,files in os.walk():
    
    file_chk=glob.glob(os.path.join(root,"*.csv"))
    
    if len(file_chk)>0:
        for file in file_chk:
            
            file_sub_str=['summary.csv','dice.csv']
            file_sub_str_lst=[x for x in file_sub_str if file.find(x)!=-1]
            if len(file_sub_str_lst)>0:
                
                file_renm='nonval_pat_32_3_'+os.path.basename(file)
                file_renm=os.path.join(os.path.dirname(file),file_renm)
                os.rename(file,file_renm)

#Appending final values after renaming of file                
file_var_loc=[]
file_var_loc=subprocess.check_output('find . -iname nonval_pat_32_3_*',shell=True).decode(sys.stderr.encoding).split('\n')
tmp_lst=[]
for val in file_var_loc:
    tmp_info=val.split('/')
    tmp_lst.append(tmp_info[1])
    
tmp_lst_uniq=set(tmp_lst)

#Finidng matching patterns in original pickle file for exporting
with open('file_path_dict','rb') as fb:
    local_s3_remote_dict=pickle.load(fb)
    
for k in list(local_s3_remote_dict.keys()):
    if k not in tmp_lst_uniq:
        del local_s3_remote_dict[k]

#Syncing final values from local to s3 remote         
for k,v in local_s3_remote_dict.items():
    cmd='aws s3 sync {0} {1} --exclude "*" --include "*.png" --include "*.mha" --include ".csv"'.format(k,v)
    subprocess.run(cmd,shell=True)

