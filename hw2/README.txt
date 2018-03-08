This is the README file for A0155937R, A0179836J submission.


== Python Version ==

We're using Python Version <3.6.2> for this assignment.

== General Notes about this assignment ==

Give an overview of your program, describe the important algorithms/steps 
in your program, and discuss your experiments in general.  A few paragraphs 
are usually sufficient.


########### SkipList ###########

We create skipPointer for the Posting List if the length of the posting list is more than 3.

########### SkipList ###########


########### DicValue ###########
DicValue class is the value of entries in the dictionary.
DicValue class with attribute frequency and pointer to posting list.
Pointer is a tuple with two integer value. It indicate the location of the
posting list stored in postings.txt file. The first value is the byte
offset of the corresponding posting list stored in the postings.txt file.
The second is the length of it. Note that it is the bytes encoded by pickle.
########### DicValue ###########

########### Search.py ###########
When there are two or more consecutive “AND”, it will optimise the merging by finding the shortest list and merge it with any list.Thus, it will save a lot of running time if the other lists are lengthy. We also implemented “AND NOT” as the Professor Jin that it would be more faster to calculate the resulting posting list.

When we need the posting list, we will load the disk into the memory and execute the query.
After we have use load it, we would set it to NONE. We followed the instruction strictly as we did not load all the posting list from the disk to the memory

########### Search.py ###########


########### Persistence to Disk ########### 

We used Pickle library to handle the loading and saving of posting list. We used pickle.load() to load the dictionary to memory. We also used pickle.dumps(posting list) to create a string representation of the posting list.

########### Persistence to Disk ########### 







== Files included with this submission ==

List the files in your submission here and provide a short 1 line
description of each file.  Make sure your submission's files are named
and formatted correctly.

########### File Included ###########

README.txt  - explain the code to the users

myHelper.py - contains the DicValue class with attribute frequency and pointer to posting list
	      and the Node Class for the ID, and a lot of helper functions like load a posting list from a txt file
 
search.py   - implement the Shunting-yard algorithm and the postfixEvaluation and our SPECIAL 		       algorithm to make the query faster 

Index.py     - Indexing

dictionary.txt - Dictionary

postings.txt  - Posting lists

########### File Included ###########






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






########### References ###########


-I was inspired by these links and I used his idea to implement the Dijkstra shunting yard algorithm for the query 

#https://en.wikipedia.org/wiki/Reverse_Polish_notation
#http://www.martinbroadhurst.com/shunting-yard-algorithm-in-python.html
#https://msoulier.wordpress.com/2009/08/01/dijkstras-shunting-yard-algorithm-in-python/

We realised that we have an error called maximum recursion depth exceeded as the pickle
Reached the maximum recession depth. Thus, we had to increase the limit.

We found out that we could increase the limit by using sys.setrecursionlimit()

https://stackoverflow.com/questions/3323001/what-is-the-maximum-recursion-depth-in-python-and-how-to-increase-it

########### References ###########


