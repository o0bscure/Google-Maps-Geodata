import requests
import sqlite3
import json

api_key= False
if api_key is False:
    #chuck's API. a list of addresses which we can pull the Json files for each address
    serviceurl = "http://py4e-data.dr-chuck.net/geojson?"              
else :
    serviceurl = "https://maps.googleapis.com/maps/api/geocode/json?"

#caching the data in a database file
conn = sqlite3.connect("geodata.sqlite")   
cur = conn.cursor()

cur.execute('''CREATE TABLE IF NOT EXISTS Locations (address TEXT, geodata JSON) 
            ''')

payload = {"address":address,"key":api_key}
file = requests.get(url=serviceurl,params=payload)
print("retrieving",file.json())
print("Retrieved",file.url)