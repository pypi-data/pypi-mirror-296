import numpy as np
import os
import pickle

from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.feature_extraction import DictVectorizer


class StressModel:
    """Wraps a primary stress classification model."""

    def __init__(self, learner=None, vectorizer=None):
        self.learner = learner if learner else self.create_learner()
        self.vectorizer = vectorizer if vectorizer else DictVectorizer(sparse=True)

    def predict_stress(self, syllables):
        """
        Outputs a prediction for a list of (string) syllables.

        :param syllables: list of strings
        :return: list of int (1 or 0)
        """
        feats = [self.extract_features_for_stress(syllables)]
        xs = self.vectorizer.transform(feats)
        probs = self.learner.predict_proba(xs)
        preds = np.zeros(len(syllables))
        max_index = np.argmax(probs[:, 1])
        preds[max_index] = 1
        return preds

    def extract_features_for_stress(self, word):
        feat_dicts = []
        for i in range(len(word)):
            f = {
                'left-position': position_feature(i),
                'right-position': position_feature(len(word) - i - 1),
                'current-syllable': str_from_list(word, i),
                'left-syllable': str_from_list(word, i - 1),
                'left-syllable-2': str_from_list(word, i - 2),
                'right-syllable': str_from_list(word, i + 1),
                'right-syllable-2': str_from_list(word, i + 2),
                'current-phone-1': word[i].split(' ')[0],
                'current-phone--1': word[i].split(' ')[-1]
            }
            # print("Word: %s, type: %s" % (word, type(word)))
            for phone in word[i].split(' '):
                f['contains-phone-{}'.format(phone)] = 1
            feat_dicts.append(f)
        return feat_dicts

    def vectorize_example(self, example_dicts):
        return self.vectorizer.transform(example_dicts)

    def vectorize_data_set(self, x_dicts):
        # first fit the vectorizer
        self.vectorizer.fit_transform(d for ds in x_dicts for d in ds)
        # then transform all the dicts again to keep their per-example structure
        x = np.array([self.vectorizer.transform(ds) for ds in x_dicts])
        return x

    def save(self, path_name: str):
        os.makedirs(path_name, exist_ok=True)
        with open(path_name + '/learner.pkl', 'wb') as f:
            pickle.dump(self.learner, f)
        with open(path_name + '/vectorizer.pkl', 'wb') as f:
            pickle.dump(self.vectorizer, f)

    @staticmethod
    def load(path_name: str):
        with open(path_name + '/learner.pkl', 'rb') as f:
            learner = pickle.load(f)
        with open(path_name + '/vectorizer.pkl', 'rb') as f:
            vectorizer = pickle.load(f)
        return StressModel(learner, vectorizer)

    @staticmethod
    def create_learner():
        # doesn't ever finish
        #svm_classifier = SVC(C=1.0, kernel='rbf', gamma='scale', verbose=True)
        # ok # rf_classifier = RandomForestClassifier(n_estimators=10, max_depth=100, random_state=42, n_jobs=-1,
        #                                       max_features='sqrt', verbose=True)
        # ok # gb_classifier = GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3, random_state=42, verbose=True)
        # doesn't ever finish #knn_classifier = KNeighborsClassifier(n_neighbors=5)
        # ok # dt_classifier = DecisionTreeClassifier(max_depth=100, random_state=42)
        mlp_classifier = MLPClassifier(hidden_layer_sizes=(10,), activation='relu', solver='sgd', max_iter=10,
                                       early_stopping=False, verbose=True) # solver='adam' hidden_layer_sizes=(100,)
        # lr_classifier = LogisticRegression(penalty='l2', C=1.0, solver='lbfgs', max_iter=1000, verbose=True)
        # sgd_classifier = SGDClassifier(loss="modified_huber", penalty="l2", shuffle=True, max_iter=500, verbose=True)

        return mlp_classifier  # REMEMBER TO CHANGE THE SAVE PATH IN THE RUN CONFIGURATION TO MATCH THE CHOSEN MODEL


def str_from_list(l, i):
    if i >= 0 and i < len(l):
        return l[i]
    else:
        return '$$$'


def position_feature(i):
    if i < 4:
        return str(i)
    else:
        return '>=4'

