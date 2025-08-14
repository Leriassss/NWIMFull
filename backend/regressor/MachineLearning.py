# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class MachineLearning(ABC):
    """
    Classe abstraite pour les méthodes d'évapotranspiration.
    """

    @abstractmethod
    def tuning(self, args):
        """
        Méthode abstraite pour le calcul de l'évapotranspiration.
        """
        pass

    @abstractmethod
    def run(self, args):
        """
        Méthode abstraite pour le calcul de l'évapotranspiration.
        """
        pass