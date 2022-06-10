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
from random import randint




class MapAll:
    def __init__(self,location,userID):
        self.location = location
        self.userID = userID
        self.color = []
        for i in range(20):
            self.color.append('#%06X' % randint(0, 0xFFFFFF))



   

    
    def saveMap(self):
        self.map_UMM = folium.Map(location = self.location, width = "100%", zoom_start = 10) # max zoom: 13
        colors = [
            'red',
            'blue',
            'gray',
            'darkred',
            'lightred',
            'orange',
            'beige',
            'green',
            'darkgreen',
            'lightgreen',
            'darkblue',
            'lightblue',
            'purple',
            'darkpurple',
            'pink',
            'cadetblue',
            'lightgray',
            'black'
        ]
        directory = 'data/user_' + self.userID + '/map_equipe'
        for i ,filename in enumerate(os.listdir(directory)):
            file = os.path.join(directory, filename)        
            with open(file) as f:
                gj = geojson.load(f)
            coordinates = gj['coordinates']
            for idx, coords in enumerate(coordinates):
                folium.Marker(location=list(reversed(coords)),color = "yellow",popup=folium.Popup("ID: {}".format(idx)),icon = folium.Icon(color=colors[i])).add_to(self.map_UMM)

        #Display the map
        self.map_UMM.save("data/user_" + self.userID + "/mapall.html")
        #webbrowser.open("data/user_" + self.userID  + "/mapall.html")


