"""
Create the database for the specified user
(who must not be siteUserAdmin)

Use this for local installations, not for MLab
"""

import pymongo
from pymongo import MongoClient
import sys

import config
CONFIG = config.configuration()

MONGO_ADMIN_URL = "mongodb://{}:{}@{}:{}/admin".format(
    CONFIG.ADMIN_USER,
    CONFIG.ADMIN_PW,
    CONFIG.DB_HOST, 
    CONFIG.DB_PORT)

try: 
    dbclient = MongoClient(MONGO_ADMIN_URL)
    db = getattr(dbclient, CONFIG.DB)
    print("Got database {}".format(CONFIG.DB))
    print("Attempting to create user")
    db.add_user(CONFIG.DB_USER,
                password=CONFIG.DB_USER_PW)
    print("Created user {}".format(CONFIG.DB_USER))
except Exception as err:
    print("Failed")
    print(err)


