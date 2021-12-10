# Dependencies
from PIL import Image
import streamlit as st
import pandas as pd
import spacy
from spacy.matcher import Matcher
from dashboardContent import func
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from gensim.models.word2vec import Word2Vec
from dashboardContent import dep
from sklearn.preprocessing import MinMaxScaler
import fitz
import matplotlib.pyplot as plt

# Word2Vec Model
model = Word2Vec.load('w2v.model')

# Sidebar Navigation: 4 Pages

st.sidebar.title("Navigation")
nav = st.sidebar.selectbox(
    "", ["Overview", "Tool", "Policy Results", "Company Policies"])


# Navigation page1: includes Information-------------------------------------------------------------------------------------------
if nav == "Overview":

    st.title("***Overview***")

    st.markdown("""# **Ambiguity Scoring in Privacy Policies**""")
    st.subheader(
        "**Corpus:** 73 privacy policies taken from publicly available apps on the Google Play Store")

    st.subheader("Inspiration")
    st.markdown(dep.Inspiration)

    st.table(dep.tab.set_index('Category'))

    st.subheader("Methodology")
    st.markdown(dep.Methodology)

    st.subheader("The Scoring Model")
    st.markdown(dep.The_Scoring_Model)

    st.image(Image.open('dashboardContent/equation.png'), caption='Equation')


# Navigation page2: Analysis tool----------------------------------------------------------------------------------------------------------
if nav == "Tool":
    nlp = spacy.load("en_core_web_sm")
    st.title("***Tool***")
    st.subheader("Test our algorithm on your custom data.")

    st.info("Choose your desired type of input from the selectbox")
    matrix_text = ''
    # Allow user to choose type of input.
    type_input = st.selectbox('Select', ['Choose your desired type of input','PDF', 'Copy and paste text'])

    if type_input == 'PDF':
    # Uploading a pdf
        uploaded_pdf = st.file_uploader("Load pdf: ", type=['pdf'])
        pdf_text = ""
        if uploaded_pdf is not None:
            doc = fitz.open(stream=uploaded_pdf.read(), filetype="pdf")
            for page in doc:
                pdf_text += page.getText()
            doc.close()

        if len(pdf_text) > 0:
            matrix_text = pdf_text


    # Getting text input
    if type_input == 'Copy and paste text':
        myfile_text = st.text_area("Copy the policy text and paste here. ")


        length_ = len(nlp(myfile_text))
        st.write(length_)

        if len(myfile_text) > 0:
            matrix_text=myfile_text

    # Generating matrix
    matrix = func.make_df(matrix_text)


    if "may" in matrix:
        max_len = len(matrix)
        word_count = matrix[['depending', 'necessary', 'appropriate', 'inappropriate', 'as needed',
       'as applicable', 'otherwise reasonably', 'sometimes',
       'from time to time', 'generally', 'mostly', 'widely', 'general',
       'commonly', 'usually', 'normally', 'typically', 'largely', 'often',
       'primarily', 'among other things', 'may', 'might', 'can', 'could',
       'would', 'likely', 'possible', 'possibly', 'anyone', 'certain',
       'everyone', 'numerous', 'some', 'most', 'few', 'much', 'many',
       'various', 'including but not limited to']].sum(axis=0).sort_values(ascending=False)
        matrix.index += 1

        st.success(f"Text Analysis Successfull. **{max_len}** ambiguous terms found.")

        tool_res = st.selectbox('' ,['Top Ambiguous words', 'Show Matrix'])
        if tool_res == 'Top Ambiguous words':
            st.bar_chart(word_count.head(5))

            def countPlot():
                fig = plt.figure(figsize=(10, 4))
                sns.countplot('Category', data=matrix)
                st.pyplot(fig)
            countPlot()


        if tool_res == 'Show Matrix':

            entries = st.slider("", 1, max_len, 1)

            st.table(matrix[["Category", "Amb_Terms", "Amb_Phrase"]].head(entries))

    else:
        st.write("No vague terms found.Try again please.")


# Navigation page3: includes Information--------------------------------------------------------------------------------------------------
elif nav == "Policy Results":

    st.title("***Policy Results***")

    # First Graph
    analysis = pd.read_csv('dashboardContent/coef_prob_plot.csv')
    analysis.columns = ['category', 'bt_coef', 'Probability']

    # Second Plot
    fi = go.Figure()
    fi.add_trace(go.Scatter(
        x=analysis['category'],
        y=analysis['Probability'],
        name='Probability of Occurence',

        marker_color='indianred',


    ))
    fi.add_trace(go.Bar(
        x=analysis['category'],
        y=analysis['bt_coef'],
        name='Ambiguity Score',

        marker_color='lightsalmon'

    ))

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


# Navigation page4: Analysis of Policies---------------------------------------------------------------------------------------------
elif nav == "Company Policies":
    st.title("Company Policies")
    Policies = pd.read_csv("dashboardContent/Policies_Results.csv")
    # Creating buttons for important companies
    amazon, snapchat, flipkart, whatsapp, facebook, instagram = st.beta_columns(
        6)

    comp_name = 0
    company_ = 'Amazon'
    with amazon:
        if st.button("Amazon",):
            company_ = 'Amazon'
            comp_name = 8

    with snapchat:
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
    # Displaying data of the company selected

    if comp_name != 0:

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

    policies_display = pd.read_csv(
        "dashboardContent/Policies_Results_display.csv")
    policies_display = policies_display.drop(columns=['Unnamed: 0'])
    policies_display["ambiguity_percentage"] = (
        policies_display["Amb_Length"]/policies_display["Length"] * 100).round(2)
    st.write(policies_display)

    fig = px.histogram(policies_display, x='ambiguity score', nbins=13)
    st.plotly_chart(fig, use_container_width=True)

    fig_scatter = px.scatter(
        policies_display, size='ambiguity_percentage', x="ambiguity score", y="Length")
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
