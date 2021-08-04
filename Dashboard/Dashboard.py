from numpy.matrixlib.defmatrix import matrix
import streamlit as st
import pandas as pd
import spacy
from spacy.matcher import Matcher
import func


myfile_text = st.text_area("Copy the policy text and paste here.")

if len(myfile_text) > 0:
    matrix = func.make_df(myfile_text)
    if matrix != None:
        st.table(matrix)
        st.write(matrix['BT Coeff'].mean())
    else:
        st.write("No vague terms found.Try again pls.")
