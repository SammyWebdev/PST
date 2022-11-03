uid = "<uid>"
sp = "->.res;"
search_radius = 500
include_shops = False

overpass_query = (
    f"[out:json][timeout:500];nwr(id:{uid}){sp}(nwr[amenity=bar](around.res:{search_radius});nwr[amenity=pub](around.res:{search_radius});nwr[amenity=biergarten](around.res:{search_radius});"
    + (")" if not include_shops else "")
    + (
        f"nwr[shop=alcohol](around.res:{search_radius});nwr[shop=beverages](around.res:{search_radius}););"
        if include_shops
        else ";"
    )
    + "out center;"
)

print(overpass_query)
