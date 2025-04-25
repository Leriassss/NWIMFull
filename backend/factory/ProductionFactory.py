from backend.production.Holtan import Holtan, HoltanModel
from backend.production.Horton import Horton, HortonModel
from backend.production.Phi import Phi, PhiModel
from backend.production.Philip import Philip, PhilipModel
from backend.production.SCS import SCS, SCSModel
from backend.production.W import W, WModel
from backend.production.WMin import WMin, WMinModel


class ProductionFactory:
    methods = {
            "SCS" : [SCS, SCSModel],
            "W" : [W, WModel],
            "WMin" : [WMin, WMinModel],
            "Horton" : [Horton, HortonModel],
            "Holtan" : [Holtan,  HoltanModel],
            "Phi" : [Phi, PhiModel],
            "Philip" : [Philip, PhilipModel]
        }
            
    """
    Fabrique pour créer des instances dynamiques des méthodes.
    """
    @staticmethod
    def createInstance(method_name: str, *args):
        return ProductionFactory.methods[method_name][0](
            args[0],
            ProductionFactory.methods[method_name][1](*args[1:]))
    
    def getMethods(self,method_name: str):
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return True
        
    @staticmethod
    def getModel(method_name: str):
        if method_name not in ProductionFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return ProductionFactory.methods[method_name][1]

    @staticmethod
    def createModel(method_name: str, *args):
        return ProductionFactory.getModel(method_name,*args)

    @staticmethod
    def getModelParameters(method_name: str):
        model_class = ProductionFactory.getModel(method_name)
        return model_class.get_parameter_names()



    @classmethod
    def getMethodKeys(cls):
        """Retourne la liste des noms de méthodes disponibles."""
        return list(cls.methods.keys())
