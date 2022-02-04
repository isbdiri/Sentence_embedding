# ***Ambiguity Scoring Tool***

The live dashboard can be found [here](https://ambiguityscoring.herokuapp.comh)

## Components:- 

### 1. Overview
This page gives a brief description about the classification of ambiguous terms in 4 categories. 


### 2. Ambiguity Scoring Tool

- The Ambiguity Scoring tool takes in a text document, passes it through an ***NLP pipelilne*** and provides an analysis of the text in terms of ambiguity. 
- Users may input a **pdf file** or ***copy and paste*** the text in a text box.
- The tool finds phrases that use ambiguous terms and displays 2 plots to the user.
- Furthermore, the user can see the list of ambiguous phrases by choosing the ***Show Matrix*** option in the drop down menu.

### 3. Policy Results

We passed 76 poicies through our pipeline to study the use of ambiguous words in Privacy Policies.
- This Policy Results are displayed in a plot that shows the numeric ambiguity score for each category along with their probability of occurence.
- The users can search for a particular word and see top ***n*** words associated with their searched word in the corpus.

### 4. Company Policies

- This section allows users to see the analysis of individual company policies. 
- It also allows users to compare the Privacy Policies of the 76 Companies in our corpus.



## Run on local machine

#### To run the application on your local machine
- install all dependencies mentioned in the [requirements](requirements.txt).

### Run the following command on terminal:-


    git clone https://github.com/isbdiri/Sentence_embedding.git
<br>

### change directory to the cloned repository

    cd Sentence_embedding
<br>

### Run the app

    streamlit run Dashboard.py
