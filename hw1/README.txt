This is the README file for A0179836J's submission

== Python Version ==

I'm (We're) using Python Version <3.6.2> for this assignment.

== General Notes about this assignment ==

This program build the language model for each language in the following way. Find all four consecutive characters for all training sentences. Compute the probability of those "4-gram" appearing in the training text.

To find all "4-gram" in a sentence, we take 4 characters of the sentence at a time and slides the window one unit right until the window capture the last four characters.

Since for each "4-gram", it may appear in all three of the language. I use a dictionary to store the data of the language model. The keys are all the "4-gram" appearing in at least one language. The values are dictionary with keys being three language and those values being the number of times the "4-gram" appears in that language.

For the add one smoothing, I added one to the count of each "4-gram" in each language.

To compute the probability, I also count the total number of "4-gram" in each language of the training text.

For each language,
P(<a,b,c,d>) = (Count(<a,b,c,d>) + 1)/(total no. of "4-gram" in that language + total no. of distinct "4-gram" among all language)

After building the language model, any arbitrary 4 consecutive characters <a,b,c,d> either appears in our language model or not. If it appears, we can retrieve the probability of that "4-gram" appearing in that language.

Therefore, for the test part, for each sentence, we find all "4-gram" and find the probability of those "4-gram" (if any in our model). Multiply those in the same language to get a estimate probability of that sentence appearing in that language. Output the language with the higher probability for that particular test sentence. The output will be my prediction for the language.

To avoid the number being too small and underflow, I used log probability. Since log is an strictly increasing function, the ordering of probability is preserved and direct comparisons of log probability are ok.

For classifying 'other' language, I observed that for sentences being 'other' language, the probability of the "4-gram" not appearing in our language model is high (about 70%). In other words, there are about 70% of "4-gram" in that sentence not being in our model. So, I made a threshold that if the test sentence has more than half of the "4-gram" are not in our model, I will classify it as 'other'.

== Files included with this submission ==

List the files in your submission here and provide a short 1 line description of each file.  Make sure your submission's files are named and formatted correctly.

build_test_LM.py	the code for generating language model and make the prediction
eval.py			evaluate the accuracy of the prediction by the language model
input.correct.txt	test with correct label
input.test.txt		test sentences
input.train.txt		training sentences
README.txt		brief description of the homework

== Statement of individual work ==

Please initial one of the following statements.

[KO, Chung Wa] I, A0179836J, certify that I have followed the CS 3245 Information
Retrieval class guidelines for homework assignments.  In particular, I
expressly vow that I have followed the Facebook rule in discussing
with others in doing the assignment and did not take notes (digital or
printed) from the discussions.

== References ==

LEE WEI QING: He is my classmate and I have discussed the homework with him in order to clarify the requirement stated in the homework.

stackoverflow: I have looked up many method to do some taskes in Python. For example, how to read txt file with correct encoding.