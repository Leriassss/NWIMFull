
from backend.baseFlow.Chapman import Chapman, ChapmanModel
from backend.baseFlow.ExponentialRecession import ExponentialRecessionCurve
from backend.baseFlow.FureyGupta import FureyGupta, FureyGuptaModel
from backend.baseFlow.QuadraticRecession import QuadraticRecessionCurve, SeparationModel

class RecessionFactory:
    methods = {
        "Chapman": [Chapman, ChapmanModel],
        "FureyGupta": [FureyGupta, FureyGuptaModel],
        "Quadratic": [QuadraticRecessionCurve, SeparationModel],
        "Exponential": [ExponentialRecessionCurve, SeparationModel]
    }

    """
    Fabrique pour créer des instances dynamiques des méthodes de récession.
    """

    @staticmethod
    def createInstance(method_name: str, *args):
        if method_name not in RecessionFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")

        # Créer l'instance de la méthode et du modèle
        return RecessionFactory.methods[method_name][0](
            args[0],
            RecessionFactory.methods[method_name][1](*args[1:])
        )

    def getMethods(self, method_name: str):
        """
        Vérifie si la méthode est disponible dans la fabrique.
        """
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        return True

    @staticmethod
    def getModel(method_name: str):
        """
        Retourne le modèle associé à la méthode spécifiée.
        """
        if method_name not in RecessionFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        return RecessionFactory.methods[method_name][1]

    @staticmethod
    def createModel(method_name: str, *args):
        """
        Crée une instance du modèle associé à la méthode spécifiée.
        """
        return RecessionFactory.getModel(method_name)(*args)

    @staticmethod
    def getModelParameters(method_name: str):
        """
        Retourne les paramètres du modèle associé à la méthode spécifiée.
        """
        model_class = RecessionFactory.getModel(method_name)
        return model_class.get_parameter_names()

    @classmethod
    def getMethodKeys(cls):
        """
        Retourne la liste des noms de méthodes disponibles.
        """
        return list(cls.methods.keys())
