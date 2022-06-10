from collections import Counter
from k_means_constrained import KMeansConstrained
from sklearn.cluster import KMeans
from geopy.distance import distance as geodist
from scipy.spatial.distance import pdist, squareform
import math
import functions
import numpy as np
import openrouteservice as ors




class Clustring():
    def __init__(self,type,data,df,df_dict,inputFiles,uzine,capacities,mix,time_max,preference):
        self.inputFiles = inputFiles
        self.type = type
        self.data = data
        self.capacities = capacities
        self.mix = mix
        self.time_max = time_max
        self.uzine = uzine
        self.preference = preference
        self.uzine = uzine
        self.df = df
        self.df_dict = df_dict
        self.generate_data()
        self.play()


    
    def generate_data(self):
        self.coordinates= self.data['coords'].str.split(expand=True).applymap(float).values.tolist()
        self.coordinates = np.array(self.coordinates)
        if self.mix :
            self.sum_commands = float(self.data['Commandes'].sum())
        else:
            self.sum_commands = int(self.data['Commandes'].sum())
        self.capacite = self.capacities[self.type]
        print("La somme des commandes pour type ",self.type," : ",self.sum_commands)
        print("la capacité de camion type ",self.type," : ",self.capacite)
        self.Nbr_clusters = math.ceil(self.sum_commands / self.capacite) 
        print("Nombre de clusters initiale : ",self.Nbr_clusters)
        


    
    def play(self):
        client1 = ors.Client(key='5b3ce3597851110001cf6248c40727486c3b4440a5338bb9cc551c58')
        max_duration = self.time_max + 1
        max_commande = self.capacite + 1
        itr = 0
        while (max_duration > self.time_max or max_commande > self.capacite ) :
            list_durations = []
            list_commandes = []
            too_many = False
            itr = itr + 1
            algo = KMeans(n_clusters=self.Nbr_clusters)
            algo.fit(self.coordinates)
            c=algo.predict(self.coordinates)
            most_common,num_most_common = Counter(c).most_common(1)[0]
            centroids  = algo.cluster_centers_ 
            dict_all = {}
            dict_routes = {}
            for j in range(self.Nbr_clusters):
                dict_all[j] = []
                for i in range(len(c)):
                    if(c[i]==j):
                        dict_all[j].append(self.coordinates[i].tolist())
                if(len(dict_all[j]) > 70):
                    too_many = True
            if too_many : 
                self.Nbr_clusters = self.Nbr_clusters + 1
                continue
            for key , value in dict_all.items():
                mycoord = []
                mycoord.append(list(reversed(self.uzine)))
                for v in value:
                    mycoord.append(list(reversed(v)))
                mycoord.append(list(reversed(self.uzine)))
                
                route = client1.directions(
                    coordinates=mycoord,
                    profile='driving-car',
                    format='geojson',
                    preference = self.preference,
                    optimize_waypoints=True,
                    validate = True,
                    radiuses=10000,
                )
                dict_routes[key] = route
                duration = route['features'][0]['properties']['summary']['duration'] / 60 + functions. somme_temps_attente(mycoord,self.df)
                list_durations.append(duration)
                if self.mix : commandes = functions.somme_commandes_mix(mycoord,self.type,self.df_dict,self.df)
                else :  commandes = functions.somme_commandes(mycoord,self.type,self.df_dict,self.df)
                list_commandes.append(commandes)

            max_duration = max(list_durations)
            max_commande = max(list_commandes)
            print(self.Nbr_clusters)
            print(list_durations)
            print(list_commandes)
            if itr == 0 : self.Nbr_clusters = self.Nbr_clusters + 1 ; itr = 0;

        if itr == 0 : self.Nbr_clusters = self.Nbr_clusters - 1
        print("Nombre groups : ",self.Nbr_clusters)
        self.dict_clients_types[self.type] = {'nbrClusters' : self.Nbr_clusters , 'dict_all' : dict_all , 'centroids' : centroids , 'list_durations' : list_durations , 'list_commandes' : list_commandes }





                


    
   

            

       
        
           

    



