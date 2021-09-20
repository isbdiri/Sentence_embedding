# dependencies
import pandas as pd
from PIL import Image


# This file contains all the texts and images to be loaded into the Dashboard.


#  Navigation : overview



Inspiration = "We have used the methodology from the paper [Ambiguity in Privacy Policies and the Impact of Regulation](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2715164) to quantify the degree of ambiguity in the set of privacy policies gathered. The paradigm they present categorizes ambiguous terms into the **four categories: Condition, Generalization, Modality and Numeric Quanitifiers**. The same have been described with examples in the table below."
table_ = {'Category': ['Condition', 'Generalization', 'Modality', 'Numeric Quantifier'],
          'Meaning': ['Action(s) to be performed are dependent on a variable or unclear trigger.', 'Action(s)/Information Types are vaguely abstracted with unclear conditions.', 'Vague likelihood of action(s) or ambiguous possibility of action or event.', 'Vague quantifier of action/information type.'],
          'Examples': ["""depending, necessary, appropriate,
inappropriate, as needed, as applicable,
otherwise reasonably, sometimes, from time
to time""", """generally, mostly, widely, general, commonly,
usually, normally, typically, largely, often,
primarily, among other things""", """may, might, can, could, would, likely, possible,
possibly""", """anyone, certain, everyone, numerous, some,
most, few, much, many, various, including but
not limited to """]}


tab = pd.DataFrame(table_)


Methodology = " The process involved scraping the privacy policies, categorizing the different terms into their respective categories, finding their probablities and finally giving them a vagueness score."

The_Scoring_Model = """Simply  counting  the  number  of  vague  terms  in  a  privacy  policy  will  not  provide  an
    adequate  measure  of  ambiguity. The score is based on a statistical measure
    that scales the overall vagueness of individual statements in each policy based on the
    Bradley-Terry model for paired comparisons. \n\nThe  coefficients  that  were  computed  by  this  method  serve  for  these  calculations  to
    rank  the  vagueness  of  every  phrase  in  each  policy  containing  a  vague  term  or
    combinations  of  vague  terms  associated  with  an  action-information  pairing  where
    one of  the four identified  data practices (action) is applied  to a type of information
    (information).    """
