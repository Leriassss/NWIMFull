import sys
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQml import qmlRegisterType



from api.RangeParametersQML import RangeParametersQML
from api.TestQML import TestQML
from api.GridParametersQML import GridParametersQML

#import io.qt.RangeParameter
if __name__ == "__main__":
    app = QGuiApplication(sys.argv)

    # Créer une instance de ProductionQML sans modèle spécifique

    engine = QQmlApplicationEngine()

    #engine.rootContext().setContextProperty("productionrangeModel", range_qml)
    #engine.rootContext().setContextProperty("initialLossrangeModel", range_qml)
    #qmlRegisterType(TestQML, "io.qt.test", 1, 0, "TestModel")
   #qmlRegisterType(RangeParameterQML, "io.qt.RangeParameterQML", 1, 0, "RangeParameterModel")


    engine.load("main.qml")

    if not engine.rootObjects():
        sys.exit(-1)

    sys.exit(app.exec())
