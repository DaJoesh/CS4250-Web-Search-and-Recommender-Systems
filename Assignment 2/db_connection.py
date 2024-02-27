#-------------------------------------------------------------------------
# AUTHOR: Joshua Jenkins
# FILENAME: db_connection.py
# SPECIFICATION: Database operations using pyscopg2
# FOR: CS 4250 - Assignment #2
# TIME SPENT: 2 1/2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with
# standard arrays

#importing some Python libraries
# --> add your Python code here
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access the environment variables
db_name = os.getenv("DB_NAME")
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
conn_string = f"dbname={db_name} user={db_user} password={db_password}"

def connectDataBase():

    # Create a database connection object using psycopg2
    # --> add your Python code here
    conn = psycopg2.connect(conn_string)
    return conn

def createCategory(cur, catId, catName):

    # Insert a category in the database
    # --> add your Python code here
    cur.execute("INSERT INTO category (catId, catName) VALUES (%s, %s)", (catId, catName))

def createDocument(cur, docId, docText, docTitle, docDate, docCat):
    # 1 Get the category id based on the informed category name
    # --> add your Python code here
    cur.execute("SELECT catId FROM category WHERE catName = %s", (docCat,))
    catId = cur.fetchone()
    
    if catId:
        catId = catId[0]
    else:
        print("Category not found")
    # 2 Insert the document in the database. For num_chars, discard the spaces and punctuation marks.
    # --> add your Python code here
    cur.execute("INSERT INTO document (docId, docText, docTitle, docDate, docCat) VALUES (%s, %s, %s, %s, %s)", (docId, docText, docTitle, docDate, catId))
    # 3 Update the potential new terms.
    # 3.1 Find all terms that belong to the document. Use space " " as the delimiter character for terms and Remember to lowercase terms and remove punctuation marks.
    # 3.2 For each term identified, check if the term already exists in the database
    # 3.3 In case the term does not exist, insert it into the database
    # --> add your Python code here
    def process_term(term):
        if term[-1] in ['.', ',', '!', '?', ':', ';']:
            term = term[:-1]
        return term.lower()
    print(docText.split())
    terms = [process_term(term) for term in docText.split()]
    print(terms)
    for term in set(terms):
        cur.execute(
            "SELECT term FROM document_terms WHERE docId = %s AND term = %s",
            (docId, term)
        )
        existing_term = cur.fetchone()

        if not existing_term:
            cur.execute(
                "INSERT INTO document_terms (docId, term) VALUES (%s, %s)",
                (docId, term)
            )
    # 4 Update the index
    # 4.1 Find all terms that belong to the document
    # 4.2 Create a data structure the stores how many times (count) each term appears in the document
    # 4.3 Insert the term and its corresponding count into the database
    # --> add your Python code here
    term_counts = {}
    for term in terms:
        term_counts[term] = term_counts.get(term, 0) + 1

    for term, count in term_counts.items():
        cur.execute(
        "INSERT INTO inverted_index (term, docId, count) VALUES (%s, %s, %s)",
        (term, docId, count)
        )

def deleteDocument(cur, docId):

    # 1 Query the index based on the document to identify terms
    # 1.1 For each term identified, delete its occurrences in the index for that document
    # 1.2 Check if there are no more occurrences of the term in another document. If this happens, delete the term from the database.
    # --> add your Python code here
    cur.execute("DELETE FROM document_terms WHERE docid = %s", (docId,))
    cur.execute("SELECT term FROM inverted_index WHERE docId = %s", (docId,))
    terms_to_delete = cur.fetchall()
    for term in terms_to_delete:
        cur.execute("DELETE FROM inverted_index WHERE docId = %s AND term = %s", (docId, term))
        cur.execute("SELECT COUNT(*) FROM inverted_index WHERE term = %s", (term,))
        term_count = cur.fetchone()[0]
        if term_count == 0:
            cur.execute("DELETE FROM document_terms WHERE term = %s", (term,))    
    # 2 Delete the document from the database
    # --> add your Python code here
    cur.execute("DELETE FROM document WHERE docId = %s", (docId,))


def updateDocument(cur, docId, docText, docTitle, docDate, docCat):

    # 1 Delete the document
    # --> add your Python code here
    deleteDocument(cur, docId)
    # 2 Create the document with the same id
    # --> add your Python code here
    createDocument(cur, docId, docText, docTitle, docDate, docCat)

def getIndex(cur):

    # Query the database to return the documents where each term occurs with their corresponding count. Output example:
    # {'baseball':'Exercise:1','summer':'Exercise:1,California:1,Arizona:1','months':'Exercise:1,Discovery:3'}
    # ...
    # --> add your Python code here
    cur.execute("SELECT term, docTitle, count FROM inverted_index JOIN document ON inverted_index.docId = document.docId ORDER BY term, docTitle")
    rows = cur.fetchall()
    index = {}
    for term, docTitle, count in rows:
        if term in index:
            index[term] += f",{docTitle}:{count}"
        else:
            index[term] = f"{docTitle}:{count}"
    return index