import QtQuick
import QtQuick.Controls
import Qt.labs.platform


    FileDialog {
        title: "Sélectionnez un fichier"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Excel (*.xlsx)","Texte (*.txt)"]

    }

