from backend.factory.ProductionFactory import ProductionFactory
from backend.factory.RecessionFactory import RecessionFactory
from backend.factory.RoutingFactory import RoutingFactory
from backend.factory.InitialLossFactory import InitialLossFactory
from backend.factory.OptimizationFactory import OptimizationFactory

from PySide6.QtCore import QObject, Signal, Slot, Property


class FactoryManager(QObject):

    factories = {
        "Production": ProductionFactory,
        "Recession": RecessionFactory,
        "Routing": RoutingFactory,
        "InitialLoss": InitialLossFactory,
        "Optimization" : OptimizationFactory
    }


    def getFactoryMethods(self, factory_name):
        current_factory = FactoryManager.get_factory(factory_name)
        return current_factory.getMethodKeys()


    @Property(list, constant = True)
    def productionMethods(self):
        return self.getFactoryMethods("Production")

    @Property(list, constant = True)
    def recessionMethods(self):
        print("----------------------------REC-------------------")
        print(self.getFactoryMethods("Recession"))
        return self.getFactoryMethods("Recession")

    @Property(list, constant = True)
    def initialLossMethods(self):
        return self.getFactoryMethods("InitialLoss")

    @Property(list, constant = True)
    def routingMethods(self):
        return self.getFactoryMethods("Routing")

    @classmethod
    def get_factory(cls, factory_name):
        """Retourne une instance de la factory demandée si elle existe, sinon None."""
        factory_class = cls.factories.get(factory_name)
        return factory_class() if factory_class else None

    @classmethod
    def get_factory_keys(cls):
        """Retourne la liste des noms des factories disponibles."""
        return list(cls.factories.keys())
