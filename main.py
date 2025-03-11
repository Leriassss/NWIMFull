# This Python file uses the following encoding: utf-8
import sys
from pathlib import Path
import numpy as np
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine

from api.ProductionQML import ProductionQML
from api.InitialLossQML import InitialLossQML
from api.RoutingQML import RoutingQML
from api.RecessionQML import RecessionQML
from api.GAModel import GAModel

if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Créer une instance de ProductionQML sans modèle spécifique
    production_qml = ProductionQML()
    loss_qml = InitialLossQML()
    routing_qml = RoutingQML()
    recession_qml = RecessionQML()
    gamodel_qml  = GAModel()

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("productionModel", production_qml)
    engine.rootContext().setContextProperty("initialLossModel", loss_qml)
    engine.rootContext().setContextProperty("routingModel", routing_qml)
    engine.rootContext().setContextProperty("recessionModel", recession_qml)
    engine.rootContext().setContextProperty("gaModel", gamodel_qml)

    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
