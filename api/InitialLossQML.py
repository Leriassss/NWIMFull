from PySide6.QtCore import QObject, Property, Signal, Slot
from backend.factory.InitialLossFactory import InitialLossFactory

class InitialLossQML(QObject):
    parametersChanged = Signal()
    methodChanged = Signal()
    parameterErrorChanged = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self._current_method = None
        self._parameters = {}
        self._methods = InitialLossFactory.getMethodKeys()
        self._parameterErrors = {}

    @Property(str, notify=methodChanged)
    def currentMethod(self):
        """Retourne la méthode actuelle."""
        return self._current_method or ""

    @Property('QVariant', notify=parametersChanged)
    def parameterNames(self):
        """Retourne les noms des paramètres du modèle sélectionné."""
        if self._current_method:
            return InitialLossFactory.getModelParameters(self._current_method)
        return {}

    @Property('QVariant', notify=parametersChanged)
    def parameters(self):
        """Retourne les paramètres actuels."""
        return self._parameters

    @Property('QVariant', constant=True)
    def availableMethods(self):
        """Retourne la liste des méthodes disponibles pour le ComboBox en QML."""
        return self._methods

    @Slot(str)
    def setMethod(self, index):
        """Met à jour la méthode et initialise ses paramètres par défaut."""
        method_name = self._methods[int(index)]
        if method_name in InitialLossFactory.methods:
            self._current_method = method_name
            self._parameters = {key: None for key in InitialLossFactory.getModelParameters(method_name)}
            self.methodChanged.emit()
            self.parametersChanged.emit()

    @Slot(str, str)
    def updateParameter(self, key, value):
        """Met à jour un paramètre et applique la validation."""
        self._parameters[key] = value
        model = InitialLossFactory.getModel(self._current_method)
        validation_result = model.validate_parameter(key, value)

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
