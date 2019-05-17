# My-Memos
My Memos uses a database to maintain data across multiple sessions and keep
a list of dated memos created by the user

## Description

A Flask app that displays all the dated memos it finds in a MongoDB database.
The user can add dated memos, from the either the index page or a separate page.
Memos are displayed in date order and the user can delete memos
 
## Functionality 
  * Users can create a memo with a date. A "memo" is just a text string, which might be a few words but could be longer. When the memo is created, it is stored in the database.
  * All memos in the database are listed, sorted by date. Additionally, dates are displayed in relative form using phrases like “today,” “next week,” and ”10 days from now.”
  * Delete selected memos.
  
## Author
* Jeremiah Clothier

