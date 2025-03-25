import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType


from api.RangeParametersQML import RangeParametersQML
from api.TestQML import TestQML
from api.GridParametersQML import GridParametersQML
from api.load_data.FileHandler import FileHandler
from api.load_data.TableModel import TableModel
if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Créer une instance de ProductionQML sans modèle spécifique

    engine = QQmlApplicationEngine()

    file_handler = FileHandler()
    model = TableModel()
    engine.rootContext().setContextProperty("dataTableModel", model)
    engine.rootContext().setContextProperty("fileHandler", file_handler)

    qmlRegisterType(GridParametersQML, "io.qml", 1, 0, "GridParametersQML")



    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
