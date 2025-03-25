from PySide6.QtCore import QAbstractTableModel, Qt

class OptimizedTableModel(QAbstractTableModel):
    def __init__(self, data=None):
        super().__init__()
        self._data = data if data else []

    def rowCount(self, parent=None):
        return len(self._data)

    def columnCount(self, parent=None):
        # Ajuster le nombre de colonnes en fonction des données
        return len(self._data[0]) if self._data else 0

    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid():
            return None
        row, col = index.row(), index.column()
        if role == Qt.DisplayRole:
            return str(self._data[row][col])
        return None

    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                # Retourner des en-têtes de colonnes personnalisés si nécessaire
                return f"Column {section + 1}"
            elif orientation == Qt.Vertical:
                return str(section + 1)
        return None

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            row, col = index.row(), index.column()
            self._data[row][col] = value
            self.dataChanged.emit(index, index)  # Informer la vue qu'il y a eu une mise à jour
            return True
        return False

    def insertRows(self, position, rows, parent=None):
        # Insérer des lignes si nécessaire
        self.beginInsertRows(parent, position, position + rows - 1)
        for _ in range(rows):
            self._data.insert(position, [''] * self.columnCount())  # Insertion de lignes vides
        self.endInsertRows()
        return True

    def removeRows(self, position, rows, parent=None):
        # Supprimer des lignes si nécessaire
        self.beginRemoveRows(parent, position, position + rows - 1)
        del self._data[position:position + rows]
        self.endRemoveRows()
        return True

    def updateData(self, new_data):
        # Mettre à jour toute la table en une fois
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

