from backend.factory.ProductionFactory import ProductionFactory
from backend.factory.RecessionFactory import RecessionFactory
from backend.factory.RoutingFactory import RoutingFactory
from backend.factory.InitialLossFactory import InitialLossFactory

class FactoryManager:
    """Gère la sélection et l'instanciation des différentes factories."""

    factories = {
        "Production": ProductionFactory,
        "Recession": RecessionFactory,
        "Routing": RoutingFactory,
        "InitialLoss": InitialLossFactory
    }

    @classmethod
    def get_factory(cls, factory_name):
        """Retourne une instance de la factory demandée si elle existe, sinon None."""
        factory_class = cls.factories.get(factory_name)
        return factory_class() if factory_class else None

    @classmethod
    def get_factory_keys(cls):
        """Retourne la liste des noms des factories disponibles."""
        return list(cls.factories.keys())
