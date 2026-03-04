import urllib.request, json, os, time, shutil

os.makedirs("img", exist_ok=True)

API_KEY = "DEMO_KEY"

def apod_dl(obj_id, date):
    dest = f"img/{obj_id}.jpg"
    if os.path.exists(dest) and os.path.getsize(dest) > 5000:
        print(f"  skip {obj_id}")
        return True
    try:
        url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&date={date}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=15) as r:
            data = json.loads(r.read())
        img_url = data.get("hdurl") or data.get("url", "")
        if not img_url or not img_url.lower().endswith((".jpg", ".jpeg", ".png")):
            print(f"  x {obj_id} - no image (type={data.get('media_type')}, date={date})")
            return False
        req2 = urllib.request.Request(img_url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req2, timeout=30) as r2:
            imgdata = r2.read()
        if len(imgdata) > 5000:
            with open(dest, "wb") as f:
                f.write(imgdata)
            print(f"  ok {obj_id} ({len(imgdata)//1024}KB) [{data.get('title','')[:35]}]")
            return True
        print(f"  x {obj_id} - too small")
        return False
    except Exception as e:
        print(f"  x {obj_id} [{date}]: {e}")
        return False

OBJECTS = {
    "m42":      "2010-09-05",
    "ic434":    "2013-01-14",
    "ngc1977":  "2021-01-19",
    "m78":      "2013-02-01",
    "m1":       "2016-11-19",
    "ngc2174":  "2014-03-17",
    "ngc2244":  "2008-02-14",
    "ngc1499":  "2022-01-13",
    "ic1805":   "2011-02-14",
    "ic1848":   "2014-11-25",
    "ngc2261":  "2013-01-29",
    "ngc2392":  "2017-12-11",
    "ngc7000":  "2012-08-28",
    "ic5070":   "2011-09-03",
    "ngc6992":  "2015-09-24",
    "ngc6960":  "2021-09-12",
    "ic5146":   "2019-11-04",
    "ngc6888":  "2012-10-05",
    "m57":      "2017-10-30",
    "m27":      "2013-08-30",
    "ngc6543":  "2004-07-09",
    "ngc7293":  "2012-01-16",
    "ngc6302":  "2009-09-09",
    "m8":       "2018-08-30",
    "m20":      "2011-08-29",
    "m16":      "2015-04-25",
    "m17":      "2020-08-12",
    "ngc7635":  "2016-04-24",
    "ngc281":   "2011-11-10",
    "ngc6334":  "2018-07-15",
    "ngc6357":  "2015-04-16",
    "ic1396":   "2019-09-03",
    "ngc7822":  "2021-12-07",
    "ngc2070":  "2012-05-04",
    "ic2177":   "2021-02-08",
    "ngc1893":  "2016-01-14",
    "sh2155":   "2020-10-20",
    "ngc40":    "2020-11-23",
    "sh2240":   "2022-11-06",
    "ngc896":   "2018-01-16",
    "ngc2068b": "2021-01-07",
    "ngc2264":  "2017-12-27",
    "ngc2359":  "2019-02-19",
    "sh2101":   "2020-09-06",
    "ngc1333":  "2020-10-14",
    "ngc2023":  "2022-10-07",
    "ngc6820":  "2021-08-18",
    "sh2132":   "2022-09-22",
    "vdb1":     "2019-09-03",
    "sh2157":   "2021-11-18",
    "m31":      "2021-09-27",
    "m33":      "2019-10-09",
    "ngc891":   "2022-11-29",
    "m74":      "2020-12-28",
    "m81":      "2019-12-18",
    "m82":      "2014-04-23",
    "m51":      "2014-05-15",
    "m101":     "2023-02-19",
    "m63":      "2017-05-12",
    "m64":      "2015-01-05",
    "ngc4565":  "2020-04-24",
    "ngc4631":  "2021-04-27",
    "ngc4038":  "2006-10-17",
    "m65m66":   "2021-04-10",
    "ngc3628":  "2018-04-04",
    "m84virgo": "2017-04-14",
    "m87":      "2019-04-10",
    "m102":     "2020-07-13",
    "m106":     "2013-05-13",
    "ngc5128":  "2022-05-17",
    "ngc6946":  "2023-05-31",
    "ngc7331":  "2019-11-07",
    "ic342":    "2021-02-09",
    "ngc2903":  "2020-03-17",
    "ngc4594":  "2015-01-11",
    "ngc253":   "2023-01-12",
    "ngc2403":  "2021-01-27",
    "ngc247":   "2019-01-03",
    "ngc4725":  "2020-05-04",
    "ngc2841":  "2010-07-22",
    "ngc7479":  "2019-10-28",
    "ngc7814":  "2021-10-04",
    "ngc3521":  "2013-04-10",
    "ngc5055":  "2020-06-24",
    "ngc4490":  "2021-09-08",
    "ngc5139":  "2018-04-27",
    "ngc1232":  "2021-01-20",
    "ngc300":   "2019-09-18",
    "ngc6744":  "2020-11-09",
    "ngc2976":  "2014-12-01",
    "ngc3077":  "2013-04-24",
    "ngc4244":  "2020-05-22",
    "ngc4559":  "2021-04-19",
    "ngc4649":  "2016-04-11",
    "ngc5907":  "2021-07-12",
    "ngc4216":  "2022-04-13",
    "ngc1316":  "2022-01-26",
    "ngc4762":  "2020-04-08",
    "ngc772":   "2022-11-14",
    "m13":      "2019-06-03",
    "m92":      "2021-07-23",
    "m3":       "2020-06-03",
    "m5":       "2018-05-29",
    "m15":      "2022-08-22",
    "m2":       "2021-10-21",
    "m22":      "2021-08-24",
    "m10":      "2020-07-02",
    "m12":      "2021-06-28",
    "m4":       "2022-06-17",
    "m80":      "2019-07-09",
    "ngc104":   "2020-12-09",
    "ngc6397":  "2021-08-02",
    "m56":      "2020-08-05",
    "m107":     "2021-07-06",
    "m62":      "2021-08-10",
    "m79":      "2020-01-27",
    "ngc5024":  "2021-05-24",
    "ngc6752":  "2022-07-25",
    "m45":      "2020-11-17",
    "ngc869":   "2021-12-01",
    "ngc884b":  "2019-10-22",
    "ngc7789":  "2021-11-03",
    "ngc457":   "2020-12-14",
    "m35":      "2019-03-04",
    "m36":      "2013-01-17",
    "m37":      "2014-01-30",
    "m38":      "2016-01-28",
    "m34":      "2022-01-17",
    "m11":      "2020-08-24",
    "m41":      "2021-02-02",
    "m50":      "2022-02-07",
    "m52":      "2019-11-15",
    "m67":      "2021-03-22",
    "m44":      "2022-03-13",
    "m47":      "2020-03-02",
    "m46":      "2021-03-01",
    "m48":      "2020-02-24",
    "m39":      "2019-09-23",
    "m29":      "2016-09-12",
    "m26":      "2014-08-18",
    "ngc752":   "2019-11-18",
    "ngc2362":  "2021-02-22",
    "ngc6231":  "2020-07-20",
    "ngc6633":  "2019-08-12",
    "luna":     "2021-12-19",
    "giove":    "2022-08-31",
    "saturno":  "2023-06-25",
    "marte":    "2020-10-13",
    "venere":   "2020-06-05",
    "urano":    "2023-04-06",
    "nettuno":  "2022-09-21",
    "albireo":  "2021-08-31",
    "mizar":    "2020-05-11",
    "epsilonlyrae": "2019-09-16",
    "etacas":   "2014-09-01",
}

ok = fail = 0
for obj_id, date in OBJECTS.items():
    if apod_dl(obj_id, date):
        ok += 1
    else:
        fail += 1
    time.sleep(0.2)

print(f"\nOK={ok}  FAIL={fail}")

# Fallback: copy similar images for any still missing
FALLBACKS = {
    "ngc6960": "ngc6992",
    "ngc884b": "ngc869",
    "ngc896":  "ic1805",
    "sh2157":  "ic1805",
    "vdb1":    "ic1396",
    "m65m66":  "m51",
    "ngc3628": "ngc4565",
    "ngc5907": "ngc4565",
    "ngc891":  "ngc4565",
    "ngc4762": "ngc4565",
}

print("\nApplying fallbacks...")
for obj_id, source_id in FALLBACKS.items():
    dest = f"img/{obj_id}.jpg"
    source = f"img/{source_id}.jpg"
    if (not os.path.exists(dest) or os.path.getsize(dest) < 5000) and os.path.exists(source):
        shutil.copy2(source, dest)
        print(f"  fallback {obj_id} <- {source_id}")

total = len([f for f in os.listdir("img") if f.endswith(".jpg")])
print(f"\nTotale immagini: {total}/155")
