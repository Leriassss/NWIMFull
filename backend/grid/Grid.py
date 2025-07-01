from joblib import Parallel, delayed
from backend.factory.OptimizationFactory import OptimizationFactory
from backend.grid.models.GridModel import GridModel
from backend.optimization.Optimization import Optimization
from backend.ptq.PTQ import PTQ
from backend.simulation.Simulation import Simulation
from backend.simulation.models.SimulationModel import SimulationModel

class Grid:
    def __init__(self, grid_data: GridModel, ptq_calage: PTQ, ptq_validation: PTQ):
        self.combinaisons, self.combin_names = grid_data.combinations, grid_data.combinations_names
        self.ptq_calage = ptq_calage
        self.ptq_validation = ptq_validation
        self.combin = []

    def _evaluate_combination(self, names, bundle, optim_name, optim_params):
        """Évalue une combinaison et retourne son score et le modèle correspondant."""
        sim = Simulation(*names, self.ptq_calage, self.ptq_validation)
        optim_method: Optimization = OptimizationFactory.createInstance(optim_name, sim, bundle, optim_params)
        optimization_results: SimulationModel = optim_method.optim()
        return optimization_results.validation_metric, names, optimization_results

    def grid_optimization(self, optim_name, **optim_params):
        
        results = Parallel(n_jobs=-1, backend="loky")(
            delayed(self._evaluate_combination)(names, bundle, optim_name, optim_params)
            for bundle, names in zip(self.combinaisons, self.combin_names)
        )

        best_crit_so_far, self.combin, best_result = max(results, key=lambda x: x[0])
        self.combin = [v for  v in self.combin]
        
        if isinstance(best_result, SimulationModel):
            return best_result
        else:
            raise ValueError("Aucun résultat satisfaisant")

