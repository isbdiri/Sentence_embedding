from spacy.matcher import Matcher
import streamlit as st

import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')


# Ambiguity Terms
Condition = ['depending', 'necessary', 'appropriate',
             'inappropriate', 'as needed', 'as applicable', 'when applicable', 'if applicable',
             'where applicable', 'when needed', 'if needed', 'where needed' 'reasonable', 'reasonably'
             'otherwise reasonably', 'sometimes',
             'from time to time']
Generalization = ['generally', 'mostly', 'widely',
                  'general', 'commonly',
                  'usually', 'normally', 'typically',
                  'largely', 'often', 'primarily',
                  'among other things']
Modality = ['may', 'might', 'can', 'could', 'would',
            'likely', 'possible', 'possibly']
Numeric_quantifier = ['anyone', 'certain', 'everyone',
                      'numerous', 'some', 'most', 'few',
                      'much', 'many', 'various', 'include',
                      'limited to',
                      'including but not limited to']
keepWords = (Condition + Generalization + Modality + Numeric_quantifier)

ambiguousWords = (['depending', 'necessary', 'appropriate',
                   'inappropriate', 'as_needed', 'as_applicable', 'when_applicable', 'if_applicable',
                  'where_applicable', 'when_needed', 'if_needed', 'where_needed', 'reasonable', 'reasonably'
                   'otherwise_reasonably', 'sometimes',
                   'from_time_to_time']+['generally', 'mostly', 'widely',
                                         'general', 'commonly',
                                         'usually', 'normally', 'typically',
                                         'largely', 'often', 'primarily',
                                         'among other things']+['may', 'might', 'can', 'could', 'would',
                                                                'likely', 'possible', 'possibly']+['anyone', 'certain', 'everyone',
                                                                                                   'numerous', 'some', 'most', 'few',
                                                                                                   'much', 'many', 'various', 'include',
                                                                                                   'limited_to',
                                                                                                   'including_but_not_limited to'])

myfile_text = st.text_area("Copy the policy text and paste here.")


def len_str(x):
    return len(x)


def replace_word(orig_text, matcher):
    tok = nlp(orig_text)
    text = ''
    buffer_start = 0
    for word, match_start, match_end in matcher(tok):
        # If we've skipped over some tokens, let's add those in (with trailing whitespace if available)
        if match_start > buffer_start:
            text += tok[buffer_start: match_start].text + \
                tok[match_start - 1].whitespace_
        # Replace token, with trailing whitespace if available
        text += nlp.vocab.strings[word] + tok[match_start].whitespace_
        buffer_start = match_end
    if buffer_start < len(tok):
        text += tok[buffer_start:].text
    return text


def ReplaceKeepwords(orig_text):
    global keepWords
    temp = keepWords.sort(key=len_str, reverse=True)
    text = orig_text
    # matcher = Matcher(nlp.vocab)
    for i in keepWords:
        matcher = Matcher(nlp.vocab)
        replacement = "_".join(i.split())
        rule = [{"LOWER": j} for j in i.split()]
        matcher.add(replacement, None, rule)
        text = replace_word(text, matcher)
    return text


final_text = nlp(ReplaceKeepwords(myfile_text))


# getting all sentences containing ambiguity terms
phrase = []


def get_sentences(sentence, phrase):

    for token in sentence:
        count = 0
        for term in ambiguousWords:
            if token.text == term:
                count = 1
        if count == 1:
            phrase.append(sentence)


# Calling the function
for sent in final_text.sents:
    get_sentences(sent, phrase)

# creating a data frame
df = pd.DataFrame()
df['Phrase'] = phrase

for amb in ambiguousWords:
    c1 = []
    for i in phrase:
        count = 0
        for token in i:
            if token.text == amb:
                count = 1

        c1.append(count)
    df[amb] = c1
df.loc['Column_Total'] = df.sum(numeric_only=True, axis=0)
df["Combinations"] = df. sum(axis=1)
df.index = df['Phrase']

length_df = len(df.index)
input_phrase_number = st.slider('Select the Phrase index', 0, length_df, 0)

count = 0
b = 1000

# for token in df['Phrase'][input_phrase_number]:

#     if (token.pos_ == 'VERB'):
#         ambiguousVerb = token

#     for term in ambiguousWords:
#         if token.text == term:
#             st.markdown(ambiguousVerb)
#             st.markdown(term)
#             b = count

#     if (token.pos_ == 'NOUN' and ((count > b) and (count <= b+2))):
#         st.markdown(token)
#     count += 1

st.write(df['Phrase'][input_phrase_number])

st.bar_chart(df)['Column_Total']
