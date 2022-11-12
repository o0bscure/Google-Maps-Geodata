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

fhand = open("where.data")
count = 0

#loop through each address in the data file
for line in fhand:
    #failsafe in case you hit the rate limit.
    if count > 200 :
        print("Retrieved 200 locations, restart to retrieve more") 
        break
    
    address = line.strip()   
    #the geodata row is the json file, and the address is the address row and each line in file. so we try to pull the json file
    #for each selected address
    cur.execute('''SELECT geodata FROM Locations WHERE address=?
                ''',(address,))
    
    try:
        #check if current address exists in the database file
        check = cur.fetchone()[0]                       
        print("Found in database",address)
        #if the address is already in the database, go back up and repeat
        continue                                                
    except:
        pass
                                                         
    payload = {"address":address,"key":api_key}
    # if no Google API key provided, keep the value as False           
    if api_key is not False:
        payload["key"] = api_key                 

    file = requests.get(url=serviceurl,params=payload)
    print("retrieving",file)
    
    print("Retrieved",file.url)
    #keeps track of how many json files retirved (how many API requests made)
    count = count + 1                                                   
    
    try :
        js = file.json()
    except: 
        print(file.text) 
        continue
    if "status" not in js or (js["status"] != "OK" and js["status"] != "ZERO_RESULTS") : #checks the validity of the json file
        print("==== Failure To Retrieve ====")
        print(file.text)
        break
    #save the json file for each address as a string data
    data = json.dumps(js)

    cur.execute("INSERT INTO Locations (address, geodata) VALUES (?,?)" ,(address,data) )   
    conn.commit()

print("Run geodump.py to read the data from the database")