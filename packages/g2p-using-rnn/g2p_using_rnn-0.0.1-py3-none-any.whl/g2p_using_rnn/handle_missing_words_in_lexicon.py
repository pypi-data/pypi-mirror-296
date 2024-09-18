"""
This script detects the missing words in updated (with corrections) lexicon and adds the missing '
words from the original data (along with transcriptions), creates train and test sets for model
training. Also checks if the train test splits are the same w.r.t. indices and words as original splits.
"""
import pandas as pd
from create_train_test_data import check_if_split_is_same
from sklearn.model_selection import train_test_split

data = pd.read_csv('data/version_control_lexicon_update_10_LDist.txt',
                   encoding='utf-8', header=None, names=['word', 'target'])
data_2 = pd.read_csv('data/lexicon_ldist_representation.txt',
                   encoding='utf-8', header=None, names=['word', 'target'])

data[data.columns] = data.apply(lambda x: x.str.strip("\')|(\'"))
data['target'] = data['target'].apply(lambda x: x.strip(" '"))

data_2[data_2.columns] = data_2.apply(lambda x: x.str.strip("\')|(\'"))
data_2['target'] = data_2['target'].apply(lambda x: x.strip(" '"))

# find which words in updated lexicon are missing
merged_df = pd.merge(data_2, data, on=['word'], how='left', indicator=True, sort=False)
merged_df.target_y.fillna(merged_df.target_x, inplace=True)
data_2_rows_missing_in_data = merged_df[merged_df['_merge'] == 'left_only']
data_rows_missing_in_data_2 = merged_df[merged_df['_merge'] == 'right_only']


merged_df = merged_df.drop(['target_x', '_merge'], axis=1)
merged_df.rename(columns={'target_y': 'target'}, inplace=True)
print(merged_df.head())
print(merged_df.shape)
are_words_duplicated = not merged_df['word'].is_unique
print(f'Does the word column contain duplicates: {are_words_duplicated}')


train, test = train_test_split(merged_df, test_size=0.01, random_state=42)

train = train.reset_index()
test = test.reset_index()

print(train.shape)
print(test.shape)

train.to_csv('data/version_control_lexicon_update_10_LDist_train.txt',  #lexicon_ldist_representation_train.txt',
             sep=',', index=False)
test.to_csv('data/version_control_lexicon_update_10_LDist_test.txt',  #lexicon_ldist_representation_test.txt',
            sep=',', index=False)


# check if multi-character replaced phoneme data is similar to original data
test_data_og = pd.read_csv('data/new_testing_data_from_mstts_lexicon_cleaned_ax_ar_test.txt',
                   encoding='utf-8', header=None, names=['index', 'word', 'target'])
test_data_updated = pd.read_csv('data/version_control_lexicon_update_10_LDist_test.txt',
                   encoding='utf-8', header=None, names=['index', 'word', 'target'])

train_data_og = pd.read_csv('data/new_testing_data_from_mstts_lexicon_cleaned_ax_ar_train.txt',
                   encoding='utf-8', header=None, names=['index', 'word', 'target'])
train_data_updated = pd.read_csv('data/version_control_lexicon_update_10_LDist_train.txt',
                   encoding='utf-8', header=None, names=['index', 'word', 'target'])

check_if_split_is_same(test_data_og, test_data_updated)
check_if_split_is_same(train_data_og, train_data_updated)

