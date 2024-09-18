"""
This script creates train, test and validation sets of input lexicon annotated data and saves them
in TSV format - required for transformer training.
"""
import pandas as pd
from g2p.src.g2p_using_rnn import check_if_split_is_same
from sklearn.model_selection import train_test_split

# create train and validation sets to train a transformer sequence to sequence model
data = pd.read_csv('data/version_control_lexicon_update_10_LDist_train.txt', encoding='utf-8',
                   index_col=False)  # lexicon_ldist_representation_train
data = data.drop('index', axis=1)
print(data.head())
data['target'] = data['target'].str.replace(' ', '')

train_data, val_data = train_test_split(data, test_size=0.1, random_state=42)

train_data = train_data.reset_index()
val_data = val_data.reset_index()

train_data.to_csv('data/data_updated_ldist_format_no_space_train.tsv', sep='\t', index=False)
val_data.to_csv('data/data_updated_ldist_format_no_space_val.tsv', sep='\t', index=False)


# create test set in tsv format
test_data = pd.read_csv('data/version_control_lexicon_update_10_LDist_test.txt', encoding='utf-8',
                   index_col=False)  # lexicon_ldist_representation_test
# test_data = test_data.drop('index', axis=1)
print(test_data.head())
#
# test_data = test_data.reset_index()
test_data['target'] = test_data['target'].str.replace(' ', '')

test_data.to_csv('data/data_updated_ldist_format_no_space_test.tsv', sep='\t', index=False)

train_data_1 = pd.read_csv('data/data_ms_format_train.tsv', encoding='utf-8',
                   index_col=False, sep='\t')
val_data_1 = pd.read_csv('data/data_ms_format_val.tsv', encoding='utf-8',
                   index_col=False, sep='\t')
test_data_1 = pd.read_csv('data/data_ms_format_test.tsv', encoding='utf-8',
                   index_col=False, sep='\t')
check_if_split_is_same(train_data, train_data_1) # index and word columns should be equal, target column of MS and LDist
# data are different due to different format
check_if_split_is_same(val_data, val_data_1)
check_if_split_is_same(test_data, test_data_1)
