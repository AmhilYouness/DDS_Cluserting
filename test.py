
from DDS import DDS
from mongo import MyMongoDB




nbr_type = int(input("Donner le nombre de types de camions : "))
capacities = {}
for i in range(nbr_type):
  cap = int(input("Donner la capacité par palette du camion de type "+ str(i+1) + " : " ))
  capacities[i+1] = cap

melanger = input("Mélanger les commandes dans une seule et même unité ? Oui / Non : ")
if melanger.lower() == 'oui':
  mix = True
else :
  mix = False

uzine=(33.50277, -7.64445)
file_clients = 'files\danone casa sud.xlsx'
file_cmds = 'files\input commandes.xlsx'

tmps_max = 1000


mongo = MyMongoDB()


test = DDS(file_clients,file_cmds,uzine,1,mongo,tmps_max,nbr_type,capacities,mix,'fastest')