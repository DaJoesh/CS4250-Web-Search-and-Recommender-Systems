#-------------------------------------------------------------------------
# AUTHOR: Joshua Jenkins
# FILENAME: indexing.py
# SPECIFICATION: This creates a tf-idf matrix from a collection of documents from collection.csv
# FOR: CS 4250- Assignment #1
# TIME SPENT: 2 hours
#-----------------------------------------------------------*/

#IMPORTANT NOTE: DO NOT USE ANY ADVANCED PYTHON LIBRARY TO COMPLETE THIS CODE SUCH AS numpy OR pandas. You have to work here only with standard arrays

#Importing some Python libraries
import csv
import math

documents = []

#Reading the data in a csv file
with open('Assignment1/collection.csv', 'r') as csvfile:
  reader = csv.reader(csvfile)
  for i, row in enumerate(reader):
         if i > 0:  # skipping the header
            documents.append (row[0])
            
#Conducting stopword removal. Hint: use a set to define your stopwords.
#--> add your Python code here
stopWords = {'She','her','and','I','their','They'}
stopword_removal1 = []
stopword_removal2 = []
stopword_removal3 = []
d_counter = 0
stopword_removal = []
for document in documents:
    words = [word for word in document.split() if word not in stopWords]
    stopword_removal.append(words)
print("stopword removal:",stopword_removal)
print ("d counter:",d_counter)

#Conducting stemming. Hint: use a dictionary to map word variations to their stem.
#--> add your Python code here
stemming = {"loves":"love","dogs":"dog","cats":"cat"}
stemming_removal = []
for doc in stopword_removal:
    stemmed_words = [stemming[word] if word in stemming else word for word in doc]
    stemming_removal.append(stemmed_words)
print("stemming removal:",stemming_removal)

#Identifying the index terms.
#--> add your Python code here
index_terms = ["love","cat","dog"]

#Building the document-term matrix by using the tf-idf weights.
#--> add your Python code here

#function to calculate term frequency
def calculate_term_frequency(doc, terms):
    return [doc.count(term) for term in terms]

#function to calculate inverse document frequency
def calculate_inverse_document_frequency(docs, terms):
    idf_list = []
    for term in terms:
        count = 0
        for doc in docs:
            if term in doc:
                count += 1
        idf_list.append(count)
    for i in range(len(idf_list)):
        idf_list[i] = round(math.log10(len(docs)/idf_list[i]),3)
    return idf_list

#calculate tf
term_frequency = []
for doc in stemming_removal:
    term_frequency.append(calculate_term_frequency(doc, index_terms))
print("Term Frequency:", term_frequency)

#calculate idf
idf = calculate_inverse_document_frequency(stemming_removal, index_terms)
print ("Inverse Document Frequency:", idf)

#calulate tf-idf
tf_idf_matrix = [["Document"] + index_terms]
for i, doc in enumerate(stemming_removal, start=1):
    row = [f"d{i}"] + [tf * idf for tf, idf in zip(calculate_term_frequency(doc, index_terms), idf)]
    tf_idf_matrix.append(row)

#Printing the document-term matrix.
#--> add your Python code here

for row in tf_idf_matrix:
    print(row)
