def somme_temps_attente(coords,df):
  somme = 0
  for coord in coords:
    c = str(coord[1]) + ' ' + str(coord[0])
    mydf = df.loc[(df['coords'] == c)]
    if(len(mydf) == 0):
      tps = 0
    else:
      tps = mydf["Tps d'attente"].values[0]
      tps = tps.replace('min','')
      tps = int(tps)
    somme += tps
  return somme


def somme_commandes(coords,type,df_dict,df):
  somme = 0
  for coord in coords:
    c = str(coord[1]) + ' ' + str(coord[0])
    mydf = df_dict[type].loc[(df['coords'] == c)]
    if(len(mydf) == 0):
      commande = 0
    else:
      commande = mydf["Commandes"].values[0]
      commande = math.ceil(commande)
    somme += commande
  return somme


def somme_commandes_mix(coords,type,df_dict,df):
  somme = 0
  for coord in coords:
    c = str(coord[1]) + ' ' + str(coord[0])
    mydf = df_dict[type].loc[(df['coords'] == c)]
    if(len(mydf) == 0):
      commande = 0
    else:
      commande = mydf["Commandes"].values[0]
      commande = round(commande,2)
    somme += commande
  return round(somme,2)