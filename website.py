import webbrowser
import osmapi as osm
import folium
import codecs

def show_at_map(uids, results, kontakte_daten, name = True, min_width=None, max_width=None):
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
                     #   print(24)
                        lat = element['lat']
                      #  print(26)
                        name = element["tags"]["name"]
                       # print(28)
                        amenity = element["tags"]['amenity']
                    #    print(30)
                        icon = choose_icon(amenity)
                        print(32)
                        try :
                            website = element['tags']['website']
                            print(website)
                            folium.Marker([lat, lon],
                                          icon=folium.CustomIcon(icon, icon_size=(15, 15), icon_anchor=(15, 15)),
                                          popup='Website: ' + website, tooltip=name).add_to(my_map)
                        except:
                            folium.Marker([lat, lon],
                                          icon=folium.CustomIcon(icon, icon_size=(15, 15), icon_anchor=(15, 15)),
                                          popup="<i>Error 404 keine Website hinterlegt </i>", tooltip=name).add_to(my_map)
                            print('keine Website')
                        # bar Öffungszeiten und web adresse anzeigen Fabi
                      #  print(34)
                     #   print('icon: ' + icon)

                except:
                    # print("Element doesn't have dtags")
                    print(
                        f"\tError occured with element:{element}\n...likely doesn't have a name tagged"
                    )
    for elements in kontakte_daten:
        lon = elements[2][1]
        lat = elements[2][0]
        name = elements[0]
        tel = elements[1]
        print(tel)
        folium.Marker([lat, lon], popup = folium.Popup("Tel: " +tel, parse_html=True, max_width=200) , tooltip=name).add_to(my_map)
    folium.LayerControl().add_to(my_map)
    my_map.save('map.html')
    webbrowser.open("map.html")

def choose_icon(amenity):
    print('amenity: ' + amenity)
    if amenity == "bar":
        return 'bier.png'
    elif amenity == "biergarten":
        return "bier.png"
    elif amenity == "bus_station":
        return 'bus.png'
    elif amenity == "pub":
        return "bier.png"