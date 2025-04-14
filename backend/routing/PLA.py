
import numpy as np
from backend.contracts.Bundle import DataSimulation, RoutingContract
from backend.routing.Routing import Routing
from backend.routing.models.PLAModel import PLAModel

class PLA(Routing):
    def __init__(self, kwargs: RoutingContract):
        self.kwargs = kwargs
        self.plaModel = PLAModel(*self.kwargs)


    def calage(self,datas : DataSimulation):
        return self.sim(datas["pn"])
    
    def validation(self,datas : DataSimulation):
        return self.sim(datas["pn"])
        
    def sim(self,q):
        mu= self.plaModel.mu
        landa = self.plaModel.landa
        t_x = self.plaModel.t_x 
        s_f = self.plaModel.s_f
        
        epsilon = 1e-6
        n = len(q)
        x = np.zeros(n)
        for i in range(3, n):
            mu_over_landa = (mu / landa) if np.isfinite(mu / landa) else 0
            if q[i] == 0:
                x[i] = x[i - 1] - mu_over_landa * x[i - 1]
            else:
                x[i] = x[i - 1] + mu_over_landa * ((q[i] + epsilon) ** (2 * mu- 1))
        
        q_sim = np.zeros(n)
        for i in range(2, n):
            power_pla = q_sim[i - 1]  ** (2 * mu- 1) if q_sim[i - 1] > 0 else 0
            mu_over_landa = (mu / landa) if np.isfinite(mu / landa) else 0
            if x[i] * s_f > t_x:
                q_sim[i] = max(0, q_sim[i - 1] - mu_over_landa * power_pla + s_f * x[i] * q[i - 1] /landa)
            else:
                q_sim[i] =max(0,q_sim[i - 1] - mu_over_landa * power_pla) 
        return np.where((q_sim < 0) | ~np.isfinite(q_sim), 0, q_sim)
    
    @staticmethod
    def help():
        """
        Affiche l'aide pour l'utilisation de la classe PLA.

        Returns
        -------
        None
        """
        print(
            """
            Classe PLA : Simulation des débits par le Principe de Moindre Action (PLA).

            Méthodes :
            ----------
            - __init__(production) : Initialise l'objet PLA avec la série de production.
            - hydrogramm(MU, LANDA, TX, SF, P, ETP) : Calcule le débit simulé à partir des paramètres et des séries d'entrée.
            - help() : Affiche cette aide.

            Paramètres des méthodes :
            -------------------------
            - MU : Coefficient d'humidité spécifique.
            - LANDA : Coefficient de transfert des flux.
            - TX : Valeur seuil pour le débit.
            - SF : Facteur de redistribution.
            - P : Série des précipitations [mm/j].
            - ETP : Série de l'évapotranspiration potentielle [mm/j].
            """
        )
