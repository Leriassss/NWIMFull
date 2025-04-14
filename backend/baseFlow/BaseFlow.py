# -*- coding: utf-8 -*-

from abc import ABC, abstractmethod

class BaseFlow(ABC):
    """
    Classe abstraite pour les modèles de production.
    """
    @abstractmethod
    def compute(self, *args, **kwargs):
        """
        Calcule le ruissellement net ou d'autres paramètres.
        """
        pass
    @abstractmethod
    def reverse_compute(self, *args, **kwargs):
        """
        Calcule le ruissellement net ou d'autres paramètres.
        """
        pass

    @abstractmethod
    def help():
        pass