#-------------------------------------------------------------------------
# AUTHOR: Joshua Jenkins
# FILENAME: db_connection_mongo_solution.py
# SPECIFICATION: maniupulates data in a mongo database.
# FOR: CS 4250 - Assignment #3
# TIME SPENT: 2 1/2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
from pymongo import MongoClient

#for getting rid of punctuation using regular expressions
import re

def connectDataBase():

    # Create a database connection object using pymongo
    client = MongoClient('mongodb://localhost:27017/')
    # Accessing the database named 'your_database_name'
    db = client['assignment3']
    return db

def createDocument(col, docId, docText, docTitle, docDate, docCat):
    docText_normalized = re.sub(r'[^\w\s]', '', docText)
    
    # create a dictionary indexed by term to count how many times each term appears in the document.
    # Use space " " as the delimiter character for terms and remember to lowercase them.
    term_counts = {}
    for term in docText_normalized.lower().split():
        term_counts[term] = term_counts.get(term, 0) + 1
        
    # create a list of objects to include full term objects. [{"term", count, num_char}]
    terms_list = [{"term": term, "count": count, "num_chars": len(term)} for term, count in term_counts.items()]
    
    # produce a final document as a dictionary including all the required document fields
    document = {
        "_id": docId,
        "text": docText,
        "title": docTitle,
        "date": docDate,
        "category": docCat,
        "terms": terms_list
    }

    # insert the document
    col.insert_one(document)
    
def deleteDocument(col, docId):

    # Delete the document from the database
    col.delete_one({"_id": docId})

def updateDocument(col, docId, docText, docTitle, docDate, docCat):

    # Delete the document
    deleteDocument(col, docId)

    # Create the document with the same id
    createDocument(col, docId, docText, docTitle, docDate, docCat)
    
def getIndex(col):
    # Query the database to return the documents where each term occurs with their corresponding count.
    # Output example: {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    index = {}
    cursor = col.find({}, {"_id": 1, "terms": 1, "title": 1})
    for doc in cursor:
        title = doc['title']
        for term_obj in doc['terms']:
            term = term_obj['term']
            count = term_obj['count']
            if term not in index:
                index[term] = {}
            if title in index[term]:
                index[term][title] += count
            else:
                index[term][title] = count
                
    formatted_index = {term: ', '.join([f'{title}:{count}' for title, count in sorted(doc_counts.items())]) for term, doc_counts in index.items()}
    sorted_index = {term: formatted_index[term] for term in sorted(formatted_index.keys())}
    return sorted_index