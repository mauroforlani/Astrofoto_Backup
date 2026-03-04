import urllib.request, json, os, time

os.makedirs("img", exist_ok=True)

def nasa_dl(obj_id, query):
    dest = f"img/{obj_id}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"  skip {obj_id}")
        return True
    try:
        q = urllib.request.quote(query)
        url = f"https://images-api.nasa.gov/search?q={q}&media_type=image&page_size=1"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        items = data.get("collection", {}).get("items", [])
        if not items:
            print(f"  x {obj_id} - no results: {query}")
            return False
        nasa_id = items[0]["data"][0]["nasa_id"]
        asset_url = f"https://images-api.nasa.gov/asset/{urllib.request.quote(nasa_id)}"
        req2 = urllib.request.Request(asset_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=15) as r2:
            assets = json.loads(r2.read())
        hrefs = [i["href"] for i in assets.get("collection", {}).get("items", [])
                 if i["href"].lower().endswith((".jpg", ".jpeg"))]
        if not hrefs:
            print(f"  x {obj_id} - no jpg assets")
            return False
        img_url = hrefs[0]
        for h in hrefs:
            if "medium" in h or "1024" in h or "orig" in h:
                img_url = h
                break
        req3 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req3, timeout=20) as r3:
            imgdata = r3.read()
        if len(imgdata) > 5000:
            with open(dest, "wb") as f:
                f.write(imgdata)
            print(f"  ok {obj_id} ({len(imgdata)//1024}KB)")
            return True
        print(f"  x {obj_id} - too small")
        return False
    except Exception as e:
        print(f"  x {obj_id}: {e}")
        return False

OBJECTS = {
    "m42": "Orion Nebula",
    "ic434": "Horsehead Nebula",
    "ngc1977": "Running Man Nebula",
    "m78": "M78 nebula",
    "m1": "Crab Nebula",
    "ngc2174": "Monkey Head Nebula",
    "ngc2244": "Rosette Nebula",
    "ngc1499": "California Nebula",
    "ic1805": "Heart Nebula",
    "ic1848": "Soul Nebula",
    "ngc2261": "Hubble Variable Nebula",
    "ngc2392": "Eskimo Nebula",
    "ngc7000": "North America Nebula",
    "ic5070": "Pelican Nebula",
    "ngc6992": "Veil Nebula",
    "ngc6960": "Witch Broom Nebula",
    "ic5146": "Cocoon Nebula",
    "ngc6888": "Crescent Nebula",
    "m57": "Ring Nebula",
    "m27": "Dumbbell Nebula",
    "ngc6543": "Cat Eye Nebula",
    "ngc7293": "Helix Nebula",
    "ngc6302": "Butterfly Nebula",
    "m8": "Lagoon Nebula",
    "m20": "Trifid Nebula",
    "m16": "Pillars of Creation",
    "m17": "Omega Nebula",
    "ngc7635": "Bubble Nebula",
    "ngc281": "Pacman Nebula",
    "ngc6334": "Cat Paw Nebula",
    "ngc6357": "War and Peace Nebula",
    "ic1396": "Elephant Trunk Nebula",
    "ngc7822": "NGC 7822",
    "ngc2070": "Tarantula Nebula",
    "ic2177": "Seagull Nebula",
    "ngc1893": "Tadpoles Nebula",
    "sh2155": "Cave Nebula",
    "ngc40": "Bow Tie Nebula NGC 40",
    "sh2240": "Spaghetti Nebula",
    "ngc896": "Fish Head Nebula",
    "ngc2068b": "Barnard Loop",
    "ngc2264": "Cone Nebula",
    "ngc2359": "Thor Helmet Nebula",
    "sh2101": "Tulip Nebula",
    "ngc1333": "NGC 1333",
    "ngc2023": "NGC 2023",
    "ngc6820": "NGC 6820",
    "sh2132": "Lion Nebula",
    "vdb1": "Elephant Trunk IC1396",
    "sh2157": "Lobster Claw Nebula",
    "m31": "Andromeda Galaxy",
    "m33": "Triangulum Galaxy",
    "ngc891": "NGC 891",
    "m74": "M74 galaxy",
    "m81": "Bode Galaxy",
    "m82": "Cigar Galaxy",
    "m51": "Whirlpool Galaxy",
    "m101": "Pinwheel Galaxy",
    "m63": "Sunflower Galaxy",
    "m64": "Black Eye Galaxy",
    "ngc4565": "Needle Galaxy",
    "ngc4631": "Whale Galaxy",
    "ngc4038": "Antennae Galaxies",
    "m65m66": "Leo Triplet",
    "ngc3628": "Hamburger Galaxy",
    "m84virgo": "Virgo Cluster",
    "m87": "M87 galaxy",
    "m102": "Spindle Galaxy",
    "m106": "NGC 4258",
    "ngc5128": "Centaurus A",
    "ngc6946": "Fireworks Galaxy",
    "ngc7331": "NGC 7331",
    "ic342": "IC 342",
    "ngc2903": "NGC 2903",
    "ngc4594": "Sombrero Galaxy",
    "ngc253": "Sculptor Galaxy",
    "ngc2403": "NGC 2403",
    "ngc247": "NGC 247",
    "ngc4725": "NGC 4725",
    "ngc2841": "NGC 2841",
    "ngc7479": "NGC 7479",
    "ngc7814": "Little Sombrero",
    "ngc3521": "NGC 3521",
    "ngc5055": "NGC 5055",
    "ngc4490": "Cocoon Galaxy",
    "ngc5139": "Omega Centauri",
    "ngc1232": "NGC 1232",
    "ngc300": "NGC 300",
    "ngc6744": "NGC 6744",
    "ngc2976": "NGC 2976",
    "ngc3077": "NGC 3077",
    "ngc4244": "NGC 4244",
    "ngc4559": "NGC 4559",
    "ngc4649": "NGC 4649",
    "ngc5907": "NGC 5907",
    "ngc4216": "NGC 4216",
    "ngc1316": "Fornax A",
    "ngc4762": "NGC 4762",
    "ngc772": "NGC 772",
    "m13": "Hercules Globular Cluster",
    "m92": "M92 globular",
    "m3": "M3 globular cluster",
    "m5": "M5 globular cluster",
    "m15": "M15 globular cluster",
    "m2": "M2 globular cluster",
    "m22": "M22 globular cluster",
    "m10": "M10 globular cluster",
    "m12": "M12 globular cluster",
    "m4": "M4 globular cluster",
    "m80": "M80 globular cluster",
    "ngc104": "47 Tucanae",
    "ngc6397": "NGC 6397",
    "m56": "M56 globular",
    "m107": "M107 globular",
    "m62": "M62 globular",
    "m79": "M79 globular",
    "ngc5024": "M53 globular",
    "ngc6752": "NGC 6752",
    "m45": "Pleiades",
    "ngc869": "Double Cluster",
    "ngc884b": "Perseus cluster",
    "ngc7789": "Caroline Rose Cluster",
    "ngc457": "ET Cluster",
    "m35": "M35 cluster",
    "m36": "M36 cluster",
    "m37": "M37 cluster",
    "m38": "M38 cluster",
    "m34": "M34 cluster",
    "m11": "Wild Duck Cluster",
    "m41": "M41 cluster",
    "m50": "M50 cluster",
    "m52": "M52 cluster",
    "m67": "M67 cluster",
    "m44": "Beehive Cluster",
    "m47": "M47 cluster",
    "m46": "M46 cluster",
    "m48": "M48 cluster",
    "m39": "M39 cluster",
    "m29": "M29 cluster",
    "m26": "M26 cluster",
    "ngc752": "NGC 752 cluster",
    "ngc2362": "NGC 2362 cluster",
    "ngc6231": "NGC 6231 cluster",
    "ngc6633": "NGC 6633 cluster",
    "luna": "Moon surface",
    "giove": "Jupiter",
    "saturno": "Saturn",
    "marte": "Mars",
    "venere": "Venus",
    "urano": "Uranus",
    "nettuno": "Neptune",
    "albireo": "Albireo",
    "mizar": "Mizar",
    "epsilonlyrae": "Epsilon Lyrae",
    "etacas": "Eta Cassiopeiae",
}

ok = fail = 0
for obj_id, query in OBJECTS.items():
    if nasa_dl(obj_id, query):
        ok += 1
    else:
        fail += 1
    time.sleep(0.3)

print(f"\nOK={ok}  FAIL={fail}")
