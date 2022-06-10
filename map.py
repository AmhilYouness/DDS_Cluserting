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
    def __init__(self, location ,centres,uzine, routes, userID):
        self.centres = centres
        self.uzine = uzine
        self.routes = routes
        self.location = location
        self.userID = userID
        self.generate_maps_folder()

    
    def generate_maps_folder(self):
        self.current_directory = os.getcwd()
        self.maps_html = os.path.join(self.current_directory, r'data/user_' + self.userID +'/maps_html')
        if not os.path.exists(self.maps_html):
            os.makedirs(self.maps_html)
        files = glob.glob(self.maps_html + '/*')
        for f in files:
            os.remove(f)





    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list



    
    def export_map(self,index):
        self.map_UMM = folium.Map(location = self.location, width = "100%", zoom_start = 10) # max zoom: 13
        cords = []
        for i in range(len(self.centres[index])):
            latt=[row[0] for row in self.centres[index][i]]
            longg=[row[1] for row in self.centres[index][i]]
            list1=self.merge(latt, longg)
            geo_json=MultiPoint(list1)
            cords.append(list1)
        cords[0].append(self.uzine)
        for idx, coords in enumerate(cords[0]):
            if(len(cords[0])-1 == idx):  
                folium.Marker(location=list(reversed(coords)),icon=folium.Icon(icon_color='#ffffff',icon='fa-industry',  prefix='fa')).add_to(self.map_UMM)
                folium.map.Marker(location=list(reversed(coords)),icon=DivIcon(icon_size=(250,36),icon_anchor=(0,0),html='<div style = "width: 60px;font-size:15px;font-weight: bold; background-color: yellow;">Entrepôt</div>',)).add_to(self.map_UMM)
            else:
                html="""<h1>Détails : </h1><br>"""
                html+= "<h3>" + "Temps d'arrivé :"+ str(00) +"</h3>"
                html+= "<h3>" + str(3)+" Personnes :</h3>"
                iframe = folium.IFrame(html=html, width=300, height=200)
                popup = folium.Popup(iframe, max_width=2650)
                folium.Marker(location=list(reversed(coords)),popup=popup,icon=folium.Icon(icon_color='#ffffff',icon='fa-user',  prefix='fa')).add_to(self.map_UMM)
                folium.map.Marker(location=list(reversed(coords)),icon=DivIcon(icon_size=(250,36),icon_anchor=(0,0),html='<div style="width: 50px;font-size:15px;font-weight: bold; background-color: yellow;">Point '+str(idx)+'</div>',)).add_to(self.map_UMM)
   

        #folium.PolyLine(locations=[list(reversed(coord)) for coord in self.routes[index]['features'][0]['geometry']['coordinates']]).add_to(self.map_UMM)
        plugins.AntPath(locations=[list(reversed(coord)) for coord in self.routes[index]['features'][0]['geometry']['coordinates']]).add_to(self.map_UMM)

        self.map_UMM.save(self.maps_html + "/map_" + str(index) + ".html")
        #webbrowser.open(self.maps_html + "/map_" + str(index) + ".html")

    
    def export_all_maps(self):
        for key in range(len(self.routes)):
            self.export_map(key)



   

   

