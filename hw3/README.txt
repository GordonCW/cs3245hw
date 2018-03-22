This is the README file for A0155937R, A0179836J submission.

Name		Metric number		Email
Lee Wei Qing	A0155937R		e0032074@u.nus.edu
KO Chung Wa	A0179836J		e0270991@u.nus.edu


== Python Version ==

We're using Python Version <3.6.2> for this assignment.







== General Notes about this assignment ==

We reused most of the code from the Homework Assignment 2. We changed the Node class, so it included the docId and the term frequency. After we have calculate the docId and term frequency for each node, we calculate the log scaled term frequency for each term that appear in the document using the formula 1 + log(ft_t,d) and we stored the value as term frequency. We calculated and saved the weighted document vector length for every document, so that we could do normalisation at the seach.py.

For the query, it would return None if there is nothing for it to query.

For the document and query, we implemented lnc.ltc.

We implemented a list and it contained the  docId ,which is in ascending order, and the score. As a result, the docID ordering is preserved.

We put the docId and the score into the heap and it will return the 10 docId which has the highest score.








== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.



README.txt  	- explain the code to the users

myHelper.py 	- contains the DicValue class with attribute frequency and pointer to posting list
	      and the Node Class for the ID, and a lot of helper functions like load a posting list from a txt file
 
search.py   	- implement the LNC.LTC for the document and query respectively. We also implemented the heap to get the top 10 result, if the query is not empty.

index.py     	- indexing

dictionary.txt 	- dictionary

postings.txt  	- posting lists

docLength.txt	- file that store information about the document length








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

Lecture Notes from Chapter 7 and 8
Prof Zhao Jin went through how to do normalisation and use heap to output the top K documents.


