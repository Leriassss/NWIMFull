from PySide6.QtQml import QmlElement
from PySide6.QtCore import QObject, Property, Signal, Slot
from api.FactoryManager import FactoryManager
import math

QML_IMPORT_NAME = "io.qml"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class RangeParametersQML(QObject):
    parametersChanged = Signal()
    parametersNamesChanged = Signal()
    parametersValuesChanged = Signal()
    methodChanged = Signal()
    parameterErrorChanged = Signal()
    availableMethodsChanged = Signal()

    def __init__(self, parent=None):
        """Initialisation sans écoute du changement de factory."""
        super().__init__(parent)
        self._factory = None
        self._current_method = None
        self._parameters = {}
        self._parameterErrors = {}
        self._methods = []
        self._keys = []

    @Property('QVariant')
    def methodKeys(self):
        return self._keys

    @Property(str, notify=methodChanged)
    def currentMethod(self):
        return self._current_method

    @Property('QVariant', notify=availableMethodsChanged)
    def availableMethods(self):
        """Retourne la liste des méthodes disponibles pour la factory actuelle."""
        return self._methods

    @Property('QVariant', notify=parameterErrorChanged)
    def parameterErrors(self):
        """Retourne les erreurs de validation pour chaque paramètre."""
        return self._parameterErrors


    @Property('QVariant', notify=parametersNamesChanged)
    def parameterNames(self):
        """Retourne les noms des paramètres disponibles."""
        return list(self._parameters.keys())

    @Property('QVariant', notify=parametersChanged)
    def parameters(self):
        """Retourne les paramètres sous forme de range {'param': [min, max]}."""
        return self._parameters

    @Property('QVariant', notify=parametersValuesChanged)
    def parameterValues(self):
        """Retourne les noms des paramètres disponibles."""
        return list(self._parameters.values())

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
        self.parametersValuesChanged.emit()
        self.parametersNamesChanged.emit()
        self.availableMethodsChanged.emit()

    @Slot(str)
    def setMethod(self, index):
        """Met à jour la méthode et initialise ses paramètres."""
        if not self._factory or int(index) >= len(self._methods):
            return

        method_name = self._methods[int(index)]
        self._current_method = method_name

        # Récupération du model
        model = self._factory.getModel(method_name)

        self._keys = model.get_parameter_names()
        default_values = model.get_default_ranges()
        self._parameters = {key: default_values[key] for key in self._keys}
        self._parameterErrors = {key: {"min":True,"max":True} for key in self._keys}

        self.methodChanged.emit()
        self.parametersChanged.emit()
        self.parametersValuesChanged.emit()
        self.parametersNamesChanged.emit()

    def safe_convert(self,value):
        """Convertit une chaîne en float si possible, sinon retourne None."""
        try:
            return float(value) if value.strip() else None
        except ValueError:
            return None

    @Slot(str, str, str)
    def updateParameter(self, key, min_value, max_value):
        """Met à jour un paramètre avec min et max en gérant les erreurs dynamiquement."""
        if key in self._parameters:
            # Conversion sécurisée des valeurs
            min_value = self.safe_convert(min_value)
            max_value = self.safe_convert(max_value)
            model = self._factory.getModel(self._current_method)

            # Validation individuelle des valeurs
            min_error = False if model.validate_parameter(key, min_value) == True else True
            max_error = False if model.validate_parameter(key, max_value) == True else True

            if min_error or max_error :
                self._parameterErrors[key] = {
                     "min": min_error,
                     "max": max_error
                }
                self.parameterErrorChanged.emit()
                return

            min_error = True if min_value is None else False
            max_error = True if max_value is None else False

            if min_error or max_error :
                self._parameterErrors[key] = {
                     "min": min_error,
                     "max": max_error
                }
                self.parameterErrorChanged.emit()
                return

            if min_value >= max_value:
                self._parameterErrors[key] = {
                     "min": True,
                     "max": max_error
                }
                self.parameterErrorChanged.emit()
                return

            # Mise à jour du paramètre
            self._parameters[key] = [min_value, max_value]
            # Émission des signaux finaux après mise à jour
            self.parametersChanged.emit()
            self.parametersValuesChanged.emit()
            self._parameterErrors[key] = {
                 "min": False,
                 "max": False
            }
            self.parameterErrorChanged.emit()
