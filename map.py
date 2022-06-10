import folium
import webbrowser
import io
import geojson
import json
import folium
import matplotlib.pyplot as plt
import numpy as np
from collections import Counter
from geojson import Point, Feature, FeatureCollection, dump
import openrouteservice as ors
import sys
from folium import plugins
from folium.features import DivIcon
from collections import defaultdict
import pandas as pd
from geojson import MultiPoint
import os
import glob
from folium import plugins
import openrouteservice as ors
import functions



class Map:
    def __init__(self ,dict_clients_types,uzine, userID,df,orsClient):
        self.df = df
        self.dict_clients_types = dict_clients_types
        self.uzine = uzine
        self.userID = userID
        self.orsClient = orsClient
        self.generate_maps_folder()
        self.clientORS  = ors.Client(key='5b3ce3597851110001cf6248b852cf5e68084fbc95a61d739c48b976')

    
    def generate_maps_folder(self):
        self.current_directory = os.getcwd()
        self.maps_html = os.path.join(self.current_directory, r'data/user_' + str(self.userID) +'/maps_html')
        if not os.path.exists(self.maps_html):
            os.makedirs(self.maps_html)
        for key in self.dict_clients_types.keys():
            files = glob.glob(self.maps_html + '/type_' + str(key) +'/*')
            for f in files:
                os.remove(f)





    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list



    
   





    def export_map(self,typeCleint,group):
        Myclients = self.dict_clients_types[typeCleint]['dict_all']
        mycoord = []
        mycoord.append(list(reversed(self.uzine)))
        for v in Myclients[group]:
            mycoord.append(list(reversed(v)))
        mycoord.append(list(reversed(self.uzine)))
        route = self.clientORS.directions(
            coordinates=mycoord,
            profile='driving-car',
            format='geojson',
            preference = 'fastest',
            optimize_waypoints=True,
            validate = True,
            radiuses=10000,
        )
        duration = route['features'][0]['properties']['summary']['duration'] / 60 + functions.somme_temps_attente(mycoord,self.df)
        mapEquipe = folium.Map(location = self.uzine, width = "100%", zoom_start = 10) 
        df_equipe = pd.DataFrame()
        coords = route['metadata']['query']['coordinates']
        for idx, cord in enumerate(coords):
            folium.Marker(location=list(reversed(cord)),popup=str(idx),icon=folium.Icon(icon_color='#ffffff',icon='fa-user',  prefix='fa')).add_to(mapEquipe)
            folium.map.Marker(location=list(reversed(cord)),icon=DivIcon(icon_size=(250,36),icon_anchor=(0,0),html='<div style="width: 25px;font-size:15px;font-weight: bold; background-color: yellow;">P'+str(idx)+'</div>',)).add_to(mapEquipe)
            cord2=str(cord[1])+' '+str(cord[0])
            df3 = self.df.loc[self.df['coords'] == cord2 ]
            df_equipe = df_equipe.append(df3)
        folium.Marker(location=list(self.uzine),icon=folium.Icon(icon_color='#ffffff',icon='fa-industry',  prefix='fa')).add_to(mapEquipe)
        folium.map.Marker(location=list(reversed(cord)),icon=DivIcon(icon_size=(250,36),icon_anchor=(0,0),html='<div style="width: 40px;font-size:15px;font-weight: bold; background-color: yellow;">Uzine</div>',)).add_to(mapEquipe)
        folium.PolyLine(locations=[list(reversed(coord)) 
                                for coord in 
                                route['features'][0]['geometry']['coordinates']],weight=6,delay=1000).add_to(mapEquipe) 
        type_path = self.maps_html + '/type_' + str(typeCleint)
        if not os.path.exists(type_path):
            os.makedirs(type_path)
        mapEquipe.save(type_path + "/map_" + str(group) + ".html")



    
    def export_all_maps(self):
        for key in self.dict_clients_types.keys():
            for group in self.dict_clients_types[key]['dict_all'].keys():
                self.export_map(key,group)



   

   

