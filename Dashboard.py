from PIL import Image
import streamlit as st
import pandas as pd
import spacy
from spacy.matcher import Matcher
import func
import seaborn as sns

import plotly.express as px
import plotly.graph_objects as go
from gensim.models.word2vec import Word2Vec

from dep import *

from sklearn.preprocessing import MinMaxScaler

model = Word2Vec.load('w2v.model')


# Backend Code:


nav = st.sidebar.selectbox(
    "Navigation:-", ["Overview", "Policy Results", "Tool", "Company Policies"])


# Navigation part 1: includes Information
if nav == "Overview":

    st.header("***Overview***")

    st.markdown("""# **Ambiguity Scoring in Privacy Policies**""")
    st.subheader(
        "**Corpus:** 73 privacy policies taken from publicly available apps on the Google Play Store")

    st.subheader("Inspiration")
    st.markdown(""" We have used the methodology from the paper [Ambiguity in Privacy Policies and the Impact of Regulation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2715164) to quantify the degree of ambiguity in the set of privacy policies gathered. The paradigm they present categorizes ambiguous terms into the **four categories: Condition, Generalization, Modality and Numeric Quanitifiers**. The same have been described with examples in the table below.
     """)

    st.table(tab.set_index('Category'))

    st.subheader("Methodology")
    st.markdown(Methodology)

    st.subheader("The Scoring Model")
    st.markdown(The_Scoring_Model)

    st.image(image1, caption='Equation')

if nav == "Tool":
    st.header("***Tool***")

    # Scoring model text: pg 14
    st.subheader(
        "This tool will Analyse your text and give an everage privacy score.")
    myfile_text = st.text_area("Copy the policy text and paste here. ")

    if len(myfile_text) > 0:
        matrix = func.make_df(myfile_text)
        if "may" in matrix:

            st.write(matrix["Category"])
            st.write("Average vagueness score = ", matrix['BT Coeff'].mean())
        else:
            st.write("No vague terms found.Try again please.")


elif nav == "Policy Results":

    st.title("***Policy Results***")

    # First Graph
    analysis = pd.read_csv('coef_prob_plot.csv')
    analysis.columns = ['category', 'bt_coef', 'Probability']

    # st.write(analysis)
    lab = {'category': 'Category', 'bt_coef': 'Ambiguity Score'}
    fig = px.bar(analysis, x='category', y='bt_coef', labels=lab,
                 color='bt_coef', )

    # Second Plot
    fi = go.Figure()
    fi.add_trace(go.Scatter(
        x=analysis['category'],
        y=analysis['bt_coef'],
        name='Ambiguity Score',

        marker_color='indianred',


    ))
    fi.add_trace(go.Bar(
        x=analysis['category'],
        y=analysis['Probability'],
        name='Probability of Occurrence',

        marker_color='lightsalmon'

    ))

    first, second = st.beta_columns(2)
    a = 0
    with first:
        if st.button("Ambiguity Scores vs Categories"):
            a = 1

    with second:
        if st.button("Probability of words in a category"):
            a = 2

    if(a == 1):
        st.plotly_chart(fig)
    elif(a == 2):
        st.plotly_chart(fi)

    st.header(
        "This tool will return the top ***n*** words associated with any word.")

    st.subheader(
        "Select the number of terms you would like to see using the slider.")

    top_terms = st.slider("number: ", 1, 30, 5)

    st.subheader("Type a word in the input box without")

    search_term = st.text_input("Word: ", value='information')

    if len(search_term) > 0:

        sim_terms = pd.DataFrame(
            model.wv.most_similar(search_term.lower(), topn=top_terms), columns=['Term', 'Similarity_Score'])

        y_range = [sim_terms['Similarity_Score'].min(
        )-0.005, sim_terms['Similarity_Score'].max()+0.005]
        fig = px.bar(sim_terms, x='Term', y='Similarity_Score',
                     color='Similarity_Score', range_y=y_range)
        st.plotly_chart(fig)
    if len(search_term) > 16:
        st.table(search_term['Term'])

elif nav == "Company Policies":


    amazon, ola, flipkart, whatsapp, facebook, instagram = st.beta_columns(
        6)

    comp_name = 8
    company_ = 'Amazon'
    with amazon:
        if st.button("Amazon",):
            company_ = 'Amazon'
            comp_name = 8

    with ola:
        if st.button("Snapchat    "):
            comp_name = 75
            company_ = 'Snapchat'

    with flipkart:
        if st.button("Flipkart "):
            comp_name = 26
            company_ = 'Flipkart'
    with whatsapp:
        if st.button("WhatsApp"):
            comp_name = 38
            company_ = 'Whatsapp Business'
    with facebook:
        if st.button("Facebook "):
            comp_name = 18
            company_ = 'Facebook'
    with instagram:
        if st.button("Instagram"):
            comp_name = 48
            company_ = 'Instagram'

    if comp_name != '':
        Policies = pd.read_csv("Policies_Results.csv")
        st.header(f"***{company_}***")
        a, b, c = st.beta_columns(3)

        with a:
            st.write("Ambiguity Score: ",
                     Policies.loc[comp_name, 'Scaled_100'])

            st.write("Corpus Mean: `63`")
        with b:
            st.write("Length: ",
                     Policies.loc[comp_name, 'Length'])

            st.write("Corpus Mean: `67`")
        with c:
            st.write("Ambiguous Phrases: ",
                     Policies.loc[comp_name, 'Amb_Length'])

            st.write("Corpus Mean: `36`")

    st.header("***Data Snapshot***")

    policies_display = pd.read_csv("Policies_Results_display.csv")
    policies_display = policies_display.drop(columns=['Unnamed: 0'])
    policies_display["ambiguity_percentage"] = (policies_display["Amb_Length"]/policies_display["Length"] * 100).round(2)
    st.write(policies_display)


    fig = px.histogram(policies_display, x='ambiguity score', nbins=13)
    st.plotly_chart(fig, use_container_width=True)

    fig_scatter = px.scatter(policies_display, size = 'ambiguity_percentage', x = "ambiguity score", y = "Length")
    st.plotly_chart(fig_scatter, use_container_width=True)

    st.subheader("Compare with the most ambiguous policy: Torrent Downloader")

    Company = Policies['File_name']
    rad_comp = st.multiselect("Select the Company.", Company)

    plot_c = []
    plot_s = []
    plot_c.append(Policies.loc[39, "File_name"])
    plot_s.append(Policies.loc[39, "Scaled_100"])

    for i in range(0, len(Company)):
        for a in rad_comp:
            if a == Company[i]:
                plot_c.append(Policies.loc[i, "File_name"])
                plot_s.append(Policies.loc[i, "Scaled_100"])

    plot_df = pd.DataFrame()
    plot_df['Company'] = plot_c
    plot_df['Ambiguity Score'] = plot_s

    fig = px.bar(plot_df, x='Company', y='Ambiguity Score')
    st.plotly_chart(fig)
