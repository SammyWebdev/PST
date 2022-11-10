import webbrowser
import osmapi as osm
import folium
import codecs
ids=[36862660, 86953877, 678537601, 678537289, 678537291] #This will be a place for your ID's list
boulder_coords = [41.3874, 2.1686]
my_map = folium.Map(location = boulder_coords, zoom_start = 7.5)
for id in ids:
    name=str(id)
    with codecs.open('./geojson/'+name+'.geojson', 'r', encoding='utf-8') as data:
        geojson= data.read()
    folium.GeoJson(geojson, name=name).add_to(my_map)
folium.LayerControl().add_to(my_map)
my_map.save('map.html')
my_map.save("map.html")
webbrowser.open("map.html")