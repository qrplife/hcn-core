# hcn-core
The core data elements of the U.S. HCN station from the NOAA GHCN dataset.

This SQLite database contains the core elements of TMAX,TMIN,PRCP,SNOW and SNWD from the U.S. historical climate network stations in NOAA GHCN dataset.

To re-create this database, start by downloading the data from NOAA:
```
curl -O ftp://ftp.ncdc.noaa.gov/pub/data/ghcn/daily/ghcnd_hcn.tar.gz
tar xzvf ghcnd_hcn.tar.gz
```
merge the undividual station daily file into a single file for all the HCN stations:
```
cat *.dly > hcn-core.txt
```
generate the intermediate SQL file, use Python 3:
```
python parsedly.py > hcn-core.sql
```
create the SQLite database:
```sql
CREATE TABLE obs (ID TEXT, YEAR INTEGER, MONTH INTEGER, DAY INTEGER, ELEMENT TEXT, VALUE INTEGER, MFLAG TEXT, QFLAG TEXT, SFLAG TEXT);
```
load the data from the intermediate SQL file into the SQLite database (this will take several hours)
```
$ sqlite3 hcn-core.sqlite3
SQLite version 3.8.11.1 2015-07-29 20:00:57
Enter ".help" for usage hints.
sqlite> CREATE TABLE obs (ID TEXT, YEAR INTEGER, MONTH INTEGER, DAY INTEGER, ELEMENT TEXT, VALUE INTEGER, MFLAG TEXT, QFLAG TEXT, SFLAG TEXT);
sqlite> .read hcn-core.sql
```
