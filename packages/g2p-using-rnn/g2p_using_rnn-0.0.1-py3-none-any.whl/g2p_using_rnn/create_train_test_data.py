"""
This script creates train and test sets from original lexicon data. Also checks if the train test
split indices (and words) of LDist data are the same as MS format data.
"""
import pandas as pd
from sklearn.model_selection import train_test_split


def check_if_split_is_same(data_og, data_replaced):
    is_index_same = data_og['index'].equals(data_replaced['index'])
    is_word_same = data_og['word'].equals(data_replaced['word'])
    is_target_same = data_og['target'].equals(data_replaced['target'])

    print(f'The two data index columns are equal or not: {is_index_same}')
    print(f'The two data word columns are equal or not: {is_word_same}')
    print(f'The two data target columns are equal or not: {is_target_same}')
    print('********')


if __name__ == '__main__':
    data = pd.read_csv('data/lexicon_ldist_representation.txt',  # new_testing_data_from_mstts_lexicon_cleaned_ax_ar.txt',
                       encoding='utf-8', header=None, names=['word', 'target'])
    data[data.columns] = data.apply(lambda x: x.str.strip("\')|(\'"))
    data['target'] = data['target'].apply(lambda x: x.strip(" '"))

    print(data.head())
    print(data.shape)
    are_words_duplicated = not data['word'].is_unique
    print(f'Does the word column contain duplicates: {are_words_duplicated}')

    train, test = train_test_split(data, test_size=0.01, random_state=42)

    train = train.reset_index()
    test = test.reset_index()

    print(train.shape)
    print(test.shape)

    train.to_csv('data/lexicon_ldist_representation_train.txt', sep=',', index=False)
    test.to_csv('data/lexicon_ldist_representation_test.txt', sep=',', index=False)

    # check if multi-character replaced phoneme data is similar to original data
    test_data_og = pd.read_csv('data/new_testing_data_from_mstts_lexicon_cleaned_ax_ar_test.txt',
                       encoding='utf-8', header=None, names=['index', 'word', 'target'])
    test_data_replaced = pd.read_csv('data/lexicon_ldist_representation_test.txt',
                       encoding='utf-8', header=None, names=['index', 'word', 'target'])

    train_data_og = pd.read_csv('data/new_testing_data_from_mstts_lexicon_cleaned_ax_ar_train.txt',
                       encoding='utf-8', header=None, names=['index', 'word', 'target'])
    train_data_replaced = pd.read_csv('data/lexicon_ldist_representation_train.txt',
                       encoding='utf-8', header=None, names=['index', 'word', 'target'])

    check_if_split_is_same(test_data_og, test_data_replaced)
    check_if_split_is_same(train_data_og, train_data_replaced)

