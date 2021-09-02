import spacy
import pandas as pd
from spacy.matcher import Matcher
nlp = spacy.load('en_core_web_sm')

Condition = ['depending', 'necessary', 'appropriate',
             'inappropriate', 'as needed', 'as applicable',
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
                      'much', 'many', 'various',
                      'including but not limited to']

bt_coef = {
    "CN": 1.619,
    "C": 1.783,
    "CM": 1.864,
    "CMN": 2.125,
    "CG": 2.345,
    "CGN": 2.443,
    "MN": 2.569,
    "N": 2.710,
    "M": 2.865,
    "CGMN": 2.899,
    "CGM": 2.968,
    "GN": 3.281,
    "GMN": 3.506,
    "G": 3.550,
    "GM": 4.045
}


def len_str(x):
    return len(x)


keepWords = Condition + Generalization + Modality + Numeric_quantifier
# print(keepWords)

index_tracker = {}
for num, i in enumerate(keepWords):
    index_tracker[i] = num
_ = keepWords.sort(key=len_str, reverse=True)


matcher = Matcher(nlp.vocab)
for i in keepWords:
    rule = [{"LOWER": j} for j in i.split()]
    matcher.add(i, None, rule)


def generateVec(sentence):
    text = nlp(sentence)

    final = []
    category_vaguesness = {"C": 0, "G": 0, "M": 0, "N": 0}
    for i in range(len(keepWords)):
        final.append(0)

    buffer_start = -1
    for word, match_start, match_end in matcher(text):
        if buffer_start < match_start:
            # print(nlp.vocab.strings[word])
            final[index_tracker[nlp.vocab.strings[word]]] += 1
            if nlp.vocab.strings[word] in Condition:
                category_vaguesness["C"] = 1
            elif nlp.vocab.strings[word] in Modality:
                category_vaguesness["M"] = 1
            elif nlp.vocab.strings[word] in Numeric_quantifier:
                category_vaguesness["N"] = 1
            else:
                category_vaguesness["G"] = 1
        buffer_start = match_end - 1

    if buffer_start == -1:
        return None

    temp = "".join([i for i in category_vaguesness if category_vaguesness[i]])
    final.append(temp)
    final.append(bt_coef[temp])

    print(final)
    return final


def generateMatrix(text_string):
    final = []
    tok = nlp(text_string)
    for i in tok.sents:
        vector = generateVec(i.text)
        if vector != None:
            final.append(generateVec(i.text))
    return final


def make_df(intext):
    visualization = pd.DataFrame(generateMatrix(intext))
    if len(visualization) == 0:
        return "None"
    keepWords = Condition + Generalization + Modality + \
        Numeric_quantifier + ["Category", "BT Coeff"]
    visualization.columns = keepWords

    return visualization
