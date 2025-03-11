import numpy as np
import pandas as pd
from scipy.special import gamma


from backend.contracts.Bundle import DataSimulation, RoutingContract, RoutingData
from backend.routing.Routing import Routing
from backend.routing.models.NashModel import NashModel

class Nash(Routing):
    def __init__(self, kwargs: RoutingContract):
        self.kwargs = kwargs
        self.nashModel =  NashModel(*self.kwargs)
    
    def calage(self,datas : DataSimulation):
        nash_k = self.nashModel.nash_k
        nash_n = self.nashModel.nash_n
        time_base = self.nashModel.time_base
        production = datas["pn"]
        n = len(production)

        # Séquencement basé sur le temps
        seq_nash = np.arange(0, n, time_base)
        nash_time_base = []

        for k in seq_nash:
            # Extraction des précipitations nettes pour une séquence donnée
            production_seq = production[k : k + time_base]
            if production_seq.sum() > 0:
                t = np.arange(0, len(production_seq))
                # Fonction gamma de Nash
                q = pd.Series(
                    (1 / (nash_k * gamma(nash_n)))
                    * np.power(t / nash_k, nash_n - 1)
                    * np.exp(-t / nash_k)
                )
                # Convolution entre la séquence de production et la fonction gamma
                nash_k_result = pd.Series(np.convolve(production_seq, q))[: len(production_seq)]
            else:
                # Si aucune production dans la séquence, retourne des zéros
                nash_k_result = pd.Series(np.zeros_like(production_seq))

            nash_time_base.append(nash_k_result)

        # Assemblage des résultats et découpage à la taille initiale
        q_sim_direct =  pd.concat(nash_time_base).reset_index(drop=True)[:n]
        return np.maximum(0,q_sim_direct + datas["qbase"])
    
    def validation(self, datas : DataSimulation):
        nash_k = self.nashModel.nash_k
        nash_n = self.nashModel.nash_n
        time_base = self.nashModel.time_base
        #production = np.maximum(0, net_rainfall - self.ptq_calage.etp)
        production = datas["pn"]
        n = len(production)

        # Séquencement basé sur le temps
        seq_nash = np.arange(0, n, time_base)
        nash_time_base = []

        for k in seq_nash:
            # Extraction des précipitations nettes pour une séquence donnée
            production_seq = production[k : k + time_base]
            if production_seq.sum() > 0:
                t = np.arange(0, len(production_seq))
                # Fonction gamma de Nash
                q = pd.Series(
                    (1 / (nash_k * gamma(nash_n)))
                    * np.power(t / nash_k, nash_n - 1)
                    * np.exp(-t / nash_k)
                )
                # Convolution entre la séquence de production et la fonction gamma
                nash_k_result = pd.Series(np.convolve(production_seq, q))[: len(production_seq)]
            else:
                # Si aucune production dans la séquence, retourne des zéros
                nash_k_result = pd.Series(np.zeros_like(production_seq))

            nash_time_base.append(nash_k_result)

        # Assemblage des résultats et découpage à la taille initiale
        q_sim_direct =  pd.concat(nash_time_base).reset_index(drop=True)[:n]
        return np.maximum(0,q_sim_direct + datas["qbase"])
    
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
