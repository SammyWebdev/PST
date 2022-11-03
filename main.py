# Fabi API info:
#   Die mit den id's zu ändernde / überschreibende Liste (bei mir set, damit id-Dopplungen von vornherein ausgeschlossen sind)
#   heißt <uids>.
#
#   Die Ergebnisse sind in dem dict <results> nach key=uid.
#
#   Der Methodenaufruf <print_per_uid_ptty(name=True)> ist nicht notwendig und nur zur Veranschaulichung der erhaltenen Daten.
# ----------------------------------------------------------------------------------

import requests
import json
import geopandas

overpass_url = "http://overpass-api.de/api/interpreter"

search_radius = 500
max_search_radius = 2000

# user id's (or search id's)
uids = {3870914569}

results = {}  # dict<uid: query_result["elements"]>

print("Fetching Data...", end="\n" * 2)
for uid in uids:
    search_radius = 500  # resetting search_radius
    while search_radius < max_search_radius:
        overpass_query = """
        [out:json][timeout:500];
        nwr(id:{0})->.res;
        nwr[amenity=bar](around.res:{1});
        out center;
        """.format(
            uid, search_radius
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

        # dealing with empty result
        if result["elements"] == []:
            search_radius += 500  # expanding search radius
        else:
            break  # stops further querying

    results[uid] = (
        f"No results {search_radius}m near uid {uid} !"
        if result["elements"] == []
        else result["elements"]
    )

print(json.dumps(results, indent=2))

# geopandas visualisation
# gdf = geopandas.read_file(resuts.json())
