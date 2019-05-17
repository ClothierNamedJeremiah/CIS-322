"""
Nose tests for update_db.py
"""

# Mongo database
import nose # Testing framework
import logging
import pymongo
from pymongo import MongoClient
import update_db
import arrow

MONGO_CLIENT_URL = "mongodb://memos:project6@ds040877.mlab.com:40877/memos_mongo"

logging.basicConfig(format='%(levelname)s:%(message)s',
                    level=logging.WARNING)
log = logging.getLogger(__name__)

try:
    dbclient = MongoClient(MONGO_CLIENT_URL)
    db = getattr(dbclient, "memos_mongo")
    collection = db.dated

except:
    print("Failure opening database.  Is Mongo running? Correct password?")
    sys.exit(1)

def test_add():
	update_db.add_to_db(collection,"2017-11-05","November 5th")
	assert(collection.find_one({"text":"November 5th"}))
	update_db.add_to_db(collection,"1999-10-27","Hello")
	assert(collection.find_one({"text":"Hello"}))

def test_list():
	# Delete the whole database
    for record in  collection.find( { "type": "dated_memo" } ).sort("date",pymongo.ASCENDING):
        collection.remove(record)
    assert(update_db.list_memos(collection) == [])
    update_db.add_to_db(collection,"2000-12-27","1st Addition")
    update_db.add_to_db(collection,"2017-06-05","2nd Addition")
    record = update_db.list_memos(collection)
    # Update timestamps for assert statement. We do not know the exact time (downto seconds) when the database will add the items above
    record[0]['date'] = "2000-12-27"
    record[1]['date'] = "2017-06-05"
    assert(record  == [ {'text': '1st Addition','date':'2000-12-27','type':'dated_memo'},
    					{'text': '2nd Addition','date':'2017-06-05','type':'dated_memo'}])

def test_humanize():
	today = arrow.utcnow().to('local')
	yesterday = today.shift(days=-1).isoformat()
	tommorrow = today.shift(days=+1).isoformat()
	last_week = today.shift(weeks=-1).isoformat()
	last_month = today.shift(weeks=-5).isoformat()
	assert(update_db.humanize_date(today.isoformat()) == "Today")
	assert(update_db.humanize_date(yesterday) == "a day ago")
	assert(update_db.humanize_date(tommorrow) == "Tomorrow")
	assert(update_db.humanize_date(last_week) == "7 days ago")
	assert(update_db.humanize_date(last_month) == "a month ago")