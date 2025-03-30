from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtQml import QmlElement
from api.FactoryManager import FactoryManager

QML_IMPORT_NAME = "io.qml"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class TestQML(QObject):
    parametersChanged = Signal()
    methodChanged = Signal()
    parameterErrorChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_method = None
        self._parameters = {}
        self._methods =[]
        self._parameterErrors = {}
        self._keys = []

    @Property('QVariant', notify=parametersChanged)
    def availableMethods(self):
        """Retourne la liste des méthodes disponibles pour le ComboBox en QML."""
        return self._methods

    @Property('QVariant', notify=parametersChanged)
    def parameterNames(self):
        """Retourne les noms des paramètres disponibles."""
        return list(self._parameters.keys())

    @Property('QVariant', notify=parametersChanged)
    def parameters(self):
        """Retourne les paramètres """
        return self._parameters


    @Slot(str)
    def setFactory(self, factory_name):
        """Définit la factory et charge ses méthodes."""
        self._factory = FactoryManager.get_factory(factory_name)
        if self._factory:
            self._methods = self._factory.getMethodKeys()
            self._parameters = {}
            self._current_method = None
        else:
            self._methods = []
            self._parameters = {}
            self._current_method = None

        self.methodChanged.emit()
        self.parametersChanged.emit()

    @Slot(str)
    def setMethod(self, index):
        """Met à jour la méthode et initialise ses paramètres par défaut."""
        method_name = self._methods[int(index)]
        if method_name in self._factory.methods:
            self._current_method =  method_name
            self._keys = self._factory.getModelParameters(method_name)
            self._parameters = {key: None for key in self._keys}
            self.methodChanged.emit()
            self.parametersChanged.emit()

    @Slot(str, str)
    def updateParameter(self, key, value):
        if key in self._keys:
            """Met à jour un paramètre et applique la validation."""
            self._parameters[key] = value
            model = self._factory.getModel(self._current_method)

            validation_result = model.validate_parameter(key, value)

            print("---------------------UP")
            print(self._parameters)
            print(self._current_method)
            print(validation_result)

            if validation_result is True:
                self._parameterErrors[key] = ""  # Pas d'erreur
            else:
                self._parameterErrors[key] = validation_result  # Stocke l'erreur

                print(f"Validation pour {key}: {validation_result}")

            self.parametersChanged.emit()
            self.parameterErrorChanged.emit()

    @Property('QVariant', notify=parameterErrorChanged)
    def parameterErrors(self):
        """Retourne les erreurs de validation pour chaque paramètre."""
        return self._parameterErrors
