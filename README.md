# wca-db-auto-update
A Python script I wrote that downloads the World Cube Association (WCA) database export from https://www.worldcubeassociation.org/results/misc/WCA_export.sql.zip, unzips it, connects to my local MySQL database and runs WCA_export.sql, which updates my local database. The WCA database contains every solve ever done by a competitor at a WCA competition, which is useful for obtaining interesting statistics. This script removes the burden of maunally downloading, unzipping and updating your database as it is all automated. 

To use the script, you will need to install pymysql and requests. When running it, pass in your MySQL username, password and database as command-line arguments.
