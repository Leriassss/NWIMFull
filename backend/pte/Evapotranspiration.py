# evapotranspiration_method.py
from abc import ABC, abstractmethod

class Evapotranspiration(ABC):
    """
    Classe abstraite pour les méthodes d'évapotranspiration.
    """

    @abstractmethod
    def calculate(self, args):
        """
        Méthode abstraite pour le calcul de l'évapotranspiration.
        """
        pass

    @staticmethod
    def help():
        """
        Méthode d'aide statique pour les classes implémentées.
        """
        return "Cette classe fournit une base pour les méthodes d'évapotranspiration."
