
import Pyro4
import os
import sys
import pickle
import pandas as pd



Pyro4.config.SERIALIZERS_ACCEPTED.add('pickle')
Pyro4.config.SERIALIZER = "pickle"


class ACL_Pyro_Objects:
    def __init__(self,ipAddressServer,connectionPort):
        self._connection = Pyro4.core.Proxy('PYRO:Pyro_Server@' + ipAddressServer + ':' + connectionPort)

    def get_IV_dataset(self):
        """
        three types of returned I-V datasets:
        1- lst_IV_datasets(): return just dataset file names (default)
        2- lst_IV_datasets(pathInclude=True): return datasets with relative paths
        3- lst_IV_datasets(pathInclude=True,type='absolute'): return datasets with absolute paths
        """
        try:
            IV_dataset, dataset_size = self._connection.lst_IV_dataset(pathInclude=True)
            for i in range(len(IV_dataset)):
                print(f'{IV_dataset[i]}: size: {dataset_size[i]} bytes')
        except Exception as e:
            print(e.args)


    def get_IV_data(self, fileName, size=None, timestamp=False) -> pd.DataFrame:
        try:
            IV_df = self._connection.get_IV_measurement(fileName, size, timestamp)
            # print(IV_df)
            # print(len(IV_df['I']))
        except Exception as e:
            print(e.args)
        return IV_df


    def call_Shutdown(self):
        try:
            self._connection.shutdown()
            self._connection._pyroRelease()
        except Exception as e:
            print(e.args)