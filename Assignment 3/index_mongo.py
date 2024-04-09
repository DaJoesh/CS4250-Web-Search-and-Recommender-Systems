#-------------------------------------------------------------------------
# AUTHOR: Joshua Jenkins
# FILENAME: index_mongo.py
# SPECIFICATION: contains the main menu for the application and connects to the database.
# FOR: CS 4250 - Assignment #3
# TIME SPENT: N/A
#-----------------------------------------------------------*/
from db_connection_mongo_solution import *

if __name__ == '__main__':

    # Connecting to the database
    db = connectDataBase()

    # Creating a collection
    documents = db.documents

    #print a menu
    print("")
    print("######### Menu ##############")
    print("#a - Create a document")
    print("#b - Update a document")
    print("#c - Delete a document.")
    print("#d - Output the inverted index.")
    print("#e - Quit")

    option = ""
    while option != "e":

          print("")
          option = input("Enter a menu choice: ")

          if (option == "a"):

              docId = input("Enter the ID of the document: ")
              docText = input("Enter the text of the document: ")
              docTitle = input("Enter the title of the document: ")
              docDate = input("Enter the date of the document: ")
              docCat = input("Enter the category of the document: ")

              createDocument(documents, docId, docText, docTitle, docDate, docCat)

          elif (option == "b"):

              docId = input("Enter the ID of the document: ")
              docText = input("Enter the text of the document: ")
              docTitle = input("Enter the title of the document: ")
              docDate = input("Enter the date of the document: ")
              docCat = input("Enter the category of the document: ")

              updateDocument(documents, docId, docText, docTitle, docDate, docCat)

          elif (option == "c"):

              docId = input("Enter the document id to be deleted: ")

              deleteDocument(documents, docId)

          elif (option == "d"):

              index = getIndex(documents)
              print(index)

          elif (option == "e"):

               print("Leaving the application ... ")

          else:

               print("Invalid Choice.")