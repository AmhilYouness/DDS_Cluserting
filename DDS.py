from ExcelGenerator import ExcelGenerator
from InputFiles import InputFiles
from OutputFiles import OutPutFiles
from Clustring import Clustring
from Routing import Routing
from map import Map
from mapAll import MapAll
import json
from mongo import MyMongoDB





class DDS():
  def __init__(self,file_clients,file_commandes,uzine,userID,mongo,time_max,nbr_type,capacities,mix,preference,orsClient,heure_debut,min_debut):
      self.userID = userID
      self.mongo = mongo
      self.time_max = time_max
      self.nbr_type = nbr_type
      self.capacities = capacities
      self.mix = mix
      self.preference = preference
      self.uzine = uzine
      self.orsClient = orsClient
      self.heure_debut = heure_debut
      self.min_debut = min_debut
      self.inputFiles = InputFiles(file_clients,file_commandes,self.mongo,self.userID,self.mix)
      self.df =  self.inputFiles.df_principale;
      self.play()
      self.export()




  def play(self):
    self.df_dict = {type: self.df[self.df['Type camion'] == type] for type in self.df['Type camion'].unique()}
    if len(self.df_dict) - 1 != self.nbr_type : raise Exception("Sorry, Number of types in the excel file is diffrente from the number you typed !") 
    self.dict_clients_types = {}
    for dict_key,data in self.df_dict.items():
      if dict_key != 0 :
        self.MyClusters = Clustring(dict_key,data,self.df,self.df_dict,self.inputFiles,self.uzine,self.capacities,self.mix,self.time_max,self.preference,self.orsClient)
        self.dict_clients_types[dict_key] = {'nbrClusters' : self.MyClusters.Nbr_clusters , 'dict_all' : self.MyClusters.dict_all , 'centroids' : self.MyClusters.centroids , 'list_durations' : self.MyClusters.list_durations , 'list_commandes' : self.MyClusters.list_commandes , 'routes' : self.MyClusters.dict_routes }
        print('successfully, besoin de ',self.dict_clients_types[dict_key]['nbrClusters'],'bus au total pour type ',dict_key) 



  def export(self):
      outPut = OutPutFiles(self.dict_clients_types,self.mongo,self.userID,self.uzine)
      outPut.export_all()
      location = list(reversed(self.uzine))
      map = Map(self.dict_clients_types,self.uzine,self.userID,self.df,self.orsClient)
      map.export_all_maps()
      excel = ExcelGenerator(self.heure_debut,self.min_dep,self.dict_clients_types ,self.inputFiles, self.uzine, self.mongo,self.userID)
      excel.export()
     
      


  


  
"""  def export(self):
    for key, value in self.MyRoutes.routes.items():
      self.mongo.insert_routes(value)
    outPut = OutPutFiles(self.MyClusters,self.mongo,self.userID)
    outPut.export_all()
    excel = ExcelGenerator(hour_dep,min_dep,self.MyClusters , self.MyRoutes.routes, self.mongo,self.userID)
    excel.export()
    location = list(reversed(self.inputFiles.cord_uzine))
    map = Map(location,self.MyClusters.dict_centers,self.MyClusters.inputFiles.cord_uzine,self.MyRoutes.routes,self.userID)
    map.export_all_maps()
    mapAll = MapAll(location,self.userID)
    mapAll.saveMap()
    print("done")"""












