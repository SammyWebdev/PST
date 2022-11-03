# Fabi API info:
#   Die mit den id's zu ändernde / überschreibende Liste (bei mir set, damit id-Dopplungen von vornherein ausgeschlossen sind)
#   heißt <uids>.
#
#   Die Ergebnisse sind in dem dict <results> nach key=uid.
#
#   Der Methodenaufruf <print_per_uid_ptty(name=True)> ist nicht notwendig und nur zur Veranschaulichung der erhaltenen Daten.
# ----------------------------------------------------------------------------------


# TODO fixes:
# - somethings I've missed :)

print("\n\n" + "<" + "=" * 150 + ">")

import requests
import json

overpass_url = "http://overpass-api.de/api/interpreter"

search_radius = 500
max_search_radius = 2000

# user id's (or search id's, probably a better name :) TODO rename
uids = {
    36862660,
    86953877,
    678537601,
    678537289,
    678537291,
    3870914569,
}  # obtained from Fabi, this is just for sample testing

# uids = {678537289, 3870914569}  # for request easy testing TODO remove

include_searchplace = False  # should stay that way
results = {}  # dict<uid: query_result["elements"]>

print("Fetching Data...", end="\n" * 2)
for uid in uids:
    search_radius = 500  # resetting search_radius
    while search_radius < max_search_radius:
        overpass_query = """
        [out:json][timeout:500];
        nwr(id:{0}){2}
        nwr[amenity=bar](around.res:{1});
        nwr[amenity=pub](around.res:{1});
        nwr[amenity=biergarten](around.res:{1});
        nwr[shop=alcohol](around.res:{1});
        nwr[shop=beverages](around.res:{1});
        out center;
        """.format(
            uid,
            search_radius,
            ";nwr._->.res;out center;" if include_searchplace else "->.res;",
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
                    else " (unknown cause :)"
                )
            )  # 400 is bad request, 429 is too many requests, 200 is ok

        # debugging status codes
        # print(f"status: {response.status_code}")

        # dealing with empty result
        if result["elements"] == []:
            search_radius += 500  # expanding search radius
        else:
            # print("debug", result)
            break  # stops further querying

    results[uid] = (
        f"No results {search_radius}m near uid {uid} !"
        if result["elements"] == []
        else result["elements"]
    )


def print_per_uid():
    for uid in uids:
        print(
            f"(uid={uid}):",
            str(results[uid])[:1000],
            "\b..." if len(str(str(results[uid]))) > 999 else "\b",
            end="\n" * 2,
        )


def print_per_uid_ptty(name=False):  # pretty prints the results
    for uid in uids:
        print(f"(uid={uid}):")
        try:
            for element in results[uid]:
                if name:
                    print(
                        "\t{} (eid={})".format(element["tags"]["name"], element["id"]),
                        end="",
                    )
                    try:
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
                        pass
                else:
                    pass
                    # print("\t(eid={}): {}".format(element.get("id"), element))
        except:
            print(f"\t{results[uid]}")  # when there are no results

        print("-" * 50)


print_per_uid_ptty(name=True)

# debugging
# print(results)
