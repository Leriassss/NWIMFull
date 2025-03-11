import QtQuick
import QtQuick.Controls
import Qt.labs.platform

Item {
    id: fileChoose

    signal fileSelected(string filePath)
    property string fileName: ""
    FileDialog {
        id: fileDialog
        title: "Sélectionnez un fichier"
        fileMode: FileDialog.OpenFile
        nameFilters: ["Texte (*.txt)"]

        onAccepted: {
            fileChoose.fileSelected(fileDialog.file)
            console.log("Fichier sélectionné: " + fileDialog.file)
            fileName = fileDialog.file
        }

        onRejected: {
            console.log("Sélection annulée")
        }
    }

    function openDialog() {
        fileDialog.open()
    }
}
