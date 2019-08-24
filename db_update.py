import requests
import os
import zipfile
import pymysql
import sys
# from bs4 import BeautifulSoup
from shutil import rmtree

sql_username = sys.argv[1]
sql_password = sys.argv[2]
sql_db = sys.argv[3]

fileName = "WCA_export.sql"
downloadURL = "https://www.worldcubeassociation.org/results/misc/WCA_export.sql.zip"
downloadFolder = os.path.dirname(__file__) + "/db_files"
downloadPath = os.path.join(downloadFolder, fileName + ".zip")
sqlFile = downloadFolder + "/" + fileName + "/" + fileName

# DELETE AND RECREATE ./db_files
if os.path.exists(downloadFolder):
    rmtree(downloadFolder)
os.makedirs(downloadFolder)
print("New empty ./db_files folder created")

tries = 0
while tries < 3:
    # DOWNLOAD ZIP FILE
    try:
        with open(downloadPath, 'wb') as f:
            print("Downloading export")
            r = requests.get(downloadURL, stream=True)
            totalLength = r.headers.get('content-length')

            # PROGRESS BAR
            if totalLength is None: # no content length header
                f.write(r.content)

            else:
                dl = 0
                totalLength = int(totalLength)
                for data in r.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / totalLength)
                    sys.stdout.write("\r[%s%s] %d%%" % ('=' * done, ' ' * (50-done), done*2))
                    sys.stdout.flush()

        print("\nExport downloaded")
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        tries += 1
        continue

    # UNZIP
    try:
        z = zipfile.ZipFile(downloadPath)
        z.extractall(os.path.join(downloadFolder, fileName))
        print("Export unzipped successfully")
        break
    except:
        print("Unzipping failed")
    tries += 1

if tries >=3:
    sys.exit()

# UPDATE DB
db = pymysql.connect("localhost", sql_username, sql_password, sql_db)
print("Database connection established")
cursor = db.cursor()

sql = "USE " + sql_db

try:
   cursor.execute(sql)
   db.commit()
   print("Database change successful")
except:
   db.rollback()
   print("Database change failed")

# OPEN FILE AND SPLIT QUERIES
with open(sqlFile, "r") as file:
            # Split file in list
            ret = file.read().split(';')
            # drop last empty entry
            ret.pop()
            queries = ret

# EXECUTE QUERIES
isSuccess = True

for query in queries:
    tries = 0
    while tries < 3:
        try:
            cursor.execute(sql)
            db.commit()
            print("Query successful")
            break
        except:
            db.rollback()
            print("Query unsuccessful, trying again")
            tries += 1

    if tries == 3:
        print("Aborting database update")
        isSuccess = False;
        break

if isSuccess:
    print("Database update successful")
else:
    print("Database update failed")

db.close()
