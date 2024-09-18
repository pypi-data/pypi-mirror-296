import argparse
import multiprocessing
import pickle

import joblib
import numpy as np
import re
import fasttext


from sklearn.metrics import confusion_matrix
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression



from sklearn_crfsuite import metrics
from itertools import chain
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# model = Model()


percent_of_data_to_use = 3

def main(parsed_args):
    # Load the input data
    examples = []
    input_words = []  # List to store input words

    for f_name in parsed_args.input:
        print('Loading {}'.format(f_name))
        with open(f_name) as f:
            data = f.readlines()
            # Calculate the number of examples to use based on the percentage
            num_examples_to_use = int(len(data) * (percent_of_data_to_use / 100))
            print ("Number of examples available in file: ", len(data))
            print ("Number of examples used to train model: ", num_examples_to_use)
            # Randomly select the subset of examples
            selected_data = np.random.choice(data, num_examples_to_use, replace=False)
            with multiprocessing.Pool() as p:
                data = p.map(process_example, selected_data)
                examples.extend(data)
                input_words.extend([example[0] for example in data])

    print('Done processing input examples')

    # Prepare the data
    x_dicts, y_tags = zip(*examples)
    # x_train, x_test, y_train, y_test = train_test_split(x_dicts, y_tags, test_size=0.2, random_state=42)

    x_dicts = list(x_dicts)
    y_tags = [ele.tolist() for ele in y_tags]
    y_tags = [[str(x) for x in ele] for ele in y_tags]

    x_train, x_test, y_train, y_test = train_test_split(x_dicts, y_tags, test_size=0.2, random_state=42)

    print("Length x train :", len(x_train))
    print("Length y train :", len(y_train))
    print("Length x test :", len(x_test))
    print("Length y test :", len(y_test))

    svm_classifier = SVC(C=1.0, kernel='rbf', gamma='scale')
    rf_classifier = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)
    gb_classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42, verbose=True)
    knn_classifier = KNeighborsClassifier(n_neighbors=5)
    dt_classifier = DecisionTreeClassifier(max_depth=None, random_state=42)
    nb_classifier = GaussianNB()
    mlp_classifier = MLPClassifier(hidden_layer_sizes=(100,), activation='relu', solver='adam', max_iter=1000)
    lr_classifier = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000)

    classifiers = {
        #'SVM': svm_classifier,
        #'Random_Forest': rf_classifier,
        'Gradient_Boosting': gb_classifier,
        #'k_Nearest_Neighbors': knn_classifier,
        #'Decision_Tree': dt_classifier,
        #'Naive_Bayes': nb_classifier,
        #'Neural_Network': mlp_classifier,
        #'Logistic_Regression': lr_classifier
    }






    def combine(arr):
        combined = []
        for item in arr:
            if isinstance(item, list):
                combined.extend(combine(item))
            else:
                combined.append(item)
        return combined



    print("Loading vector model for phonemes...")

    fasttext_model = fasttext.load_model("g2p/sylseg/vector_model_for_phonemes.bin")  # Model(vectorizer=v)

    print("Vectorizing x train...")
    x_train_encoded = vectorize_dicts(x_train, fasttext_model)

    print("Vectorizing x test...")
    x_test_encoded = vectorize_dicts(x_test, fasttext_model)

    x_train_enc_zero = x_train_encoded[0][0]








    first_nested_array = x_train_encoded[0]


    y_train_flat = flatten(y_train)
    y_test_flat = flatten(y_test)

#    print(y_train_flat)
#    print(y_train_flat.shape)

    for classifier_name, classifier in classifiers.items():

        print()
        print(f"Training {classifier_name} classifier:")
        trained_model = train(classifier, np.array(x_train_encoded), y_train_flat)

        print()
        print(f"Evaluating {classifier_name} classifier:")
        evaluate(trained_model, np.array(x_test_encoded), y_test_flat, input_words)

        print()
        print(f"Saving {classifier_name} model:")
        filename = parsed_args.model_dest+classifier_name+".pkl"
        #joblib.dump(trained_model, filename)
        with open(filename, 'wb') as f:
            pickle.dump(trained_model, f)


def vectorize_dicts(train_data, embedding_model):

    train_data_encoded_character_level = []
    for list_of_dicts in train_data:
        for dict_ in list_of_dicts:
            feature_vectors_of_a_character = []
            for value in dict_.values():
                # embedding_model.get_word_vector(value)
                feature_vectors_of_a_character.extend(embedding_model.get_word_vector(value)) # 16 features - 1 feat = 50 dim vector
            train_data_encoded_character_level.append(feature_vectors_of_a_character)
    return train_data_encoded_character_level


def ngram(start, end, chars):
    """
    Extracts the consecutive elements of a list from start to end.

    The element at index start is included in the list, while end is excluded. If end >= start, the indices are swapped.
    """
    start, end = (start, end) if end >= start else (end, start)
    start = 0 if start < 0 else start
    end = len(chars) if end > len(chars) else end
    return ' '.join(chars[start:end])


def extract_features(phones):
    """
    Extracts a feature dict from a list of phones.

    :param phones: a list of phones
    :return: a mapping from feature names to values
    """
    fs = []
    for idx in range(0, len(phones)):
        f = {
            'left-1-1': ngram(idx + 1, idx, phones),
            'left-1-2': ngram(idx + 1, idx - 1, phones),
            'left-2-2': ngram(idx, idx - 1, phones),
            'left-1-3': ngram(idx + 1, idx - 2, phones),
            'left-2-3': ngram(idx, idx - 2, phones),
            'left-3-3': ngram(idx - 1, idx - 2, phones),
            'right-1-1': ngram(idx + 1, idx + 2, phones),
            'right-1-2': ngram(idx + 1, idx + 3, phones),
            'right-2-2': ngram(idx + 2, idx + 3, phones),
            'right-1-3': ngram(idx + 1, idx + 4, phones),
            'right-2-3': ngram(idx + 2, idx + 4, phones),
            'right-3-3': ngram(idx + 3, idx + 4, phones),
            'lr-1-1': ngram(idx + 1, idx, phones) + ngram(idx + 1, idx + 2, phones),
            'lr-2-1': ngram(idx + 1, idx - 1, phones) + ngram(idx + 1, idx + 2, phones),
            'lr-1-2': ngram(idx + 1, idx, phones) + ngram(idx + 1, idx + 3, phones),
            'lr-2-2': ngram(idx + 1, idx - 1, phones) + ngram(idx + 1, idx + 3, phones),
        }
        fs.append(f)
    return fs


def process_example(example):
    example = re.sub('\ufeff', '', example)  # remove BOM
    example = example.strip()
    phones, label = label_example(example)
    feats = extract_features(phones)
    return feats, label


def label_example(ex):
    """
    Turns an example string into a list of phones along with a list of classification outcomes.

    :param ex: an example
    :return: a tuple of a list of phones and an array of tags
    """
    in_phones = re.split(' ', ex)
    out_phones = []
    tags = []
    for idx in range(0, len(in_phones)):
        if in_phones[idx] != '-':
            out_phones.append(in_phones[idx])
            tags.append(0)
        else:
            tags[-1] = 1

    return out_phones, np.array(tags)


def split_train_dev(x, y, dev_proportion, shuffle=True):
    """
    Splits x and y arrays to a train and dev set.

    :param x: an array of vectorized examples
    :param y: an array of training labels
    :param dev_proportion: proportion of examples to assign to the dev set
    :return: x_train, y_train, x_dev, y_dev
    """
    assert len(x) == len(y)

    if shuffle:
        shuffle_indices = np.random.permutation(np.arange(len(x)))
        x = x[shuffle_indices]
        y = y[shuffle_indices]

    dev_idx = int(dev_proportion * len(x))
    x_train = x[dev_idx:]
    y_train = y[dev_idx:]
    x_dev = x[:dev_idx]
    y_dev = y[:dev_idx]
    return x_train, y_train, x_dev, y_dev


def train(model_1, x_train, y_train):

    model_1.fit(x_train, y_train)

    return model_1


def flatten(labels):
    return list(chain.from_iterable(labels))


def evaluate(model_, x_test, y_test, input_words):
    #     """
    #     Evaluates a structured model.
    #
    #     :param model: a Model instance
    #     :param x_dev: an array of vectorized test examples
    #     :param y_dev: an array of labels
    #     :return: an accuracy score
    #     """

    # Predict labels
    y_pred = model_.predict(x_test)
    # print("Flat Accuracy:", metrics.flat_accuracy_score(y_test, y_pred))

    # Flatten y_pred and y_test
    y_test_flat = flatten(y_test)
    y_pred_flat = flatten(y_pred)

    # Calculate accuracy
    accuracy = accuracy_score(y_test_flat, y_pred_flat)
    accuracy_percentage = accuracy * 100  # Convert accuracy to percentage
    print("Accuracy Score: {:.2f}%".format(accuracy_percentage))

    # Generate confusion matrix
    cm = confusion_matrix(y_test_flat, y_pred_flat)
    print(cm)
    # ANSI color codes for text color
    GREEN = '\033[92m'
    RED = '\033[91m'
    END = '\033[0m'  # Reset to default color

    # Print statements with colorized output
    print(f"{GREEN}Syllable Boundary predicted and found in test data - TP:{END}", cm[1][1])
    print(f"{GREEN}Syllable Boundary not predicted and not found in test data - TN:{END}", cm[0][0])
    print(f"{RED}Syllable Boundary predicted but not found in test data - FP:{END}", cm[0][1])
    print(f"{RED}Syllable Boundary not predicted but found in test data - FN:{END}", cm[1][0])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a statistical model for phonetic syllable segmentation.')
    parser.add_argument('--input', action='append', required=True,
                        help='Name of an input file containing segmented X-SAMPA strings, one per line. '
                             'May be specified more than once.')
    parser.add_argument('--model-dest', default='model', type=str,
                        help='Path to save the trained model to.')
    parser.add_argument('--dev-proportion', default=0.1, type=float,
                        help='Proportion of examples to assign to the dev set (default: 0.1).')
    args = parser.parse_args()
    main(args)
