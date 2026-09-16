from backend.factory.OptimizationFactory import OptimizationFactory
from backend.grid.models.GridModel import GridModel
from backend.optimization.Optimization import Optimization
from backend.ptq.PTQ import PTQ
from backend.simulation.Simulation import Simulation
from backend.simulation.models.SimulationModel import SimulationModel

class Grid:
    def __init__(self, grid_data: GridModel, ptq_calage: PTQ, ptq_validation: PTQ):
        self.combinaisons = grid_data.combinations
        self.combin_names = grid_data.combinations_names
        self.ptq_calage = ptq_calage
        self.ptq_validation = ptq_validation
        self.combin = []

    def _evaluate_combination(
        self,
        names,
        bundle,
        m_weightNSE,
        m_weightKGE,
        optim_name,
        optim_params
    ):
        sim = Simulation(*names, self.ptq_calage, self.ptq_validation)

        sim.weightNSE = m_weightNSE
        sim.weightKGE = m_weightKGE
        sim.crit = "KGE" if sim.weightNSE < sim.weightKGE else "NSE"

        optim_method: Optimization = OptimizationFactory.createInstance(
            optim_name, sim, bundle, optim_params
        )

        optimization_results: SimulationModel = optim_method.optim()

        return (
            optimization_results.validation_metric,
            names,
            optimization_results
        )

    def grid_optimization(
        self,
        m_weightNSE,
        m_weightKGE,
        optim_name,
        **optim_params
    ):
        results = []

        for bundle, names in zip(self.combinaisons, self.combin_names):
            res = self._evaluate_combination(
                names,
                bundle,
                m_weightNSE,
                m_weightKGE,
                optim_name,
                optim_params
            )
            results.append(res)

        best_crit, best_names, best_result = max(results, key=lambda x: x[0])
        self.combin = list(best_names)

        if isinstance(best_result, SimulationModel):
            return best_result, self.combin
        else:
            raise ValueError("Aucun résultat satisfaisant")
