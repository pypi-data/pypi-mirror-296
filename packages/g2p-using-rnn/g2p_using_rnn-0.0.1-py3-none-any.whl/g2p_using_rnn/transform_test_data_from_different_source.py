"""
This script takes in word and phoneme transcription data in Excel sheet and converts it into txt file
that can be used further to generate predictions on
"""
import pandas as pd
from g2p_program import convert_to_formalism

data = pd.read_excel('data/Transcriptions.2.xlsx')  # , header=None, names=['word', 'target'] encoding='utf-8'
print(data.head())

data.drop(data.columns[data.columns.str.contains(
    'unnamed', case=False)], axis=1, inplace=True)
print(data.head())
data['target'] = data['Transcription Patrick McCrae'].apply(lambda x: convert_to_formalism(x, 'ldist'))

data = data.drop(columns=['Transcription Patrick McCrae'])
data = data.reset_index()
print(data.head())

data.to_csv('data/lexicon_ldist_representation_test_external_source.txt', sep=',', index=False)
