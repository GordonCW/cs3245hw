This is the README file for A0155937R, A0179836J submission.

Name        	Metric number       	Email
Lee Wei Qing    A0155937R       	e0032074@u.nus.edu
KO Chung Wa 	A0179836J       	e0270991@u.nus.edu



== Python Version ==

We're using Python Version <3.5.4> for this assignment.



== General Notes about this assignment ==

In the index stage, we recoded the dictionary as it was not efficient enough.
Dictionary's key is the term and the value is a list in which the first entry is the df_term and the second one is the posting list consisting of tuples. In the tuple, it contains two entries. For the first entry, it is the documentID and the second entry is the weighted term frequency without normalization.

To compute the weighted documented vector length for normalization, we created another dictionary and its key is the documentID and the value is the weighted vector length.

We save the posting list into "postings.txt" for each term in the first dictionary using pickle. We replace the list with a pointer, which can help us to retrieve the posting list in the searching stage. After that, we save the the first dictionary into the "dictionary.txt" and the second dictionary into "docLength.txt".

This concludes the indexing stage.

In the searching stage, we pickle the dictionary from the "dictionary.txt" file and the weighted documented vector length for normalization from the "docLength.txt". Next, we would read the given query and identify whether it is a boolean query or free text query. If it is boolean query, we will remove the operator. After that, we tokenizise the query and do query expansion for each token. Finally, we do some preprocessing on query like casefolding, punctuation removal and stemming. The preprocessing is the same for both kind of queries and execute the search using ranked retrieval, which is cosine similiarity implemented in HW3.

For the Query expansion, we expand each term by one by finding the synonyms of each term using NLTK WordNet. If the synonyms is a adverb, we do not add it into the query.

For the document and query, we implemented lnc.ltc.

We tried an new idea which is limiting the search space for each query. We observed that for any free text query have more than one words, the user generally do not want the retrieved documents containing only one key word. We have tried to record how many key words a document contains and simply ignore the documents containing only one key words. However, the result of testing on the competition framework is not satisfactory so we disabled it.

We also tried an new idea which is to capture more documents when the query is boolean query. We observed that when it comes to boolean query, the resulting set of documents will be very samll. We tried to use thesaurus-based query expansion to expand each word in the boolean query. For example, let w_1, w_2, ..., w_n be the (preprocessed) term in the boolean query. We find S_1, S_2, ..., S_n where each S_k is the set of synonyms for w_k union {w_k}. We then limit our scope for searching in the following way. Define D_k to be the set of documents containing words in S_k. We define our search scope to be D_1 intersects D_2 intersects ... intersects D_n. Finally, we perform the seach using cosine similarity. The advantage of this method is that although we performed cosine similarity in the final step, the result set will not be too big. This is because we force the result document set to contain at least one synonyms for each w_k. However, the result of testing on the competition framework is also not satisfactory so we disabled it.



== Files included with this submission ==

List the files in your submission here and provide a short 1 line description of each file.  Make sure your submission's files are named and formatted correctly.



README.txt           - explain the code to the users

myHelper.py          - contains helper functions like load a posting list from a txt file

search.py            - implement the lnc.ltc for the document and query respectively.

queryExpansion.py    - functions to expand the query

index.py             - indexing

dictionary.txt       - dictionary

postings.txt         - posting lists

docLength.txt        - file that store information about the document length



== Statement of individual work ==

Please initial one of the following statements.

[ ] I, A0032074R, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

[ ] I, A0179836J, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.



== References ==

Lecture Notes from Chapter 7, 8, 9
Dr Zhao Jin went through how to do query expansion and TA explained to us about average precision.