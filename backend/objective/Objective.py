from contracts.Bundle import RoutingData
from factory.OptimizationFactory import OptimizationFactory
from optimization.Optimization import Optimization
from simulation.models.SimulationModel import SimulationModel
from simulation.Simulation import Simulation

class Objective:
    def __init__(self, simulation: Simulation):
        self.simulation = simulation
        self.kwargs = []

    def sim(self, objectif: float, optim_name, kwargs: RoutingData, n_sim = 50, **optim_params):
        """
        Exécute l'optimisation jusqu'à obtenir un critère de validation supérieur à 'objectif'.
        """
        optim_method: Optimization = OptimizationFactory.createInstance(optim_name, self.simulation, kwargs, **optim_params)
        best_so_far = -float("inf")  # Meilleure valeur trouvée
        sim_model = None
        i = 0

        while True:
            sim_r: SimulationModel = optim_method.optim()

            if sim_r.validation_metric > best_so_far:
                best_so_far = sim_r.validation_metric
                sim_model = sim_r
                self.kwargs = self.simulation.kwargs

            print(f"Iteration {i}: Validation Metric = {sim_r.validation_metric}")

            # Condition d'arrêt : si l'objectif est atteint
            if sim_r.validation_metric >= objectif:
                return sim_model
            
            # Condition de sécurité pour éviter une boucle infinie
            if i >= n_sim:
                break
            
            i += 1

        # Si on sort de la boucle sans atteindre l'objectif
        if sim_model:
            print("Aucun résultat dépassant l'objectif, mais on retourne la meilleure solution trouvée.")
            return sim_model
        else:
            raise ValueError("Aucun résultat satisfaisant après 50 itérations.")
