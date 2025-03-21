import pandas as pd
from PySide6.QtCore import QObject, Signal, Slot, Property
from PySide6.QtQml import QmlElement

class FileHandler(QObject):
    def __init__(self):
        super().__init__()
        self._headers = []
        self._data = []
        self._data_dict = {}

    # Signal pour envoyer les en-têtes de colonnes à QML
    headersChanged = Signal(list)

    # Signal pour envoyer les données à QML
    dataChanged = Signal(list)

    bundleChanged = Signal()

    # Propriété pour les en-têtes
    @Property(list, notify=headersChanged)
    def headers(self):

        return self._headers

    # Propriété pour les données
    @Property(dict, notify=dataChanged)
    def data(self):
        return self._data

    @Slot(str)
    def readFile(self, filePath):
        try:
            if filePath.endswith('.csv'):
                df = pd.read_csv(filePath)
            elif filePath.endswith('.xlsx'):
                df = pd.read_excel(filePath, engine='openpyxl')
            else:
                print("Format de fichier non supporté")
                return

            # Extraire les en-têtes et les données
            hd = df.columns.tolist()
            hd.append("Aucun")
            self._headers =hd
            self._data = df.to_dict(orient="list")
            # Émettre les signaux pour mettre à jour QML
            self.headersChanged.emit(self._headers)
            self.dataChanged.emit(self._data)

        except Exception as e:
            print(f"Erreur lors de la lecture du fichier : {e}")

    @Slot(str)
    def getColumn(self, index):
        print(self._data[index])
        return self._data[index]

    @Slot('QVariant')
    def setDictValues(self, data_dict):
        print(data_dict.toVariant() )
        self._data_dict = data_dict.toVariant()


        self.bundleChanged.emit()

