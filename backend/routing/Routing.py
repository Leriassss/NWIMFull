# -*- coding: utf-8 -*-
# evapotranspiration_method.py
from abc import ABC, abstractmethod

class Routing(ABC):
    """
    Classe abstraite pour les méthodes d'évapotranspiration.
    """

    @abstractmethod
    def calage(self, args):
        """
        Méthode abstraite pour le calcul de l'évapotranspiration.
        """
        pass

    @abstractmethod
    def validation(self, args):
        """
        Méthode abstraite pour le calcul de l'évapotranspiration.
        """
        pass

    @abstractmethod
    def help():
        """
        Méthode d'aide statique pour les classes implémentées.
        """
        pass

    


"""
import numpy as np

class Routing:
    def __init__(self, NET_RAINFALL, ETP):
        self._NET_RAINFALL = NET_RAINFALL
        self._ETP = ETP

    def get_net_rainfall(self):
        return np.maximum(0,self._NET_RAINFALL-self._ETP)

    def get_total_flow(q_sim, q_base):
        return q_sim+q_base
    
    def sim(self,Q_base,hydrogramm,*args):
        rainfall_without_eto = self.get_net_rainfall()
        q_sim_without_q_flow = hydrogramm(rainfall_without_eto,*args)
        Q_sim = self.get_total_flow(q_sim_without_q_flow, Q_base)
        return Q_sim
"""








