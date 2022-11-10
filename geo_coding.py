import pandas as pd
import folium
from geopy.geocoders import Nominatim

def get_osm_id(dfkontakte):
    print('geo coding start')
    print(dfkontakte.shape)
    List = get_coordinates(dfkontakte)
    osm_id_list =search_around(List)
    return osm_id_list
def search_around(list):
    print('hi')
    locator = Nominatim(user_agent="myGeocoder")
    osm_id_list =[]
    for items in list:
        x = items[2][0]
        y = items[2][1]
        coordinates = x, y
        location = locator.reverse(coordinates)
        osm_id_list.append(location.raw['osm_id'])
        print('Name: ' + items[0])
        print(location.raw['osm_id'])
    print(osm_id_list)
    return(osm_id_list)
#______________________________gibt die Coordinaten ader Adressen Zurück_________________________________
def get_coordinates(dfkontakte):
    #print(dfkontakte.shape)
    i = 0
    loc = Nominatim(user_agent="GetLoc")
    List=[]
    while i < dfkontakte.shape[0]:
        print('hi')
        print(str(i))
        Plz =dfkontakte.loc[i].get('Plz')
        ort = dfkontakte.loc[i].get('Ort')
        Street = dfkontakte.loc[i].get('Street')
        Hausnummer = dfkontakte.loc[i].get('Hausnummer')
        #print(dfkontakte)
        adresse = ort + ' ' + str(Plz).split('.')[0] + ' ' + Street + ' ' + str(Hausnummer).split('.')[0]
        #print(adresse)
        getLoc = loc.geocode(adresse) #liest geo daten aus
        print(getLoc)
        List.append((dfkontakte.loc[i].get('Name'),dfkontakte.loc[i].get('Tel'),(getLoc.latitude,getLoc.longitude))) #liste mit Namen, Tel und Koordinaten
        #print("Latitude = ", getLoc.latitude, "\n")
        #print("Longitude = ", getLoc.longitude)
        print(List)
        i = i+1
    return List
#___________simuliert durch ausgeben das Koordinaten das anzeigen auf karte welches durch wietergeben der Koordinaten geschehen würde
def show_at_map(x,y):
    boulder_coords = [40.015, -105.2705]

    # Create the map
    my_map = folium.Map()

    # Display the map
    my_map
#______________________________in arbeit
def show_List_at_map(list):
    for temp in list:
        x = temp[2][0]
        y = temp[2][1]
        name =temp[0]
        Tel = temp[1]
        print('Name: ' + name + ' Tel: ' + Tel + ' X: ' + str( x) + ' y: ' + str(y))
        #osm id angeben