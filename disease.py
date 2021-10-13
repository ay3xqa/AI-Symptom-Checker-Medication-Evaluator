# import numpy as np
# import random
# import warnings
# warnings.filterwarnings('ignore')
# import pandas as pd
# df = pd.read_csv('medium_clean.csv')
# from sklearn import preprocessing
# # Create x, where x the 'scores' column's values as floats
# x = df[["usefulCount"]].values.astype(float)
#
# # Create a minimum and maximum processor object
# min_max_scaler = preprocessing.MinMaxScaler()
#
# # Create an object to transform the data to fit minmax processor
# x_scaled = min_max_scaler.fit_transform(x)
#
# # Run the normalizer on the dataframe
# df["normCount"] = x_scaled
# a=[]
# for index, row in df.iterrows():
#     comp = row["rating"]+(row["normCount"])
#     #print(comp)
#     a.append(comp)
# df["CompScore"] = a
# export_csv = df.to_csv(r'C:\Users\1440806\Documents\export_dataframe.csv')


import numpy as np
import random


import numpy as np
import random
import warnings
warnings.filterwarnings('ignore')
import pandas as pd

from rake_nltk import Rake
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer


def main(args):
    condition = args[0]
    df = pd.read_csv('export_dataframe.csv')
    df = df[df["condition"] == condition]
    df = df.reset_index(drop=True)
    df['Key_words'] = ""

    for index, row in df.iterrows():
        plot = row['review']
        r = Rake()
        r.extract_keywords_from_text(plot)
        key_words_dict_scores = r.get_word_degrees()
        row['Key_words'] = str(list(key_words_dict_scores.keys()))
        df.at[index, "Key_words"] = row['Key_words']

    newdf = df[["drugName", "Key_words"]]
    newdf = newdf.reset_index(drop=True)
    newdf = newdf.set_index("drugName")

    count = CountVectorizer()
    count_matrix = count.fit_transform(df['Key_words'])
    cosine_sim = cosine_similarity(count_matrix, count_matrix)

    indices = pd.Series(newdf.index)

    def recommendations(title, cosine_sim=cosine_sim):

        recommended_drug = []
        idx = indices[indices == title].index[0]
        recommended_drug.append(idx)
        score_series = pd.Series(cosine_sim[idx]).sort_values(ascending=False)
        top_5_indexes = list(score_series.iloc[1:5].index)
        for i in top_5_indexes:
            recommended_drug.append(list(df.index)[i])

        return recommended_drug

    idxlist = recommendations(df.iloc[df['CompScore'].argmax()]["drugName"])

    toRet = []
    for i in idxlist:
        d = dict()
        d["DrugName"] = df.iloc[i].drugName
        d["Review"] = df.iloc[i].review
        # numbers=df.iloc[i].rating+", "+df.iloc[i].usefulCount
        # d["stats"] = numbers
        toRet.append(d)
    return toRet

if __name__ == '__main__':
    import sys
    main(sys.argv[1:])