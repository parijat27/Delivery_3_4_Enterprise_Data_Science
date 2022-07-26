#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
import subprocess
import numpy as np
import pandas as pd
import requests
import json
from datetime import datetime

def get_JH_data():

    git_pull = subprocess.Popen( "/usr/bin/git pull" ,
                         cwd = os.path.dirname( 'data/raw/COVID-19/' ),
                         shell = True,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE )
    (out, error) = git_pull.communicate()


    print("Error : " + str(error))
    print("out : " + str(out))


def get_current_data_germany():

    data=requests.get('https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json')

    json_obj=json.loads(data.content)
    full_list=[]
    for pos,each_dict in enumerate (json_obj['features'][:]):
        full_list.append(each_dict['attributes'])

    pd_full_list=pd.DataFrame(full_list)
    pd_full_list.to_csv('data/raw/GER_state_data.csv',sep=';')
    print(' Number of regions rows: '+str(pd_full_list.shape[0]))

if __name__ == '__main__':
    get_JH_data()
    get_current_data_germany()

