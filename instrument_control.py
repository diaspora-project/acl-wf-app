import os.path
import Pyro4
import time
import sys
import pickle
import socket
import numpy as np
import pandas as pd
from pprint import pprint

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

ipAddressServer='192.168.1.242'
connectionPort='5001'

@Pyro4.expose
class Embedded_Server(object):
    def __init__(self, daemon):
        self.daemon = daemon
        
    def Pyro_test_call(self,client_host_name,client_host_ip):
        print(f"Hello Pyro Client!!")
        print(f"A connection received from {client_host_name} with IP: {client_host_ip}")
        return socket.gethostname(),ipAddressServer
    
    def lst_IV_datasets(self):
        dataset=[os.path.splitext(x)[0] for x in os.listdir('./I-V_data')]
        return dataset


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

# xx=df['t'].head().diff()
# xx=xx.dropna().reset_index(drop=True)
# xx.mean().round(2)