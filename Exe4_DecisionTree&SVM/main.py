"""
Author
    Sebastian Mackiewicz - PJAIT student

Build program that based on given two datasets (in this scenario Pima Indians Diabetes Dataset
and Heart Disease Dataset) learn Decision Tree and SVM (Support Vector Machines)to classify data for each one dataset.
As a result display quality-related metrics.

Links for datasets:
Pima Indians Diabetes Dataset - https://machinelearningmastery.com/standard-machine-learning-datasets/
Heart Disease Dataset - https://www.kaggle.com/datasets/yasserh/heart-disease-dataset

Before running program install
pip install numpy
pip install sklearn

Make sure you have installed python at least in version 3.10
"""

import numpy as np
from sklearn import svm
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.model_selection import train_test_split

pima_indians_diabetes_file = 'pima_indians_diabetes.txt'
heart_disease_file = 'heart_disease.txt'

data_indians = np.loadtxt(pima_indians_diabetes_file, delimiter=',')
data_heart = np.loadtxt(heart_disease_file, delimiter=',')

X_indians, y_indians = data_indians[:, :-1], data_indians[:, -1]
X_water, y_water = data_heart[:, :-1], data_heart[:, -1]


def DecisionTreeClassification(data_x, data_y):
    """Description of the DecisionTreeClassification function
        Parameters:
             data_x: ndarray loaded with the data from the text file
             data_y: ndarray loaded with the data from the text file
        Returns:
             Return string with information about accuracy, precision and recall score of Decision Tree classification
    """

    X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.25, random_state=5)

    clf = DecisionTreeClassifier()
    clf = clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy_score = metrics.accuracy_score(y_test, y_pred)
    precision_score = metrics.precision_score(y_test, y_pred)
    recall_score = metrics.recall_score(y_test, y_pred)

    return print(f'Decision Tree:\nAccuracy: {accuracy_score} \nPrecision: {precision_score} \nRecall score: {recall_score}')


def SVMClassification(data_x, data_y):
    """Description of the SVMClassification function
        Parameters:
             data_x: ndarray loaded with the data from the text file
             data_y: ndarray loaded with the data from the text file
        Returns:
             Return string with information about accuracy, precision and recall score of SVM classification
    """

    X_train, X_test, y_train, y_test = train_test_split(data_x, data_y, test_size=0.25, random_state=5)

    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)

    y_pred = clf.predict(X_test)

    accuracy_score = metrics.accuracy_score(y_test, y_pred)
    precision_score = metrics.precision_score(y_test, y_pred)
    recall_score = metrics.recall_score(y_test, y_pred)

    return print(f'SVM:\nAccuracy: {accuracy_score} \nPrecision: {precision_score} \nRecall score: {recall_score}')


print('Pima Indians Diabetes Dataset')
print('=============================')
DecisionTreeClassification(X_indians, y_indians)
SVMClassification(X_indians, y_indians)
print('=============================')
print('\nHeart Disease Dataset')
print('=============================')
DecisionTreeClassification(X_water, y_water)
SVMClassification(X_water, y_water)
print('=============================')