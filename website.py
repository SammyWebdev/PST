import webbrowser
import osmapi as osm
import folium
import codecs

def show_at_map(uids,results,kontakte_daten,name = True):
    print("show at map")
    bereich = [51.879092, 9.640534]
    my_map = folium.Map(location=bereich, zoom_start=7.5)
    for uid in uids:
        print(f"(uid={uid}):")


        # TODO reintroduce try except
        # try:
        if type(results[uid]) == str:  # ...means there weren't any results
            print(f"\t{results[uid]}")
        else:
            for element in results[uid]:
                try:
                    print(element)
                    if name:
                        lon = element['lon']
                        lat = element['lat']
                        name = element["tags"]["name"]
                        folium.Marker([lat,lon],popup="<i>Mt. Hood Meadows</i>", tooltip=name).add_to(my_map)
                except:
                    # print("Element doesn't have dtags")
                    print(
                        f"\tError occured with element:{element}\n...likely doesn't have a name tagged"
                    )
    for elements in kontakte_daten:
        lon = elements[2][1]
        lat = elements[2][0]
        name = elements[0]
        folium.Marker([lat, lon], popup="<i>Mt. Hood Meadows</i>", tooltip=name).add_to(my_map)
    folium.LayerControl().add_to(my_map)
    my_map.save('map.html')
    webbrowser.open("map.html")
