import argparse
import multiprocessing
import numpy as np
import random
import re

from g2p.primstress.stress_model import StressModel
from collections import defaultdict
from sklearn.metrics import confusion_matrix


stressmodel = StressModel()


def main(parsed_args):




    # Load the input data
    examples = []
    for f_name in parsed_args.input:
        print('Loading {}'.format(f_name))
        with open(f_name) as f:
            with multiprocessing.Pool() as p:
                examples.extend(p.map(process_example, f))

    random.shuffle(examples)

    # Prepare the data
    dev_index = int((1.0 - parsed_args.dev_proportion) * len(examples))
    wfv_train = examples[:dev_index]
    wfv_dev = examples[dev_index:]

    # Vectorize
    feats_train = [d for t in wfv_train for d in t[1]]
    feats_dev = [d for t in wfv_dev for d in t[1]]
    x_train = stressmodel.vectorizer.fit_transform(feats_train)
    y_train = np.asarray([l for t in wfv_train for l in t[2]])

    # Train
    train(stressmodel, x_train, y_train)

    # Evaluate
    if parsed_args.dev_proportion > 0:
        x_dev = stressmodel.vectorizer.transform(feats_dev)
        y_dev = np.asarray([l for t in wfv_dev for l in t[2]])
        score, cm, false_positives, false_negatives = evaluate(stressmodel, x_dev, y_dev, feats_dev)
        print('Test score: {}'.format(score))
        #print('False Positives:')
        #for fp in false_positives:
        #    print(fp)
        #print('False Negatives:')
        #for fn in false_negatives:
        #    print(fn)
        print("Confusion Matrix:")
        print(cm)


    stressmodel.save(parsed_args.model_dest)
    print('Model written to {}'.format(parsed_args.model_dest))


def process_example(example):
    example = re.sub('\ufeff', '', example)  # remove BOM
    example = example.strip()
    output_word = example.split(' - ')
    input_word = [remove_stress(syl) for syl in output_word]
    labels = [label_syllable(syl) for syl in output_word]
    feats = stressmodel.extract_features_for_stress(input_word)
    return input_word, feats, labels

# THE OLD VERSION FROM XSAMPA
# def label_syllable(syl):
#     if syl.startswith('" '):
#         return 1
#     else:
#         return 0

def label_syllable(syl):
    if '1' in syl:
        return 1  # Indicates a syllable with stress
    else:
        return 0  # Indicates a syllable without stress

# THE OLD VERSION FROM XSAMPA
# def remove_stress(syllable):
#     return ' '.join(p for p in syllable.split(' ') if p != '"')

def remove_stress(syllable):
    # Removes stress symbols from ms-tts data.
    return ' '.join(part for part in syllable.split(' ') if part != '1')

def vectorize_dicts(x_dicts, model):
    return model.vectorize_data_set(x_dicts)


def train(model, x_train, y_train):
    """
    Trains a structured model.

    :param model: the model to train
    :param x_train: an array of vectorized training examples
    :param y_train: an array of training labels
    :return: a Model instance
    """
    learner = model.learner
    learner.fit(x_train, y_train)
    return model


#def evaluate(model, x_dev, y_dev, examples):
    """
    Evaluates a structured model.

    :param model: a Model instance
    :param x_dev: an array of vectorized test examples
    :param y_dev: an array of labels
    :param examples: a list of input examples
    :return: an accuracy score
    """
    #preds = model.learner.predict(x_dev)
    #confusion_matrix = defaultdict(int)
    #false_positives = defaultdict(list)
    #false_negatives = defaultdict(list)

    #for i, (pred, true_label) in enumerate(zip(preds, y_dev)):
    #    if pred != true_label:
    #        if pred == 1:
    #            false_positives[examples[i][0]].append(i)
    #        else:
    #            false_negatives[examples[i][0]].append(i)
    #    confusion_matrix[(true_label, pred)] += 1

    #print("Confusion Matrix:")
    #for k, v in confusion_matrix.items():
    #    print(k, v)

    #print("False Positives:")
    #for word, indices in false_positives.items():
    #    print(word, indices)

    #print("False Negatives:")
    #for word, indices in false_negatives.items():
    #    print(word, indices)

    #accuracy = model.learner.score(x_dev, y_dev)
    #return accuracy


def evaluate(model, x_test, y_test, examples):
    # Predict labels using the trained model
    y_pred = model.learner.predict(x_test)

    # Compute accuracy
    accuracy = np.mean(y_test == y_pred)

    # Compute confusion matrix
    cm = confusion_matrix(y_test, y_pred)

    # Extract false positives and false negatives
    false_positives = []
    false_negatives = []
    for i in range(len(y_test)):
        if y_test[i] != y_pred[i]:
            if y_pred[i] == 1:
                false_positives.append(examples[i])
            else:
                false_negatives.append(examples[i])

    return accuracy, cm, false_positives, false_negatives



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Train a statistical model for primary stress detection.')
    parser.add_argument('--input', action='append', required=True,
                        help='Name of an input file containing segmented X-SAMPA strings, one per line. '
                             'May be specified more than once.')
    parser.add_argument('--model_dest', default='model', type=str,
                        help='Path to save the trained model to.')
    parser.add_argument('--dev-proportion', default=0.5, type=float,
                        help='Proportion of examples to assign to the dev set (default: 0.1).')
    args = parser.parse_args()
    main(args)
