#Quick and dirty to be used on the command line for nasty conversions

import os
import glob
import subprocess
import sys

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