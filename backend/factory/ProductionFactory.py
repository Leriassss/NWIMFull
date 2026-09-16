from backend.production.Philip import Philip, PhilipModel
from backend.production.SCS import SCS, SCSModel
from backend.production.WMin import WMin, WMinModel
from backend.production.HortonModified import HortonModified, HortonModifiedModel

class ProductionFactory:
    methods = {
            "SCS" : [SCS, SCSModel],
            "WMin" : [WMin, WMinModel],
            "HortonModified" : [HortonModified, HortonModifiedModel],
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
