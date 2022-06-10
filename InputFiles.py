from geojson import MultiPoint
import geojson
import numpy as np
import pandas as pd
import math


class InputFiles():
    def __init__(self,file_clients,file_commandes,mongo,userID,mix):
        self.file_clients = file_clients
        self.file_commandes = file_commandes
        self.mongo = mongo
        self.userID = userID
        self.mix = mix
        self.generate_clients()
        self.generate_commandes()
        self.generate_df_principale()

    
   
    
    def generate_clients(self):
        self.df_clients = pd.read_excel(self.file_clients,sheet_name="Feuil1")
        self.df_clients['coords']=self.df_clients['Adresse GPS latitude'].astype(str)+' '+self.df_clients['Adresse GPS longitude'].astype(str)
        self.df_clients.drop_duplicates(subset=['coords'] , inplace = True)
        self.df_clients.dropna(inplace = True)
        self.df_clients["Type camion"] = self.df_clients['Type camion'].astype('int')
        self.df_clients['Adresse GPS longitude'] = self.df_clients['Adresse GPS longitude'].astype(float)
        self.df_clients['Adresse GPS latitude'] = self.df_clients['Adresse GPS latitude'].astype(float)



    def generate_commandes(self):
        self.df_cmds = pd.read_excel(self.file_commandes)
        self.df_cmds['coords']=self.df_cmds['Adresse GPS latitude'].astype(str)+' '+self.df_cmds['Adresse GPS longitude'].astype(str)
        self.df_cmds.drop_duplicates(subset=['coords'] , inplace = True)
        self.df_cmds.dropna(inplace = True)
        self.df_cmds['Adresse GPS longitude'] = self.df_cmds['Adresse GPS longitude'].astype(float)
        self.df_cmds['Adresse GPS latitude'] = self.df_cmds['Adresse GPS latitude'].astype(float)
        if not self.mix :
            mycmds = []
            for ind,row in self.df_cmds.iterrows():
                mycmds.append(math.ceil(row['Commandes']))
            self.df_cmds['Commandes'] = mycmds 

    
    def generate_df_principale(self):
        self.df_principale = pd.merge(self.df_cmds, self.df_clients, on=['coords','Adresse GPS latitude','Adresse GPS longitude'])
        
    








