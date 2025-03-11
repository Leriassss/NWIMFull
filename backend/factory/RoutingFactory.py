from backend.routing.HUN import HUN, HUNModel
from backend.routing.Muskingum import Muskingum, MuskingumModel
from backend.routing.Nash import Nash, NashModel
from backend.routing.PLA import PLA, PLAModel



class RoutingFactory:
    methods = {
        "HUN": [HUN, HUNModel],
        "Nash": [Nash, NashModel],
        "Muskingum": [Muskingum, MuskingumModel],
        "PLA": [PLA, PLAModel]
    }

    """
    Fabrique pour créer des instances dynamiques des méthodes de routage.
    """
    @staticmethod
    def createInstance(method_name: str, *args):
        return RoutingFactory.methods[method_name][0](
            *args[0:1],  # Arguments spécifiques pour la méthode
            RoutingFactory.methods[method_name][1](*args[1:])  # Modèle spécifique pour la méthode
        )

    def getMethods(self, method_name: str):
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return True

    @staticmethod
    def getModel(method_name: str):
        if method_name not in RoutingFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return RoutingFactory.methods[method_name][1]

    @staticmethod
    def createModel(method_name: str, *args):
        return RoutingFactory.getModel(method_name).create(*args)

    @staticmethod
    def getModelParameters(method_name: str):
        model_class = RoutingFactory.getModel(method_name)
        return model_class.get_parameter_names()

    @classmethod
    def getMethodKeys(cls):
        """Retourne la liste des noms de méthodes disponibles."""
        return list(cls.methods.keys())

