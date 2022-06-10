
from DDS import DDS
from mongo import MyMongoDB
import openrouteservice as ors

client1 = ors.Client(key='5b3ce3597851110001cf6248c40727486c3b4440a5338bb9cc551c58')
client2 = ors.Client(key='5b3ce3597851110001cf624873cfc5a6a9e34d7eba09987f00e30062')
client3 = ors.Client(key='5b3ce3597851110001cf62482f52e3003f4347459e93daca8d62d292')
client4 = ors.Client(key='5b3ce3597851110001cf6248b852cf5e68084fbc95a61d739c48b976')


nbr_type = 2 #int(input("Donner le nombre de types de camions : "))
capacities = {}
for i in range(nbr_type):
  cap = int(input("Donner la capacité par palette du camion de type "+ str(i+1) + " : " ))
  capacities[i+1] = cap

melanger = 'oui'#input("Mélanger les commandes dans une seule et même unité ? Oui / Non : ")
if melanger.lower() == 'oui':
  mix = True
else :
  mix = False

uzine=(33.50277, -7.64445)
file_clients = 'files\danone casa sud.xlsx'
file_cmds = 'files\input commandes.xlsx'

tmps_max = 1000


mongo = MyMongoDB()

prefrence = 'fastest'


dds = DDS(file_clients,file_cmds,uzine,1,mongo,tmps_max,nbr_type,capacities,mix,prefrence)