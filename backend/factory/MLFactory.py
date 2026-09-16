from backend.regressor.KNN import KNN, KNNModel
from backend.regressor.RandomForest import RandomForest, RandomForestModel
from backend.regressor.RidgeRegression import RidgeRegression, RidgeRegressionModel
from backend.regressor.SVM import SVM, SVMModel
from backend.regressor.XGBoost import XGBoost, XGBoostModel


class MLFactory:
    methods = {
        "SVM": [SVM, SVMModel],
        "Ridge": [RidgeRegression, RidgeRegressionModel],
        "KNN": [KNN, KNNModel],
        "Random Forest": [RandomForest, RandomForestModel],
        "XGBoost" : [XGBoost, XGBoostModel]
    }

    """
    Fabrique pour créer des instances dynamiques des méthodes de routage.
    """
    @staticmethod
    def createInstance(method_name: str, *args):
        return MLFactory.methods[method_name][0](*args)

    def getMethods(self, method_name: str):
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return True

    @staticmethod
    def getModel(method_name: str):
        if method_name not in MLFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return MLFactory.methods[method_name][1]

    @staticmethod
    def createModel(method_name: str, args):
        return MLFactory.getModel(method_name)(**args)

    @staticmethod
    def getModelParameters(method_name: str):
        model_class = MLFactory.getModel(method_name)
        return model_class.get_parameter_names()

    @classmethod
    def getMethodKeys(cls):
        """Retourne la liste des noms de méthodes disponibles."""
        return list(cls.methods.keys())

