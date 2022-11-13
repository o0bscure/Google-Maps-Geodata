import json
import sqlite3

conn = sqlite3.connect("geodata.sqlite")
cur = conn.cursor()

#connect to the database file
cur.execute("SELECT * FROM Locations")
#open the js file
fhand = open("where.js","w")
fhand.write("myData = [\n") 
count = 0

#read through the database file
for row in cur :
    data = row[1]
    try: 
        js = json. loads(data)
    except:
        continue
    
    if not "status" in js and js["status"] == "OK":
        continue
    
    try:
        lat = js["results"][0]["geometry"]["location"]["lat"]
        lng = js["results"][0]["geometry"]["location"]["lng"]
        if lat == 0 or lng == 0 :
            continue
        where = js["results"][0]["formatted_address"]
        where = where.replace("'","")
    except Exception as error:
        #print(error)
        continue
    try:
        print(where,lat,lng)
        count = count + 1
        if count > 1 : fhand.write(",\n")
        output = f"[{lat},{lng},'{str(where)}']"
        fhand.write(output)
    except:
        continue
    
fhand.write("\n]"+";")
cur.close()
fhand.close()