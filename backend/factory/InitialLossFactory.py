from backend.initialLoss.AmountLoss import AmountLoss, AmountLossModel
from backend.initialLoss.EToLoss import EToLoss, EToLossModel
from backend.initialLoss.IaLoss import IaLoss, IaLossModel
from backend.initialLoss.NoLoss import NoLoss, NoLossModel
from backend.initialLoss.PLoss import PLoss, PLossModel


class InitialLossFactory:
    methods = {
        "ia_loss": [IaLoss, IaLossModel],
        "eto_loss": [EToLoss, EToLossModel],
        "s_loss": [AmountLoss, AmountLossModel],
        "no_loss": [NoLoss, NoLossModel],
        "p_loss": [PLoss, PLossModel]
    }

    """
    Fabrique pour créer des instances dynamiques des méthodes.
    """

    @staticmethod
    def createInstance(method_name: str, *args):
        if method_name not in InitialLossFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        return InitialLossFactory.methods[method_name][0](
            args[0], InitialLossFactory.methods[method_name][1](*args[1:])
        )

    def getMethods(self, method_name: str):
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        return True

    @staticmethod
    def getModel(method_name: str):
        """
        Retourne la classe du modèle associée à une méthode spécifique.
        """
        if method_name not in InitialLossFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        return InitialLossFactory.methods[method_name][1]

    @staticmethod
    def createModel(method_name: str, *args):
        """
        Crée une instance du modèle associé à une méthode spécifique.
        """
        model_class = InitialLossFactory.getModel(method_name)
        return model_class(*args)

    @staticmethod
    def getModelParameters(method_name: str):
        """
        Retourne les noms des paramètres du modèle associé à une méthode spécifique.
        """
        model_class = InitialLossFactory.getModel(method_name)
        return model_class.get_parameter_names()

    @classmethod
    def getMethodKeys(cls):
        """Retourne la liste des noms de méthodes disponibles."""
        return list(cls.methods.keys())


