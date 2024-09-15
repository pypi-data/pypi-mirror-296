import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, confusion_matrix


def dummify(data, dummy_columns):
    data_categorical = data[dummy_columns]
    data_numerical = data.drop(dummy_columns, axis=1)
    data_dummies = pd.get_dummies(data_categorical, columns=dummy_columns)
    data = pd.concat([data_numerical, data_dummies], axis=1)
    return data


def learn_all(X, y, test_size=.2, random_state=42):
    response = {}
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    X_train = X_train / np.max(X_train)
    X_test = X_test / np.max(X_test)

    models = [
        ("LR", LogisticRegression()),
        ("KNN", KNeighborsClassifier()),
        ("DTC", DecisionTreeClassifier()),
        ("RFC", RandomForestClassifier()),
        ("GNB", GaussianNB()),
        ("SVC", SVC())
    ]

    for name, model in models:
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        acc = accuracy_score(y_test, y_pred)  # sum(y_pred==y_test)/len(y_test)
        cm = confusion_matrix(y_test, y_pred)
        response[name] = {
            "accuracy_score": acc,
            "confusion_matrix": cm,
            "model": model
        }
    return response
