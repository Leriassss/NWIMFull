# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod

class Optimization(ABC):
    """
    Classe abstraite pour les modèles de production.
    """
    @abstractmethod
    def optim(self, *args, **kwargs):
        """
        Calcule le ruissellement net ou d'autres paramètres.
        """
        pass
