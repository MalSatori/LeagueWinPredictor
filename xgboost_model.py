import numpy as np
import pandas as pd
import itertools
import xgboost as xgb
from IPython.display import display
import csv
import pickle
import matplotlib.pyplot as plt
from xgboost import plot_tree
import os
os.environ["PATH"] += os.pathsep + 'Z:/Program Files (x86)/Graphviz2.38/bin/'


path = 'Z:/Homebrew Programs/Python/leagueSummonerIDs/data/training_data.txt'
fi = 'Z:/Homebrew Programs/Python/leagueSummonerIDs/data/training_edit.txt'

'''with open(fi, 'r') as f, open(path, 'w') as out:
    r = csv.writer(out)
    try:
        for row in csv.reader(f):
            if row[7] != '':
                r.writerow(row)
    except IndexError:
        pass'''
dif



data = pd.read_csv(path)

display(data.head())
n_matches = data.shape[0]
n_features = data.shape[1] - 1
n_bluewins = len(data[data.SIDE == 'Blue'])
win_rate = (float(n_bluewins) / (n_matches)) * 100

print('Total number of matches: {}'.format(n_matches))
print('Total number of features: ' + str(n_features))
print('Win rate of blue side: {:.2f}%'.format(win_rate))

X_all = data.drop(['SIDE'], 1)
y_all = data['SIDE']

from sklearn.preprocessing import scale


cols = [['ONE', 'TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 'NINE', 'TEN']]
for col in cols:
    X_all[col] = scale(X_all[col])

X_all.HM1 = X_all.ONE.astype('str')
X_all.HM2 = X_all.TWO.astype('str')
X_all.HM3 = X_all.THREE.astype('str')
X_all.AM1 = X_all.FOUR.astype('str')
X_all.AM2 = X_all.FIVE.astype('str')
X_all.AM3 = X_all.SIX.astype('str')

def preprocess_features(X):
    ''' Preprocesses the football data and converts catagorical variables into dummy variables. '''

    # Initialize new output DataFrame
    output = pd.DataFrame(index=X.index)

    # Investigate each feature column for the data
    for col, col_data in X.iteritems():

        # If data type is categorical, convert to dummy variables
        if col_data.dtype == object:
            col_data = pd.get_dummies(col_data, prefix=col)

        # Collect the revised columns
        output = output.join(col_data)

    return output

X_all = preprocess_features(X_all)

print("Processed feature columns ({} total features):\n{}".format(len(X_all.columns), list(X_all.columns)))

print("\nFeature values:")
display(X_all.head())

from sklearn.model_selection import train_test_split

# Shuffle and split the dataset into training and testing set.
X_train, X_test, y_train, y_test = train_test_split(X_all, y_all,
                                                    test_size = 50,
                                                    random_state = 2,
                                                    stratify = y_all)


# for measuring training time
from time import time
# F1 score (also F-score or F-measure) is a measure of a test's accuracy.
# It considers both the precision p and the recall r of the test to compute
# the score: p is the number of correct positive results divided by the number of
# all positive results, and r is the number of correct positive results divided by
# the number of positive results that should have been returned. The F1 score can be
# interpreted as a weighted average of the precision and recall, where an F1 score
# reaches its best value at 1 and worst at 0.
from sklearn.metrics import f1_score


def train_classifier(clf, X_train, y_train):
    ''' Fits a classifier to the training data. '''

    # Start the clock, train the classifier, then stop the clock
    start = time()
    clf.fit(X_train, y_train)
    end = time()

    # Print the results
    print("Trained model in {:.4f} seconds".format(end - start))


def predict_labels(clf, features, target):
    ''' Makes predictions using a fit classifier based on F1 score. '''

    # Start the clock, make predictions, then stop the clock
    start = time()
    y_pred = clf.predict(features)

    end = time()
    # Print and return results
    print("Made predictions in {:.4f} seconds.".format(end - start))

    return f1_score(target, y_pred, pos_label='Blue'), sum(target == y_pred) / float(len(y_pred))


def train_predict(clf, X_train, y_train, X_test, y_test):
    ''' Train and predict using a classifer based on F1 score. '''

    # Indicate the classifier and the training set size
    print("Training a {} using a training set size of {}. . .".format(clf.__class__.__name__, len(X_train)))

    # Train the classifier
    train_classifier(clf, X_train, y_train)

    # Print the results of prediction for both training and testing
    f1, acc = predict_labels(clf, X_train, y_train)
    print(f1, acc)
    print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc))

    f1, acc = predict_labels(clf, X_test, y_test)
    print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))


#Boosting refers to this general problem of producing a very accurate prediction rule
#by combining rough and moderately inaccurate rules-of-thumb
clf_C = xgb.XGBClassifier(seed=82)

train_predict(clf_C, X_train, y_train, X_test, y_test)
print('')



# TODO: Import 'GridSearchCV' and 'make_scorer'
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import make_scorer

# TODO: Create the parameters list you wish to tune
parameters = {'learning_rate': [0.1],
              'n_estimators': [40],
              'max_depth': [3],
              'min_child_weight': [3],
              'gamma': [0.4],
              'subsample': [0.8],
              'colsample_bytree': [0.8],
              'scale_pos_weight': [1],
              'reg_alpha': [1e-5]
              }

# TODO: Initialize the classifier
clf = xgb.XGBClassifier(seed=2)

# TODO: Make an f1 scoring function using 'make_scorer'
f1_scorer = make_scorer(f1_score, pos_label='Blue')

# TODO: Perform grid search on the classifier using the f1_scorer as the scoring method
grid_obj = GridSearchCV(clf,
                        scoring=f1_scorer,
                        param_grid=parameters,
                        cv=5)

# TODO: Fit the grid search object to the training data and find the optimal parameters
grid_obj = grid_obj.fit(X_train, y_train)

# Get the estimator
clf = grid_obj.best_estimator_
print(clf)

# Report the final F1 score for training and testing after parameter tuning
f1, acc = predict_labels(clf, X_train, y_train)
print("F1 score and accuracy score for training set: {:.4f} , {:.4f}.".format(f1, acc))

f1, acc = predict_labels(clf, X_test, y_test)
print("F1 score and accuracy score for test set: {:.4f} , {:.4f}.".format(f1, acc))

pickle.dump(clf, open('xgboost.model', 'wb'))

loaded_clf = pickle.load(open('xgboost.model', 'rb'))

y_pred = pd.read_csv('Z:/Homebrew Programs/Python/leagueSummonerIDs/data/test_data.txt')

scores = loaded_clf.predict_proba(y_pred)
y_pred = loaded_clf.predict(y_pred)

print(scores)
print(y_pred)

plot_tree(clf)
plt.show()
