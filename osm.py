# Fabi API info:
#   Die mit den id's zu ändernde / überschreibende Liste (bei mir set, damit id-Dopplungen von vornherein ausgeschlossen sind)
#   heißt <uids>.
#
#   Die Ergebnisse sind in dem dict <results> nach key=uid.
#
#   Der Methodenaufruf <print_per_uid_ptty(name=True)> ist nicht notwendig und nur zur Veranschaulichung der erhaltenen Daten.
# ----------------------------------------------------------------------------------


def osm_main(osm_id_list):
    print("osm_main()")
    return search_near_by(osm_id_list)


print("\n\n" + "<" + "=" * 150 + ">")

import requests
import json
import time

# user id's (or search id's, probably a better name :) TODO rename
sample_uids = {
    36862660,
    86953877,
    678537601,
    678537289,
    678537291,
    3870914569,
}  # obtained from Fabi, this is just for sample testing

# uids = {678537289, 3870914569}  # for request easy testing TODO remove

results = {}  # dict<uid: query_result["elements"]>


def search_near_by(osm_id_list):
    overpass_url = "http://overpass-api.de/api/interpreter"
    search_radius = 500
    max_search_radius = 2000
    include_shops = False
    global results

    print(f"search_near_by(osm_id_list={osm_id_list})")
    include_searchplace = False  # should stay that way
    sp = ";nwr._->.res;out center;" if include_searchplace else "->.res;"

    print("Fetching Data...", end="\n" * 2)
    for uid in osm_id_list:
        search_radius = 500  # resetting search_radius
        while search_radius <= max_search_radius:
            print(f"For uid={uid}: sending query with radius={search_radius}")
            overpass_query = (
                f"[out:json][timeout:500];nwr(id:{uid}){sp}(nwr[amenity=bar](around.res:{search_radius});nwr[amenity=pub](around.res:{search_radius});nwr[amenity=biergarten](around.res:{search_radius});"
                + (
                    f"nwr[shop=alcohol](around.res:{search_radius});nwr[shop=beverages](around.res:{search_radius}););"
                    if include_shops
                    else ");"
                )
                + "out center;"
            )
            try:
                response = requests.get(overpass_url, params={"data": overpass_query})
                result = response.json()
            except:
                print(
                    f"Exception occured during data query: {response.status_code}"
                    + (
                        " (Too many requests)"
                        if response.status_code == 429
                        else " (Bad request)"
                        if response.status_code == 400
                        else " (Gateway Timeout)"
                        if response.status_code == 504
                        else " (unknown cause :)"
                    )
                )  # 400 is bad request, 429 is too many requests, 200 is ok

            # debugging status codes
            # print(f"status: {response.status_code}")

            # dealing with empty result
            if result["elements"] == []:
                search_radius += 500  # expanding search radius
                time.sleep(1)
            else:
                # print("debug", result)
                break  # stops further querying

        results[uid] = (
            f"No results {search_radius}m near uid {uid} !"
            if result["elements"] == []
            else result["elements"]
        )

    return results


# TODO remove or fix
def print_per_uid(uids,results):
    print("print_per_uid()")
    for uid in uids:
        print(
            f"(uid={uid}):",
            str(results[uid])[:1000],
            "\b..." if len(str(str(results[uid]))) > 999 else "\b",
            end="\n" * 2,
        )


def print_per_uid_ptty(uids, name=True):  # pretty prints the results
    print(f"print_per_uid_ptty(name={name})")
    for uid in uids:
        print(f"(uid={uid}):")

        # TODO reintroduce try except
        # try:
        if type(results[uid]) == str:  # ...means there weren't any results
            print(f"\t{results[uid]}")
        else:
            for element in results[uid]:
                if name:
                    try:
                        print(
                            "\t{} (eid={})".format(
                                element["tags"]["name"], element["id"]
                            ),

                            end="",
                        )  # TODO check if putting it in here was neccessary... befor it was directly after name
                        found_addr = False
                        addr_string = ', Address: "'
                        print(addr_string, end="")
                        addr = {  # possible address components
                            "city": "_",
                            "country": "_",
                            "housenumber": "_",
                            "postcode": "_",
                            "street": "_",
                        }
                        tags = element["tags"]
                        for tag_key, _ in tags.items():
                            if tag_key[:4] == "addr":  # finds address components
                                found_addr = True
                                addr[tag_key[5:]] = tags[tag_key]
                                # print("debug:", addr, tag_key)
                            else:
                                pass  # key isn't part of an address
                        if found_addr:
                            print(
                                addr["street"],
                                addr["housenumber"],
                                addr["postcode"],
                                addr["city"],
                                end='"\n',
                            )
                        else:

                            print('No Address given."')
                    except:
                        # print("Element doesn't have tags")
                        print(
                            f"\tError occured with element:{element}\n...likely doesn't have a name tagged"
                        )
                else:
                    print("\t(eid={}): {}".format(element.get("id"), element))

        # except Exception as e:
        #     print(f"\tException occured while printing results: {e}")
        #     print(f"\t{results[uid]}")  # when there are no results

        print("-" * 50)

if __name__ == "__main__":
    osm_main(sample_uids)
    print_per_uid_ptty(sample_uids)

# debugging
# print(results)
