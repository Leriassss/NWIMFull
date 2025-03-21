from PySide6.QtCore import QAbstractTableModel, Qt, Slot, Signal, QVariant

class TableModel(QAbstractTableModel):
    dataChanged = Signal()  # Signal pour informer QML que les données ont changé

    def __init__(self, data=None):
        super().__init__()
        self._data = data or {}

    def rowCount(self, parent=None):
        """Retourne le nombre de lignes (longueur des listes)"""
        if self._data:
            return max(len(v) for v in self._data.values())  # Trouver la liste la plus longue
        return 0

    def columnCount(self, parent=None):
        """Retourne le nombre de colonnes (nombre de clés du dictionnaire)"""
        return len(self._data.keys()) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        """Retourne la valeur de la cellule"""
        if not index.isValid() or role != Qt.DisplayRole:
            return QVariant()

        column = list(self._data.keys())[index.column()]  # Obtenir le nom de la colonne
        row = index.row()

        # Vérifier si la ligne existe dans la liste
        if row < len(self._data[column]):
            return self._data[column][row]
        return QVariant()  # Valeur vide si la liste est plus courte

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        """Gère les noms des colonnes"""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return list(self._data.keys())[section]
        return QVariant()

    @Slot("QVariantMap")
    def setData(self, data_dict):
        """Mise à jour des données et notification à QML"""
        self.beginResetModel()
        self._data = data_dict
        self.endResetModel()
        self.dataChanged.emit()
