import glob
import os
from geojson import MultiPoint
import geojson
import json


class OutPutFiles():
    def __init__(self,clusters,mongo,userID):
        self.current_directory = os.getcwd()
        self.map_equipe = os.path.join(self.current_directory, r'data/user_'+userID+'/map_equipe')
        self.equipes = os.path.join(self.current_directory, r'data/user_'+userID+'/equipes')
        self.excel_files = os.path.join(self.current_directory, r'data/user_'+userID+'/excel_files')
        self.dict_centers = clusters.dict_centers
        self.dict_first_clustring = clusters.dict_first_clustring
        self.dist = clusters.inputFiles.cord_uzine
        self.mongo = mongo
        self.userID = userID
        self.create_output_folders()
        self.remove_files_in_folders()
    

    def create_output_folders(self):
        if not os.path.exists(self.map_equipe):
            os.makedirs(self.map_equipe)
        if not os.path.exists(self.equipes):
            os.makedirs(self.equipes)
        if not os.path.exists(self.excel_files):
            os.makedirs(self.excel_files)
        

    
    def remove_files_in_folders(self):
        files = glob.glob(self.map_equipe + '/*')
        for f in files:
            os.remove(f)
        files = glob.glob(self.equipes + '/*')
        for f in files:
            os.remove(f)
        files = glob.glob(self.excel_files + '/*')
        for f in files:
            os.remove(f)

        
        


    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list
        
    
    def generate_equipes_output(self):
        for i in range(len(self.dict_first_clustring)):
            latt=[row[0] for row in self.dict_first_clustring[i]]
            longg=[row[1] for row in self.dict_first_clustring[i]]
            list1=self.merge(latt, longg)
            geo_json=MultiPoint(list1)
            geo_json['myid'] = i
            geo_json['userID'] = self.userID
            with open(self.equipes+'/equipe_'+str(i)+'.geojson','w') as f:
                json.dump(geo_json, f, ensure_ascii=False)
            self.mongo.insert_equipes(geo_json)

    
    def generate_map_equipe_output(self):
         for i in range(len(self.dict_centers)):
            latt=[row[0] for row in self.dict_centers[i][0]]
            longg=[row[1] for row in self.dict_centers[i][0]]
            list1=self.merge(latt, longg)
            list1.append(self.dist)
            geo_json=MultiPoint(list1)
            geo_json['myid'] = i
            geo_json['userID'] = self.userID
            with open(self.map_equipe+'/map_equipe_'+str(i)+'.geojson','w') as f:
                json.dump(geo_json, f, ensure_ascii=False)
            self.mongo.insert_map_equipes(geo_json)


    
    def export_all(self):
        self.mongo.delete_all_equipes(self.userID)
        self.mongo.delete_all_map_equipes(self.userID)
        self.generate_equipes_output()
        self.generate_map_equipe_output()









