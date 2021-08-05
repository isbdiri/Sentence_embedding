import streamlit as st
import pandas as pd
import spacy
from spacy.matcher import Matcher
import func
import seaborn as sns
from matplotlib.pyplot import figure


nav = st.sidebar.selectbox("Analysis of:-", [ "Overview","Scraped Policies","Your own text"])




if nav == "Your own text":


    # Scoring model text: pg 14
    myfile_text = st.text_area("Copy the policy text and paste here.")

    if len(myfile_text) > 0:
        matrix = func.make_df(myfile_text)
        if "may" in matrix:
            
            st.write(matrix["Category"])
            st.write("Average vagueness score = ", matrix['BT Coeff'].mean())
        else:
            st.write("No vague terms found.Try again please.")

elif nav == "Scraped Policies":
    
    pol_analysis = st.selectbox("Choose:-", ["Plots" , "Scoring"])
    
    if pol_analysis == "Plots":

        st.write("Ambiguity score for each of the category: ")
        analysis = pd.read_csv('../coef_prob_plot.csv')

        score = figure(figsize=(10, 6), dpi=80)
        ax = sns.barplot(x="Unnamed: 0", y="bt_coef", data=analysis)
        st.pyplot(score)

        st.write("\n\n\n\n\n")

        st.write("Probability of the words in each category: ")
        prob = figure(figsize=(10, 6), dpi=80)
        ax = sns.barplot(x="Unnamed: 0", y="Probablity", data=analysis)
        st.pyplot(prob)

    if pol_analysis == "Scoring":
    
        policies_data = pd.read_csv("../Policies.csv")
        Company = policies_data['File_name']
        rad_comp = st.multiselect("Select the Company.", Company)
        
        
        for i in range(0, len(Company)):
            for a in rad_comp:
                if a == Company[i]:
                    st.write(Company[i], ":  ", policies_data.loc[i, "vague_score"])
        
        
                    
                    


       
    
    
    

