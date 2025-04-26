import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType
from PySide6 import QtCore
from PySide6.QtCore import QUrl, QtMsgType, QFileInfo, QFile

from api.RangeParametersQML import RangeParametersQML
from api.TestQML import TestQML
from api.GridParametersQML import GridParametersQML
from api.load_data.FileHandler import FileHandler
from api.load_data.TableModel import TableModel
from api.load_data.EToManager import EToManager
from api.FactoryManager import FactoryManager
from api.simulation.ManualCalibration import ManualCalibration
from api.simulation.AutomaticCalibration import AutomaticCalibration

# Implémentation de votre Message Handler
def qtMessageHandler(mode, context, message):
    match mode:
        case QtMsgType.QtDebugMsg:
            modeStr = "Debug"
        case QtMsgType.QtInfoMsg:
            modeStr = "Information"
        case QtMsgType.QtWarningMsg:
            modeStr = "Warning"
        case QtMsgType.QtCriticalMsg:
            modeStr = "Critical"
        case _:
            modeStr = "Fatal"
    fileName = QFileInfo(QFile(context.file).fileName()).fileName()
    print(f"QML - {modeStr}: {message} ({fileName}:{context.line})")

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer une instance de ProductionQML sans modèle spécifique

    engine = QQmlApplicationEngine()

    file_handler = FileHandler()
    eto_manager = EToManager()
    model = TableModel()
    factory_manager = FactoryManager()
    manual_calibration = ManualCalibration()
    automatic_calibration = AutomaticCalibration()

    engine.rootContext().setContextProperty("manualCalibration", manual_calibration)
    engine.rootContext().setContextProperty("automaticCalibration", automatic_calibration)
    engine.rootContext().setContextProperty("dataTableModel", model)
    engine.rootContext().setContextProperty("fileHandler", file_handler)
    engine.rootContext().setContextProperty("etoManager", eto_manager)
    engine.rootContext().setContextProperty("factoryManager", factory_manager)

    qmlRegisterType(GridParametersQML, "io.qml", 1, 0, "GridParametersQML")


    QtCore.qInstallMessageHandler(qtMessageHandler)
    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
