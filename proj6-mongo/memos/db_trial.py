"""
Just to test database functions,
outside of Flask.

We want to open our MongoDB database,
insert some memos, and read them back
"""

import pymongo
from pymongo import MongoClient
import arrow
import sys

import config
CONFIG = config.configuration()

MONGO_CLIENT_URL = "mongodb://{}:{}@{}:{}/{}".format(
    CONFIG.DB_USER,
    CONFIG.DB_USER_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT, 
    CONFIG.DB)

print("Using URL '{}'".format(MONGO_CLIENT_URL))

try: 
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, CONFIG.DB)
    print("Got database")
    collection = db.dated
    print("Using sample collection")
except Exception as err:
    print("Failed")
    print(err)
    sys.exit(1)


#
# Insertions:  I commented these out after the first
# run successfuly inserted them
# 

record = { "type": "dated_memo", 
           "date":  arrow.utcnow().naive,
           "text": "This is a sample memo"
          }

print("Inserting 1")
collection.insert(record)
print("Inserted")

record = { "type": "dated_memo", 
           "date":  arrow.utcnow().replace(days=+1).naive,
           "text": "Sample one day later"
          }

print("Inserting 2")
collection.insert(record)
print("Inserted")


#
# Read database --- May be useful to see what is in there,
# even after you have a working 'insert' operation in the flask app,
# but they aren't very readable.  If you have more than a couple records,
# you'll want a loop for printing them in a nicer format. 
#

print("Reading database")

records = [ ] 
for record in collection.find( { "type": "dated_memo" } ):
   records.append(
        { "type": record['type'],
          "date": arrow.get(record['date']).to('local').isoformat(),
           "text": record['text']
    })

print("Records: ")
print(records)
