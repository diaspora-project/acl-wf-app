import os
import Pyro4
import time
import sys
import pickle
import numpy as np
import pandas as pd
from pprint import pprint

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

ipAddressServer='192.168.1.242'
connectionPort='5001'
datasetPath='./instrument_mService/I-V_data'

@Pyro4.expose
class Embedded_Server(object):
    def __init__(self, daemon):
        self.daemon = daemon
    
    def lst_IV_datasets(self, pathInclude=False,type='relative') -> list:
        datasets=[os.path.splitext(x)[0] for x in os.listdir(datasetPath)]
        if pathInclude:
            if type == 'absolute':
                datasets = [os.path.abspath(y) for y in (os.path.join(datasetPath, x) for x in datasets)]
            else:
                datasets=[os.path.relpath(y) for y in (os.path.join(datasetPath,x) for x in datasets)]
        return datasets

    def get_IV_dataset(self, dataset,size: int |None)-> pd.DataFrame:
        pass

    @Pyro4.oneway
    def shutdown(self):
        print(f'Ecosystem communication session is terminated ')
        self.daemon.shutdown()

    

    
daemon = Pyro4.Daemon(host=ipAddressServer, port=int(connectionPort))
call_pyro_class = Embedded_Server(daemon)
uri = daemon.register(call_pyro_class, objectId='Pyro_Server')
print(Embedded_Server)
print(f'\turi = {uri}')
print('daemon running.')
time.sleep(5)
daemon.requestLoop()
daemon.close()
print('daemon closed')

# if __name__ == '__main__':
#   pass

# df = pd.read_csv('./I-V_data/Test_Ferrocene_disconnect_counter_v01.txt',sep='\t')
# xx=df['t'].head().diff()
# xx=xx.dropna().reset_index(drop=True)
# xx.mean().round(2)