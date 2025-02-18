# -*- coding: utf-8 -*-
'''
Processor of ground-based lidar through LIDARGO

Inputs (both hard-coded and available as command line inputs in this order):
    path_config: path to general config file
    delete [bool]: whether to delete processed data
'''
import os
cd=os.path.dirname(__file__)
import sys
import warnings
import lidargo as lg
from datetime import datetime
import traceback
import yaml
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
import glob

warnings.filterwarnings('ignore')

#%% Inputs

#users inputs
if len(sys.argv)==1:#use this if running through an editor
    path_config=os.path.join(cd,'config/config_wfip3.yaml') #config path
    delete=False #delete a0 files?
else:#use this if running through command line
    path_config=os.path.join(cd,'config',sys.argv[1])
    delete=sys.argv[2] 
    
#%% Initalization
#configs
with open(path_config, 'r') as fid:
    config = yaml.safe_load(fid)

config_stand=pd.read_excel(config['path_config_stand']).set_index('regex')#lidargo configs collection

#general logging
logfile_main=os.path.join(cd,'log',datetime.strftime(datetime.now(), '%Y%m%d.%H%M%S'))+'_errors.log'
os.makedirs(os.path.join(cd,'log'),exist_ok=True)

#%% Main
for channel in config['channels']:
    save_path=os.path.join(config['path_data'],channel.replace('a0','b0'))#path where files are saved
    
    #list files to process
    files=glob.glob(os.path.join(config['path_data'],channel,'*nc'))

    #process all files
    for f in files:
        try:
            date=np.int64(re.search(r'\d{8}.\d{6}',f).group(0)[:8])
            
            #standardization
            if config_stand is not None:
                
                #find lidargo config
                for regex in config_stand.columns:
                    match = re.findall(regex, f)
                    sdate=config_stand[regex]['start_date']
                    edate=config_stand[regex]['end_date']
                    
                    if len(match)==1 and date>=sdate and date<=edate:
                        config_lg = lg.LidarConfig(**config_stand[regex].to_dict())
                    
                        #run lidargo
                        logfile=os.path.join(cd,'log',os.path.basename(f).replace('nc','log'))
                        lproc = lg.Standardize(f, config=config_lg, verbose=True,logfile=logfile)
                        lproc.process_scan(replace=True, save_file=True, make_figures=True, save_figures=True, save_path=save_path)
                        
                        if delete==True:
                            os.remove(f)
                        plt.close('all')
                
        except:
            print('Error at file '+f)
            
            with open(logfile_main, 'a') as lf:
                lf.write('Error at file '+f+':\n')
                traceback.print_exc(file=lf)
                lf.write('\n --------------------------------- \n')
