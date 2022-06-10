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



class Map:
    def __init__(self, location ,dict_clients_types,uzine, userID):
        self.dict_clients_types = dict_clients_types
        self.uzine = uzine
        self.location = location
        self.userID = userID
        self.generate_maps_folder()

    
    def generate_maps_folder(self):
        self.current_directory = os.getcwd()
        self.maps_html = os.path.join(self.current_directory, r'data/user_' + str(self.userID) +'/maps_html')
        if not os.path.exists(self.maps_html):
            os.makedirs(self.maps_html)
        files = glob.glob(self.maps_html + '/*')
        for f in files:
            os.remove(f)





    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list



    
    def export_map(self,typeCleint):
        self.map_UMM = folium.Map(location = self.location, width = "100%", zoom_start = 10) 
        data = self.dict_clients_types[typeCleint]
        for group in range(len(data['dict_all'])):
            cords = []
            latt=[row[0] for row in data['dict_all'][group]]
            longg=[row[1] for row in data['dict_all'][group]]
            list1=self.merge(latt, longg)
            geo_json=MultiPoint(list1)
            cords.append(list1)
            cords[0].append(self.uzine)
            for idx, coords in enumerate(cords[0]):
                if(len(cords[0])-1 == idx):  
                    folium.Marker(location=list(reversed(coords)),icon=folium.Icon(icon_color='#ffffff',icon='fa-industry',  prefix='fa')).add_to(self.map_UMM)
                    folium.map.Marker(location=list(reversed(coords)),icon=DivIcon(icon_size=(250,36),icon_anchor=(0,0),html='<div style = "width: 60px;font-size:15px;font-weight: bold; background-color: yellow;">Entrepôt</div>',)).add_to(self.map_UMM)
                else:
                    folium.Marker(location=list(reversed(coords)),popup=str(group),icon=folium.Icon(icon_color='#ffffff',icon='fa-user',  prefix='fa')).add_to(self.map_UMM)
                    folium.map.Marker(location=list(reversed(coords)),icon=DivIcon(icon_size=(250,36),icon_anchor=(0,0),html='<div style="width: 50px;font-size:15px;font-weight: bold; background-color: yellow;">Point '+str(idx)+'</div>',)).add_to(self.map_UMM)


            #folium.PolyLine(locations=[list(reversed(coord)) for coord in self.routes[index]['features'][0]['geometry']['coordinates']]).add_to(self.map_UMM)
            plugins.AntPath(locations=[list(reversed(coord)) for coord in data['routes'][group]['features'][0]['geometry']['coordinates']]).add_to(self.map_UMM)
            type_path = self.maps_html + '/type_' + str(typeCleint)
            if not os.path.exists(type_path):
                os.makedirs(type_path)
            self.map_UMM.save(type_path + "/map_" + str(group) + ".html")

    
    def export_all_maps(self):
        for key in self.dict_clients_types.keys():
            self.export_map(key)



   

   

