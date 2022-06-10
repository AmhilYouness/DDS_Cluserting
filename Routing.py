import openrouteservice as ors
from geojson import MultiPoint



class Routing():
    def __init__(self,clusters,preference='fastest' , profile = 'driving-car' , key = '5b3ce3597851110001cf624873cfc5a6a9e34d7eba09987f00e30062'):
        self.c = clusters
        self.preference = preference
        self.client = ors.Client(key=key)
        self.routes = {}
        self.directions()

        

    def merge(self,list1, list2):
        merged_list = [(list1[i], list2[i]) for i in range(0, len(list1))]
        return merged_list



    
    def directions(self):
        list_tour = []
        k = 0
        for points in self.c.dict_centers.values():
            cord = []
            for i in range(len(points)):
                latt=[row[0] for row in points[i]]
                longg=[row[1] for row in points[i]]
                list1=self.merge(latt, longg)
                geo_json=MultiPoint(list1)
                cord.append(list1)
            #cord[0].append(self.c.inputFiles.cord_uzine)
            cord[0].append((33.50277,-7.64445))
            print(cord[0])
            route = self.client.directions(
                coordinates=cord[0],
                profile='driving-car',
                format='geojson',
                preference = self.preference,
                radiuses=10000,
                optimize_waypoints = True,
                validate = True,
            )

            self.routes[k] = route
            k = k + 1
            list_tour.append(route['features'][0]['properties']['summary']['duration']/60)
        self.time_calc=max(list_tour)






