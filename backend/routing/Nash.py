import numpy as np
import pandas as pd
from scipy.special import gamma


from backend.contracts.Bundle import DataSimulation, RoutingContract
from backend.routing.Routing import Routing
from backend.routing.models.NashModel import NashModel

class Nash(Routing):
    def __init__(self, kwargs: RoutingContract):
        self.kwargs = kwargs
        self.nashModel =  NashModel(*self.kwargs)
    
    def compute(self,datas : DataSimulation):
        nash_k = self.nashModel.nash_k
        nash_n = self.nashModel.nash_n
        time_base = self.nashModel.time_base
        production = datas["pn"]
        n = len(production)
        xtra_flow = np.zeros(time_base-1)
        # Séquencement basé sur le temps
        seq_nash = np.arange(0, n, time_base)
        nash_time_base = []
        t = np.arange(0, time_base)
                # Fonction gamma de Nash
        q = pd.Series(
                    (1 / (nash_k * gamma(nash_n)))
                    * np.power(t / nash_k, nash_n - 1)
                    * np.exp(-t / nash_k)
                )
        for k in seq_nash:
            # Extraction des précipitations nettes pour une séquence donnée
            production_seq = production[k : k + time_base]
            len_ips = len(production)
            
            nash_k_result = pd.Series(np.convolve(production_seq, q))[: len(production_seq)]
            total_sim = np.convolve(production_seq, q)
            sim_flow = total_sim[:len_ips]    
            sim_flow[:len(xtra_flow)] += xtra_flow[:len(sim_flow)]
            xtra_flow = total_sim[len_ips:]
            
            nash_time_base.append(nash_k_result)

        # Assemblage des résultats et découpage à la taille initiale
        q_sim_direct =  pd.concat(nash_time_base).reset_index(drop=True)[:n]      
        return q_sim_direct
    
    def validation(self, datas : DataSimulation):
        return self.compute(datas)
    
    def calage(self, datas : DataSimulation):
        return self.compute(datas)
    
    @staticmethod
    def help():
        print(
            """
            Classe Nash : Simulation des débits par la méthode conceptuelle de Nash.
            
            Méthodes :
            ----------
            - __init__(data_model: NashModel) : Initialise l'objet Nash avec un modèle de données.
            - hydrogramm(production: pandas.Series) : Calcule le débit simulé à partir des précipitations nettes.
            - sim() : Simule les débits en tenant compte des précipitations nettes et de l'évapotranspiration.
            - help() : Affiche cette aide.
            """
        )
