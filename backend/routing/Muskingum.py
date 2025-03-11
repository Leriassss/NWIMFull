
import numpy as np
import pandas as pd

from backend.contracts.Bundle import DataSimulation, RoutingContract, RoutingData
from backend.routing.Routing import Routing
from backend.routing.models.MuskingumModel import MuskingumModel

class Muskingum(Routing):
    def __init__(self,kwargs: RoutingContract):
        self.kwargs = kwargs
        self.muskingumModel = MuskingumModel(*self.kwargs)
    
    def calage(self,datas : DataSimulation):
        production = datas["pn"]
        K = self.muskingumModel.K
        x = self.muskingumModel.x
        dt = self.muskingumModel.dt
        n = len(production)

        # Calcul des coefficients
        C0 = (dt - 2 * K * x) / (2 * K * (1 - x) + dt)
        C1 = (dt + 2 * K * x) / (2 * K * (1 - x) + dt)
        C2 = (2 * K * (1 - x) - dt) / (2 * K * (1 - x) + dt)

        # Initialisation du tableau pour le débit simulé
        hydrogramm_muskingum = np.zeros(n)

        # Boucle pour le calcul de la méthode Muskingum
        for t in range(1, n):
            hydrogramm_muskingum[t] = max(0,
                C0 * production[t]
                + C1 * production[t - 1]
                + C2 * hydrogramm_muskingum[t - 1]
            )

        return np.maximum(0,hydrogramm_muskingum + datas["qbase"])

    def validation(self,datas : DataSimulation):
        production = datas["pn"]
        K = self.muskingumModel.K
        x = self.muskingumModel.x
        dt = self.muskingumModel.dt
        n = len(production)

        # Calcul des coefficients
        C0 = (dt - 2 * K * x) / (2 * K * (1 - x) + dt)
        C1 = (dt + 2 * K * x) / (2 * K * (1 - x) + dt)
        C2 = (2 * K * (1 - x) - dt) / (2 * K * (1 - x) + dt)

        # Initialisation du tableau pour le débit simulé
        hydrogramm_muskingum = np.zeros(n)

        # Boucle pour le calcul de la méthode Muskingum
        for t in range(1, n):
            hydrogramm_muskingum[t] = max(0,
                C0 * production[t]
                + C1 * production[t - 1]
                + C2 * hydrogramm_muskingum[t - 1]
            )
          
        return np.maximum(0,hydrogramm_muskingum + datas["qbase"])
    
    @staticmethod
    def help():
        """
        """
        description = """
        Implémente l'Hydrogramme selon Muskingum
        """
        print(description)
