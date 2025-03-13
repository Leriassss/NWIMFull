from PySide6.QtQml import QmlElement
from PySide6.QtCore import QObject, Property, Signal, Slot
from api.FactoryManager import FactoryManager
import math

QML_IMPORT_NAME = "io.qml"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class GridParametersQML(QObject):
    parametersChanged = Signal()
    methodChanged = Signal()
    parameterErrorChanged = Signal()

    def __init__(self, parent=None):
        """Initialisation sans écoute du changement de factory."""
        super().__init__(parent)
        self._factory = None
        self._current_method = None
        self._parameters = {}
        self._methods = []
        self._parameterErrors = {}
        print("----------------------*-*-*-")

    @Property('QVariant', notify=methodChanged)
    def availableMethods(self):
        """Retourne la liste des méthodes disponibles pour la factory actuelle."""
        return self._methods

    @Property('QVariant', notify=parametersChanged)
    def parameterNames(self):
        """Retourne les noms des paramètres disponibles."""
        return list(self._parameters.keys())

    @Property('QVariant', notify=parametersChanged)
    def parameters(self):
        """Retourne les paramètres sous forme de range {'param': [min, max]}."""
        return self._parameters

    @Property('QVariant', notify=parameterErrorChanged)
    def parameterErrors(self):
        """Retourne les erreurs de validation pour chaque paramètre."""
        return self._parameterErrors

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
    def setMethod(self, method_name):
        """Met à jour la méthode et initialise ses paramètres."""

        if not self._factory or method_name not in self._methods:
            return

        self._current_method = method_name

        # Récupération des valeurs par défaut
        default_values = self._factory.getModelParameters(method_name)
        self._parameters = {key: [None,None] for key in default_values}

        self.methodChanged.emit()
        self.parametersChanged.emit()


    @Slot(str, float, float)
    def updateParameter(self, key, min_value, max_value):
        """Met à jour un paramètre avec min et max en s'assurant que min < max et en gérant les valeurs vides."""

            # Remplacement des NaN par None
        min_value = None if math.isnan(min_value) else min_value
        max_value = None if math.isnan(max_value) else max_value

            # Initialisation des erreurs
        error_min, error_max = "", ""

        if key in self._parameters:
                # Vérification que min < max
            if min_value is not None and max_value is not None and min_value >= max_value:
                error_min = "La valeur minimale doit être strictement inférieure à la valeur maximale."
            else:
                model = self._factory.getModel(self._current_method)

                    # Validation individuelle des valeurs
                error_min = "Champ obligatoire" if min_value is None else model.validate_parameter(key, min_value)
                error_max = "Champ obligatoire" if max_value is None else model.validate_parameter(key, max_value)

                    # Mise à jour des paramètres
                self._parameters[key] = [min_value, max_value]

                # Stockage des erreurs (affichage en rouge si nécessaire)
            self._parameterErrors[key] = {
                "min": error_min if error_min is not True else "",
                "max": error_max if error_max is not True else ""
            }

                # Émission des signaux de mise à jour
            self.parametersChanged.emit()
            self.parameterErrorChanged.emit()
