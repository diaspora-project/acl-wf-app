import os
import Pyro4
import time
import sys
import pandas as pd

import data_handling

Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"

# to run instrument_control.py via cmd
# python instrument_control.py ipServerAddress=127.0.0.1 connectionPort=443

datasetPath='./I-V_data'
#datasetPath="instrument_mService/I-V_data/"
@Pyro4.expose
class Embedded_Server(object):
    def __init__(self, daemon):
        self.daemon = daemon
    
    def lst_IV_dataset(self, pathInclude=False,type='relative') -> list:
        dataset=[os.path.splitext(x)[0] for x in os.listdir(datasetPath)]
        if pathInclude:
            dataset = os.listdir(datasetPath)
            if type == 'absolute':
                dataset = [os.path.abspath(y) for y in (os.path.join(datasetPath, x) for x in dataset)]
            else:
                dataset=[os.path.relpath(y) for y in (os.path.join(datasetPath, x) for x in dataset)]
        dataset_size = [os.path.getsize(x) for x in dataset]
        return dataset,dataset_size

    def get_IV_measurement(self, dataset_file,size=None,timestamp=False)-> pd.DataFrame:
        """
        :param dataset_file:
        :param size: default is None.
        if there is a size it should be in byte and larger than measurement file to replicate data to that size
        :param timestamp: default is False. if True means fetch the timestamp of recording the reaction datasample
        :return: dataframe of the potential (I), voltage (V), and possibly the timestamp.
        the return dataframe may be replicated based on the given size.
        """
        dataset_df=data_handling.get_measurement(os.path.dirname(dataset_file),os.path.basename(dataset_file),timestamp)
        if size is not None:
            df_size=data_handling.get_measurement_size(dataset_df)
            IV_df_replication=size//df_size
            if IV_df_replication >1:
                dataset_df=data_handling.duplicate_IV_measurement(dataset_df,IV_df_replication)
            if timestamp:
                columns=['t','I','Ewe']
            else:
                columns=['I','Ewe']
            dataset_df=data_handling.extract_measurement_parameters(dataset_df,columns)

        return dataset_df

    def stream_IV_measurement(self, dataset_file, size=None, timestamp=False):
        """
        unlike get_IV_measurement, this method is to stream measurement from instrument facility to the workflow orchestrator based on the timestamp of each collected point in the reaction.
        this method is TODO and to figure out which is the proper streaming mechanism to apply
        """
        pass


    @Pyro4.oneway
    def shutdown(self):
        print(f'Ecosystem communication session is terminated ')
        self.daemon.shutdown()

    



if __name__ == '__main__':
    ipAddressServer=(sys.argv[1]).split('=')[1]
    connectionPort=(sys.argv[2]).split('=')[1]
    # ipAddressServer='127.0.0.1'
    # connectionPort='443'
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
