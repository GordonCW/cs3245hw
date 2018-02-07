This is the README file for A0179836J's submission

== Python Version ==

I'm using Python Version <3.6.2> for this assignment.

== General Notes about this assignment ==

This program builds the language model for the three languages and make a prediction of which language it is for each sentence in the test file. Define "4-gram" to be a sequence of 4 consecutive characters in the following.

To build the language model,
1) create a 4-character window and slides through all the text in the file to collect all "4-grams"
2) build a dictionary with keys being the "4-gram" and the corresponing value being a dictionary with keys being the three different language and the corresponding value being the number of times the "4-gram" appearing that language.
3) add one to all the languages for each "4-gram" in the dictionary (add one smoothing)
4) compute the pobability of each "4-gram" appeaing in each language by the formula below
P(<a,b,c,d> appearing in language L) = (Count(<a,b,c,d>) in the table with add one smoothing)/(total no. of "4-grams" in L + total no. of distinct "4-grams" among all language)

To predict the language,
1) create a 4-character window and slides through all the text in the file to collect all "4-grams" in the test file
2) compute for each sentence in the test file P(the sentence appearing in language L) = the product of all "4-grams" appearing in L (p.s. if there are "4-grams" not appearing in our language model, just ignore that "4-grams")
3) output the L with the largest P(the sentence appearing in language L).
4) if there are more than half of the "4-grams" in the sentence absent from our language model built previously, classify it to be "other" language. I make this condition because I observed that every sentence being "other" language has more than 70% of the "4-grams" absent from the language model while the those sentence being the three language has at most 40% of the "4-grams" absent from the language model. So, I just pick the threshold to be 50%.

One thing to note is that to avoid underflow of the product of probability, I used log probability instead.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line description of each file.  Make sure your submission's files are named and formatted correctly.

build_test_LM.py	the code for generating language model and make the prediction in a .txt file
README.txt		brief description of the homework

== Statement of individual work ==

Please initial one of the following statements.

[X] I, A0179836J, certify that I have followed the CS 3245 Information Retrieval class guidelines for homework assignments. In particular, I expressly vow that I have followed the Facebook rule in discussing with others in doing the assignment and did not take notes (digital or printed) from the discussions.  

[ ] I, A0000000X, did not follow the class rules regarding homework assignment, because of the following reason:

== References ==

LEE WEI QING: He is my classmate and I have discussed the homework with him in order to clarify the requirements stated in the homework.

stackoverflow: I have looked up many methods to do some taskes in Python. For example, how to read txt file with correct encoding.