import pymongo
from pymongo import MongoClient
import arrow
import sys

def humanize_date(date):
    """
    @brief      Converts UTC ISO format string into readable format

    @param      date a UTC ISO formatted string

    @return     string, "today", "yesterday", "in 5 days", etc.
    """
    try:
        then = arrow.get(date).to('local')
        now = arrow.utcnow().to('local')
        if then.date() == now.date():
            human = "Today"
        else:
            human = then.humanize(now)
            if human == "in a day":
                human = "Tomorrow"
    except:
        human = date
    return human

def add_to_db(db, date, text):
    """
    @brief      Adds content to database.

    @param      db (collection) The MongoDB database
    @param      date (str)  Date formatted as YYYY-MM-DD
    @param      text (str)  String of text for a given Memo

    @return     none, updates the MongoDB. If improper formatted then ignore the request
                and don't add a Memo, otherwise add the content to the database
    """
    # If the text and date fields are filled in then we will process the request and add it to our Database
    if text != "" and date != None:
        current_time = arrow.now().format(" HH:mm:ss")
        date = arrow.get(date + current_time,"YYYY-MM-DD HH:mm:ss").to("local").isoformat()
        record = {
            "type": "dated_memo",
            "date": date,
            "text": text
            }
        db.insert(record)
    return None

def delete_from_db(db,request):
    """
    @brief      parses through a POST request deleting all check marked memos

    @param      db (collection)      The MongoDB database
    @param      request  The POST request from index.html as a result of the "delete selected"
                         button being clicked

    @return     none, updates the MongoDB. Deleting all memos which have been "checked off" on the index.html
                webpage
    """
    for i in range(1,db.count()+1):
        try:
            date = request.form["check{}".format(i)]
            date_found = db.find_one({"date":date})
            db.remove(date_found)
        # We are are looking at a count{i} input that was not checked off, therefore we ignore it
        except:
            pass
    return None

def list_memos(db):
    """
    @brief      returns all memos in the database, in a form that can be inserted directly into the "session" object

    @param      db (collection)    The MongoDB databse

    @return     records (list), a list of memos properly formatted for our flask session
    """
    records = [ ]
    # Loop through our DB in Ascending order (using dates) i.e. past memos -> future/upcomming memos
    for record in db.find( { "type": "dated_memo" } ).sort("date",pymongo.ASCENDING):
      # remove the useless id
      del record['_id']
      # if there is an empty memo in our record then we should remove it
      if record["text"] == "":
        db.remove(record)
        continue
      records.append(record)
    return records
