import argparse
import multiprocessing
import numpy as np
import re

import sklearn_crfsuite
from sklearn.metrics import confusion_matrix, precision_recall_fscore_support
from g2p.sylseg.syllable_model import SyllableModel
from sklearn_crfsuite import metrics
from itertools import chain
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


syllablemodel = SyllableModel()
percent_of_data_to_use = 100

def main(parsed_args):
    # Load the input data
    examples = []
    input_words = []  # List to store input words
    phones_list = []

    for f_name in parsed_args.input:
        print('Loading {}'.format(f_name))
        with open(f_name) as f:
            data = f.readlines()
            # Calculate the number of examples to use based on the percentage
            num_examples_to_use = int(len(data) * (percent_of_data_to_use / 100))
            # Randomly select the subset of examples
            selected_data = np.random.choice(data, num_examples_to_use, replace=False)

            #with multiprocessing.Pool() as p:
            #    processed_data = p.map(process_example, selected_data)
            #    examples.extend(processed_data)
            #    input_words.extend([example[0] for example in processed_data])

            with multiprocessing.Pool() as p:
                processed_data = p.map(process_example, selected_data)
                for feat, label, phones in processed_data:
                    examples.append((feat, label))
                    phones_list.append(phones)

        #with open(f_name) as f:
        #    with multiprocessing.Pool() as p:
        #        data = p.map(process_example, f)
        #        examples.extend(data)
        #        input_words.extend([example[0] for example in data])

    # Prepare the data
    x_dicts, y_tags = zip(*examples)
    x_dicts = list(x_dicts)
    y_tags = [ele.tolist() for ele in y_tags]
    y_tags = [[str(x) for x in ele] for ele in y_tags]


    x_train, x_test, y_train, y_test = train_test_split(x_dicts, y_tags, test_size=0.2, random_state=42)

    #split = int(0.8 * len(x_dicts))
    #x_train = x_dicts[:split]
    #y_train = y_tags[:split]
    #x_test = x_dicts[split:]
    #y_test = y_tags[split:]

#    phones_list_test = phones_list[split:] #TODO fix now with different split

    print("Number of words used for training: ", len(x_train))
    print("Number of words used for testing: ", len(x_test))
    # print("length phones_list_test:", len(phones_list_test))
    # print("First few elements of phones_list_test:", phones_list_test[:10])

    # Train
    syllable_model_init = sklearn_crfsuite.CRF(algorithm='lbfgs', c1=0.1, c2=0.1, max_iterations=100, all_possible_transitions=True, verbose=True)
    trained_syllable_model = train(syllable_model_init, x_train, y_train)

    # Evaluate
    evaluate(trained_syllable_model, x_test, y_test) #phones list removed until split is fixed

    # Save Model
 #   model.save(parsed_args.syllablemodel_dest)
 #   print('Model written to {}'.format(parsed_args.syllablemodel_dest))
    print("Saving Model..")
    filename = parsed_args.syllable_model_dest
    joblib.dump(trained_syllable_model, filename)
    # some time later...
    # load the model from disk
 #   loaded_model = joblib.load(filename)



def process_example(example):
    example = re.sub('\ufeff', '', example)  # remove BOM
    example = example.strip()
    phones, label = label_example(example)
    feats = syllablemodel.extract_features_for_syllables(phones)
    return feats, label, phones


def label_example(ex):
    """
    Turns an example string into a list of phones along with a list of classification outcomes.

    :param ex: an example
    :return: a tuple of a list of phones and an array of tags
    """
    in_phones = re.split(' ', ex)
    # in_phones.pop(0)
    # in_phones.pop(-1)
    out_phones = []
    tags = []
    for idx in range(0, len(in_phones)):
        if in_phones[idx] != '-':
            out_phones.append(in_phones[idx])
            tags.append(0)
        else:
            tags[-1] = 1

    return out_phones, np.array(tags)


def vectorize_dicts(x_dicts, model):
    return model.vectorize_data_set(x_dicts)


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


def train(syllablemodel_1, x_train, y_train):
    """
    Trains a structured model.

    :param syllablemodel_1: the model to train
    :param x_train: an array of vectorized training examples
    :param y_train: an array of training labels
    :return: a Model instance
    """

    syllablemodel_1.fit(x_train, y_train)

    #for x, y in zip(X_train, y_train):
    #    syllablemodel_1.append(x, y)
    #syllablemodel_1.train('seg_model/syllablemodel_1.crfsuite')
   # learner = syllablemodel_1.learner
   # learner.fit(x_train, y_train)
    return syllablemodel_1

def flatten(labels):
    return list(chain.from_iterable(labels))

def evaluate(syllablemodel, x_test, y_test):

    #     """
    #     Evaluates a structured model.
    #
    #     :param model: a Model instance
    #     :param x_dev: an array of vectorized test examples
    #     :param y_dev: an array of labels
    #     :return: an accuracy score
    #     """

    # Predict labels
    y_pred = syllablemodel.predict(x_test) #model_.predict
    #print("Flat Accuracy:", metrics.flat_accuracy_score(y_test, y_pred))

    # Flatten y_pred and y_test
    y_test_flat = flatten(y_test)
    y_pred_flat = flatten(y_pred)

    # Calculate accuracy
    accuracy = accuracy_score(y_test_flat, y_pred_flat)
    accuracy_percentage = accuracy * 100  # Convert accuracy to percentage
    print("Accuracy Score: {:.2f}%".format(accuracy_percentage))
    print("PR", precision_recall_fscore_support(y_test_flat, y_pred_flat))

    # Generate confusion matrix
    cm = confusion_matrix(y_test_flat, y_pred_flat)
    print(cm)
    # ANSI color codes for text color
    GREEN = '\033[92m'
    RED = '\033[91m'
    GRAY = '\033[90m'
    END = '\033[0m'  # Reset to default color

    print(f"{GREEN}Syllable Boundary predicted and found in test data - TP:{END}", cm[1][1])
    print(f"{GREEN}Syllable Boundary not predicted and not found in test data - TN:{END}", cm[0][0])
    print(f"{RED}Syllable Boundary predicted but not found in test data - FP:{END}", cm[0][1])
    print(f"{RED}Syllable Boundary not predicted but found in test data - FN:{END}", cm[1][0])

    # # Get indices of false positives and false negatives
    # fp_indices = [i for i, (pred, true) in enumerate(zip(y_pred_flat, y_test_flat)) if pred == '1' and true == '0']
    # fn_indices = [i for i, (pred, true) in enumerate(zip(y_pred_flat, y_test_flat)) if pred == '0' and true == '1']
    #
    # phones_flat = flatten(phones_list_test)
    #
    # fp_tuples = []
    # fn_tuples = []
    #
    # # Populate the list of tuples
    # for idx in fp_indices:
    #     fp_tuples.append((phones_flat[idx - 1], phones_flat[idx], phones_flat[idx + 1]))
    #
    # for idx in fn_indices:
    #     fn_tuples.append((phones_flat[idx - 1], phones_flat[idx], phones_flat[idx + 1]))
    #
    # print("length fp indices", len(fp_indices))
    # print("length fn indices", len(fn_indices))
    #
    # from collections import Counter
    #
    # # Count occurrences of false positives and false negatives tuples
    # fp_counts = Counter(fp_tuples)
    # fn_counts = Counter(fn_tuples)
    #
    # # Sort false positives and false negatives tuples based on their counts
    # sorted_fp_tuples = sorted(fp_counts.items(), key=lambda x: x[1], reverse=True)
    # sorted_fn_tuples = sorted(fn_counts.items(), key=lambda x: x[1], reverse=True)
    #
    # # Print top ten most common false positives and false negatives along with their counts
    # print("Top 10 Most Common False Positives:")
    # for fp_tuple, count in sorted_fp_tuples[:10]:
    #     print("Out Phone:", fp_tuple[0], RED + "-" + "\033[0m", fp_tuple[1], fp_tuple[2], "(", count, ")")
    #
    # print("\nTop 10 Most Common False Negatives:")
    # for fn_tuple, count in sorted_fn_tuples[:10]:
    #     print("Out Phone:", fn_tuple[0], GRAY + "-" + "\033[0m", fn_tuple[1], fn_tuple[2], "(", count, ")")



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a statistical model for phonetic syllable segmentation.')
    parser.add_argument('--input', action='append', required=True,
                        help='Name of an input file containing segmented ms-TTS strings, one per line. '
                             'May be specified more than once.')
    parser.add_argument('--syllable_model-dest', default='syllablemodel', type=str,
                        help='Path to save the trained model to.')
    parser.add_argument('--dev-proportion', default=0.1, type=float,
                        help='Proportion of examples to assign to the dev set (default: 0.1).')
    args = parser.parse_args()
    main(args)