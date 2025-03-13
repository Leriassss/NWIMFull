import sys
from pathlib import Path
import numpy as np
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType

from api.ProductionQML import ProductionQML
from api.InitialLossQML import InitialLossQML
from api.RoutingQML import RoutingQML
from api.RecessionQML import RecessionQML
from api.OptimizationQML import OptimizationQML

from api.RangeParametersQML import RangeParametersQML
from api.TestQML import TestQML

#import io.qt.RangeParameter
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Créer une instance de ProductionQML sans modèle spécifique
    production_qml = ProductionQML()
    loss_qml = InitialLossQML()
    routing_qml = RoutingQML()
    recession_qml = RecessionQML()
    optimization_qml  = OptimizationQML()
    #range_qml  = RangeParameterQML()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("productionModel", production_qml)
    engine.rootContext().setContextProperty("initialLossModel", loss_qml)
    engine.rootContext().setContextProperty("routingModel", routing_qml)
    engine.rootContext().setContextProperty("recessionModel", recession_qml)
    engine.rootContext().setContextProperty("optimizationModel", optimization_qml)

    #engine.rootContext().setContextProperty("productionrangeModel", range_qml)
    #engine.rootContext().setContextProperty("initialLossrangeModel", range_qml)
    #qmlRegisterType(TestQML, "io.qt.test", 1, 0, "TestModel")
   #qmlRegisterType(RangeParameterQML, "io.qt.RangeParameterQML", 1, 0, "RangeParameterModel")


    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
