from unittest import TestCase

from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

from sklearn_evaluation import ClassifierEvaluator


class TestReportGeneration(TestCase):
    def setUp(self):
        iris = load_iris()
        X_train, X_test, y_train, y_test = train_test_split(
            iris.data, iris.target, test_size=0.30, random_state=0
        )

        model = RandomForestClassifier()
        model.fit(X_train, y_train)

        y_pred = model.predict(X_test)
        y_score = model.predict_proba(X_test)
        target_names = ["setosa", "versicolor", "virginica"]
        feature_names = range(4)
        model_name = "a model"

        self.results = ClassifierEvaluator(
            estimator=model,
            y_true=y_test,
            y_pred=y_pred,
            y_score=y_score,
            feature_names=feature_names,
            target_names=target_names,
            estimator_name=model_name,
        )

    def test_can_create_report(self):
        self.results.make_report()
