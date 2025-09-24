# -*- coding: utf-8 -*-

from scipy.stats.qmc import LatinHypercube, scale
import pandas as pd 

from backend.optimization.models.LHCModel import LHCModel
from backend.simulation.models.SimulationModel import SimulationModel
from backend.simulation.Simulation import Simulation

class LatinHypercubeOptimization:
    def __init__(self, simulation : Simulation, param_ranges, lhc_model : LHCModel):
        self.simulation = simulation
        self.param_ranges = param_ranges
        self.n_samples = lhc_model.n_samples


    def population(self,param_ranges, n_samples):
        """
        Parameters
        ----------
        param_ranges : Dictionnaire des paramètres et leurs plages respectives, organisé par catégories.
                       Format : { "cat1": { "param1": [min, max], ... }, "cat2": ... }
        n_samples : Nombre d'échantillons à générer.

        Returns
        -------
        DataFrame avec des colonnes hiérarchiques (catégorie > paramètres).
        """
        # Extraction des paramètres et des plages
        categories = []
        param_names = []
        bounds_list = []

        for category, params in param_ranges.items():
            if params == {None} :
                continue
            for param, bounds in params.items():
                categories.append(category)
                param_names.append(param)
                bounds_list.append(bounds)

        # Création des échantillons avec Latin Hypercube
        sampler = LatinHypercube(d=len(param_names))
        samples = sampler.random(n=n_samples)


        parameters_scaled = scale(
            samples,
            l_bounds=[bounds[0] for bounds in bounds_list],
            u_bounds=[bounds[1] for bounds in bounds_list],
        )

        # Création du DataFrame avec des colonnes multi-index
        hierarchical_columns = pd.MultiIndex.from_tuples(
            list(zip(categories, param_names)),
            names=["Category", "Parameter"]
        )
        parameters_df = pd.DataFrame(parameters_scaled, columns=hierarchical_columns)
        return parameters_df

    def optim(self):
        crit = "KGE" if self.simulation.weightNSE < self.simulation.weightKGE else "NSE"
        parameters = self.population(self.param_ranges,self.n_samples)
        print("parameters optim LHS ------------- : ", parameters)
        results =  []
        for i in range(self.n_samples):
            parameters_line = parameters.iloc[i]
            extracted_params = {
                category: [parameters_line[(category, param)] for param in parameters[category].columns]
                for category in parameters.columns.levels[0]
            }
            
            qsim = self.simulation.manual_calibration(extracted_params)

            criteria_value = self.simulation.calibration_metric[crit]

            results.append({"parameters" : parameters_line, crit: criteria_value})

        runs = pd.DataFrame(results).sort_values([crit],ascending=False)
        best_run : pd.DataFrame = runs.iloc[0]["parameters"]
        best_pars = best_run.reset_index(level='Parameter', drop=True).groupby("Category").apply(list).to_dict()
        print("best_pars optim LHS -------------- : ", best_pars)
        best_sim = self.simulation.manual_calibration(best_pars)
        criteria_value, qsim_validation  = self.simulation.validation()
        return SimulationModel(best_sim,qsim_validation,best_pars,runs.iloc[0][crit],criteria_value[crit])
        #return runs.iloc[0] , best_sim #, runs, self.simulation.calibration_results

    def objective(self, objectif : float, iterations : int):
        i = 0
        best_so_far = -1000000
        sim_model = 0
        while(i < iterations):
            sim_r = self.optim()
            if(best_so_far < sim_r.validation_metric):
                best_so_far = sim_r.validation_metric
                sim_model = sim_r
            if(best_so_far>objectif):
                return sim_model
            print(i)
            i += 1
        if isinstance(sim_model, SimulationModel):
            return sim_model
        else:
            raise ValueError(" Aucun résultat satisfaisant")
