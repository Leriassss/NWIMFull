from PySide6.QtCore import QObject, Property, Signal, Slot
from PySide6.QtQml import QmlElement
#from api.FactoryManager import FactoryManager

"""
QML_IMPORT_NAME = "io.qmlv"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
"""
class ParametersQML(QObject):
    textChanged = Signal()  # Signal pour informer QML des changements
    labelChanged = Signal() # Signal pour mettre à jour le label

    def __init__(self, parent=None):
        super().__init__(parent)
        self._text = "Texte initial"
        self._label = "Label par défaut"

    @Property(str, notify=textChanged)
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        if self._text != value:
            self._text = value
            self.textChanged.emit()

    @Property(str, notify=labelChanged)
    def label(self):
        return self._label

    @label.setter
    def label(self, value):
        if self._label != value:
            self._label = value
            self.labelChanged.emit()

    @Slot(str)
    def updateText(self, newText):
        """Met à jour le texte et émet le signal de changement"""
        self.text = newText


