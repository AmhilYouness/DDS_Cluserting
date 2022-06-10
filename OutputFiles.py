import glob
import os
from geojson import MultiPoint
import geojson
import json


class OutPutFiles():
    def __init__(self,dict_clients_types,mongo,userID,uzine):
        self.current_directory = os.getcwd()
        self.equipes = os.path.join(self.current_directory, r'data/user_'+str(userID)+'/equipes')
        self.excel_files = os.path.join(self.current_directory, r'data/user_'+str(userID)+'/excel_files')
        self.dict_clients_types = dict_clients_types
        self.mongo = mongo
        self.userID = userID
        self.uzine = uzine
        self.create_output_folders()
        self.remove_files_in_folders()
    

    def create_output_folders(self):
        if not os.path.exists(self.equipes):
            os.makedirs(self.equipes)
        if not os.path.exists(self.excel_files):
            os.makedirs(self.excel_files)
        

    
    def remove_files_in_folders(self):
        for key in self.dict_clients_types.keys():
            files = glob.glob(self.equipes + '/type_' + str(key) + '/*')
            for f in files:
                os.remove(f)
            files = glob.glob(self.excel_files + '/*')
            for f in files:
                os.remove(f)

        
        


    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list


    def generate_equipes_output(self):
        for typeClient,data in self.dict_clients_types.items():
            for group in range(len(data['dict_all'])):
                latt=[row[0] for row in data['dict_all'][group]]
                longg=[row[1] for row in data['dict_all'][group]]
                list1=self.merge(latt, longg)
                list1.append(self.uzine)
                geo_json=MultiPoint(list1)
                geo_json['myid'] = group
                geo_json['userID'] = self.userID
                self.MyTypepath = self.equipes +'/type_' + str(typeClient)
                if not os.path.exists(self.MyTypepath):
                    os.makedirs(self.MyTypepath)
                with open(self.MyTypepath+'/equipe_'+str(group)+'.geojson','w') as f:
                    json.dump(geo_json, f, ensure_ascii=False)
                #self.mongo.insert_map_equipes(geo_json)


    
    
    def export_all(self):
        #self.mongo.delete_all_equipes(self.userID)
        #self.mongo.delete_all_map_equipes(self.userID)
        self.generate_equipes_output()









