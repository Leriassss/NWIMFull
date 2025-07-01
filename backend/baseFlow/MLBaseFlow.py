import numpy as np
import pandas as pd

from backend.baseFlow.BaseFlow import BaseFlow
from backend.contracts.Bundle import DataBaseFlow
from backend.ptq.PTQ import PTQ

from sklearn.neighbors import KNeighborsRegressor
from sklearn.model_selection import GridSearchCV
class MLBaseFlow(BaseFlow):

    def __init__(self):
        """
        Initialise le modèle WMin avec un modèle de données validé.

        :param data_model: Instance de WMinDataModel contenant les données validées.
        """

        self._best_knn = None

    def compute(self, n, inf_rain, flow_series):
        qbase_witness = self.chapman_computing(flow_series)
        qbase_knn = self.knn_calibration(n,inf_rain,qbase_witness)
        return qbase_knn
        
    
    def chapman_computing(self, flow_series):
        alpha = 0.925
        Q_base = flow_series.copy()
        factor1 = (3 * alpha - 1) / (3 - alpha)
        factor2 = (1 - alpha) / (3 - alpha)
        
        for k in range(1, len(flow_series)):
            Q_base[k] = (
                factor1 * Q_base[k - 1]
                + factor2 * (flow_series[k] + flow_series[k - 1])
            )

        return Q_base
    
    def reverse_compute(self,previous_qbase, Q_direct):
        alpha = 0.925
        Q_base_rev = np.zeros(len(Q_direct))
        Q_base_rev[0]  = previous_qbase

        factor1 = ((3 * alpha) - 1) / (3 - alpha)
        factor2 = (1 - alpha) / (3 - alpha)

        for k in range(1, len(Q_direct)):
            Q_base_rev[k] = (1/(1-factor2)) * ( Q_base_rev[k-1]*(factor1+factor2) + 
                                            factor2*(Q_direct[k] + Q_direct[k-1]))
        
        return Q_base_rev
        
    def knn_calibration(self, n, inf_rain, Qbase):
        print()
        param_grid = {
            'n_neighbors': range(1, n),  
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        }
        variabes_df = pd.concat([inf_rain], axis=1)
        knn = KNeighborsRegressor()
        grid_search = GridSearchCV(knn, param_grid, cv=5, scoring='neg_mean_squared_error', n_jobs=-1)
        grid_search.fit(variabes_df, Qbase)

        self._best_knn = grid_search.best_estimator_
        

        q_base_knn = np.maximum(0, self._best_knn.predict(variabes_df))
        return q_base_knn
    
    def knn_validation(self,inf_rain):
        variabes_df = pd.concat([inf_rain], axis=1)
        return np.maximum(0, self._best_knn.predict(variabes_df))

    def validation(self,inf_rain):
        qbase_knn = self.knn_validation(inf_rain)
        return qbase_knn
        
    @staticmethod
    def help():
        """
        Fournit une description des méthodes disponibles dans la classe Recession.
        """
        description = """
        Implémente le filtre de récession de Furey-Gupta.


        Arguments pour `furey_gupta`:
        - flow_series : Série temporelle des débits [mm/jour] (pd.Series ou np.ndarray).
        - gamma : Coefficient de récession (par défaut 0.03).
        - cs_over_c : Ratio des coefficients (par défaut 1.1).
        """
        print(description)
