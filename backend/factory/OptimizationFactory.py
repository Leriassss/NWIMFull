


from optimization.DifferentialEvolutionOptimization import DifferentialEvolutionOptimization, DEModel
from optimization.GeneticalAlgortihmOptimization import GeneticalAlgorithmOptimization, GAModel
from optimization.LatinHypercubeOptimization import LatinHypercubeOptimization, LHCModel


class OptimizationFactory:
    methods = {
            "lhc" : [LatinHypercubeOptimization, LHCModel],
            "ga" : [GeneticalAlgorithmOptimization, GAModel],
            "de" : [DifferentialEvolutionOptimization, DEModel]
        }
            
    """
    Fabrique pour créer des instances dynamiques des méthodes.
    """
    @staticmethod
    def createInstance(method_name: str, sim,bundle, **params):
        model = OptimizationFactory.methods[method_name][1](**params)

        return OptimizationFactory.methods[method_name][0](sim,bundle,model)
    
    def getMethods(self,method_name: str):
        if method_name not in self.methods:
            raise ValueError(f"Méthode inconnue : {method_name}")
        else:
            return True

