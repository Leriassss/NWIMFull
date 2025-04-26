
from backend.optimization.DifferentialEvolutionOptimization import DifferentialEvolutionOptimization, DEModel
from backend.optimization.GeneticalAlgortihmOptimization import GeneticalAlgorithmOptimization, GAModel
from backend.optimization.LatinHypercubeOptimization import LatinHypercubeOptimization, LHCModel


class OptimizationFactory:
    methods = {
        "LatinHypercube": [LatinHypercubeOptimization, LHCModel],
        "GeneticalAlgorithm": [GeneticalAlgorithmOptimization, GAModel],
        "DifferentialEvolution": [DifferentialEvolutionOptimization, DEModel]
    }

    """
    Fabrique pour créer des instances dynamiques des méthodes d'optimisation.
    """

    @staticmethod
    def createInstance(method_name: str, *args):
        print("-----------OPTIMIZATION FACTORY ----------")
        print(args[2:])
        return OptimizationFactory.methods[method_name][0](
            args[0],  # sim
            args[1],  # bundle
            OptimizationFactory.methods[method_name][1](**args[2:][0])  # Model instancié avec les paramètres restants
        )

    def getMethods(self, method_name: str):
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return True

    @staticmethod
    def getModel(method_name: str):
        if method_name not in OptimizationFactory.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return OptimizationFactory.methods[method_name][1]

    @staticmethod
    def createModel(method_name: str, *args):
        return OptimizationFactory.getModel(method_name)(*args)

    @staticmethod
    def getModelParameters(method_name: str):
        model_class = OptimizationFactory.getModel(method_name)
        return model_class.get_parameter_names()

    @classmethod
    def getMethodKeys(cls):
        """Retourne la liste des noms de méthodes d'optimisation disponibles."""
        return list(cls.methods.keys())


