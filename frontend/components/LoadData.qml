import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import "."
import io.qml

Dialog {
    id: loadDataDialog
    title: "IMPORTATION"
    modal: true
    width: 1300
    height: 700
    standardButtons: Dialog.Ok | Dialog.Cancel
    padding: 5

    property var fileData: null
    property var columnMapping: ({})

    FileChoose {
        id: fileChooseComponent
        property string fileName: ""

        onAccepted: {
            fileName = cleanFilePath(fileChooseComponent.file.toString());
            if (fileName) {
                try {
                    fileHandler.readFile(fileName)
                    var headers = fileHandler.headers
                    columnMappingDialog.headers = headers
                    columnMappingDialog.open()
                } catch (error) {
                    errorDialog.text = "Erreur lors du chargement du fichier : " + error
                    errorDialog.open()
                }
            }
        }
        onRejected: {
            console.log("Sélection annulée");
        }

    }

    Dialog {
        id: errorDialog
        title: "Erreur"
        standardButtons: Dialog.Ok
        property string text: ""
        Label {
            text: errorDialog.text
        }
    }

    function cleanFilePath(filePath) {
        if (filePath.startsWith("file:///")) {
            return filePath.substring(8);
        }
        return filePath;
    }

    Dialog {
        id: columnMappingDialog
        title: "Mapping des colonnes"
        modal: true
        width: 600
        height: 400
        standardButtons: Dialog.Ok | Dialog.Cancel

        property var headers: fileHandler.headers // En-têtes du fichier chargé

        GridLayout {
            height: parent.height
            width: parent.width * 0.5
            columns: 2 // Deux colonnes : une pour les labels, une pour les ComboBox
            columnSpacing: 10
            rowSpacing: 10

            // Ligne pour Dates
            Label {
                text: "Dates"
                Layout.alignment: Qt.AlignRight
            }
            ComboBox {
                id: datesComboBox
                model: columnMappingDialog.headers
                currentIndex: 0
                Layout.fillWidth: true
            }

            // Ligne pour P
            Label {
                text: "P"
                Layout.alignment: Qt.AlignRight
            }
            ComboBox {
                id: pComboBox
                model: columnMappingDialog.headers
                currentIndex: 0
                Layout.fillWidth: true
            }

            // Ligne pour T
            Label {
                text: "T"
                Layout.alignment: Qt.AlignRight
            }
            ComboBox {
                id: tComboBox
                model: columnMappingDialog.headers
                currentIndex: 0
                Layout.fillWidth: true
            }

            // Ligne pour Q
            Label {
                text: "Q"
                Layout.alignment: Qt.AlignRight
            }
            ComboBox {
                id: qComboBox
                model: columnMappingDialog.headers
                currentIndex: 0
                Layout.fillWidth: true
            }

            // Ligne pour ETP
            Label {
                text: "ETP"
                Layout.alignment: Qt.AlignRight
            }
            ComboBox {
                id: etpComboBox
                model: columnMappingDialog.headers
                currentIndex: 0
                Layout.fillWidth: true
            }

            // Bouton Valider
            Button {
                text: "Valider"
                Layout.columnSpan: 2 // Le bouton occupe deux colonnes
                Layout.alignment: Qt.AlignRight
                onClicked: {
                    // Enregistrer le mapping des colonnes
                    columnMapping = {
                        "Dates":datesComboBox.currentText === "Aucun" ? [] : fileHandler.data[datesComboBox.currentText],
                        "P": pComboBox.currentText === "Aucun" ? [] : fileHandler.data[pComboBox.currentText],
                        "T": tComboBox.currentText === "Aucun" ? [] : fileHandler.data[tComboBox.currentText],
                        "Q": qComboBox.currentText === "Aucun" ? [] : fileHandler.data[qComboBox.currentText],
                        "ETP": etpComboBox.currentText === "Aucun" ? [] : fileHandler.data[etpComboBox.currentText]
                    }
                    fileHandler.setDictValues(columnMapping)
                    // Mettre à jour le modèle ListView avec les données
                    listviewdata.model.clear()
                    for (var i = 0; i < columnMapping.Dates.length; i++) {
                        listviewdata.model.append({
                            date: columnMapping.Dates[i],
                            etp: columnMapping.ETP[i],
                            p: columnMapping.P[i],
                            q: columnMapping.Q[i],
                            t: columnMapping.T[i]
                        })
                    }

                    columnMappingDialog.close()
                }
            }
        }
    }

    Row {
        anchors.fill: parent
        spacing: 5
        padding: -5

        Column {
            width: parent.width * 0.3
            height: parent.height
            spacing: 5

            Row {
                width: parent.width
                height: parent.height * 0.2
                spacing: 0

                Label {
                    text: "Location : "
                    anchors.verticalCenter: fileLocation.verticalCenter
                    padding: 5
                    anchors.rightMargin: 5
                }

                TextField {
                    id: fileLocation
                    width: parent.width * 0.6
                    height: 30
                    text: fileChooseComponent.fileName
                }

                Button {
                    width: parent.width * 0.2
                    text: "Browse"
                    height: 30

                    onClicked: {
                        fileChooseComponent.open()
                    }
                }
            }
            Rectangle{
                width: parent.width
                height: parent.height * 0.8
                border.width: 2
                ListView {
                    id: listviewdata
                    width: parent.width
                    height: parent.height
                    model: ListModel {}

                    delegate: Item {
                        width: parent.width
                        height: 50

                        Rectangle {
                            width: parent.width
                            height: 50
                            border.color: "blue"
                            border.width: 1

                            Row {
                                anchors.fill: parent
                                anchors.margins: 5
                                spacing: 10

                                // Colonne Date
                                Rectangle {
                                    width: parent.width * 0.2
                                    height: parent.height
                                    color: "lightblue"
                                    border.color: "blue"
                                    border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: model.date
                                        font.pixelSize: 14
                                    }
                                }

                                // Colonne ETP
                                Rectangle {
                                    width: parent.width * 0.2
                                    height: parent.height
                                    color: "lightblue"
                                    border.color: "blue"
                                    border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: model.etp
                                        font.pixelSize: 14
                                    }
                                }

                                // Colonne P
                                Rectangle {
                                    width: parent.width * 0.2
                                    height: parent.height
                                    color: "lightblue"
                                    border.color: "blue"
                                    border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: model.p
                                        font.pixelSize: 14
                                    }
                                }

                                // Colonne Q
                                Rectangle {
                                    width: parent.width * 0.2
                                    height: parent.height
                                    color: "lightblue"
                                    border.color: "blue"
                                    border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: model.q
                                        font.pixelSize: 14
                                    }
                                }

                                // Colonne T
                                Rectangle {
                                    width: parent.width * 0.2
                                    height: parent.height
                                    color: "lightblue"
                                    border.color: "blue"
                                    border.width: 1
                                    Text {
                                        anchors.centerIn: parent
                                        text: model.t
                                        font.pixelSize: 14
                                    }
                                }
                            }
                        }
                    }
                }

            }


        }

        Column {
            width: parent.width * 0.7
            height: parent.height
            spacing: 5

            Rectangle {
                id: simulationPane
                width: parent.width
                height: parent.height
                border.width: 2

                Column {
                    width: parent.width
                    height: parent.height

                    Rectangle {
                        id: plotOptions
                        width: parent.width
                        height: parent.height * 0.15
                        border.width: 2

                        Row {
                            width: parent.width
                            height: parent.height
                            spacing: 6

                            Rectangle {
                                width: parent.width * 0.5
                                height: parent.height
                                border.width: 2
                                Text {
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "CALIBRATION"
                                }
                            }

                            Rectangle {
                                border.width: 2
                                anchors.margins: 20
                                width: parent.width * 0.5 - 6
                                height: parent.height
                                Text {
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "PLOT"
                                }

                                Row {
                                    spacing: 6
                                    width: parent.width
                                    height: parent.height

                                    Rectangle {
                                        width: parent.width * 0.5
                                        height: parent.height * 0.7
                                        anchors.bottom: parent.bottom
                                        border.width: 2
                                        Text {
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            text: "PARAMETERS"
                                        }

                                        Row {
                                            anchors.centerIn: parent
                                            width: parent.width
                                            spacing: 5
                                            leftPadding: 10

                                            CheckBox {
                                                checked: true
                                                text: "ETP"
                                            }

                                            CheckBox {
                                                text: "P"
                                            }

                                            CheckBox {
                                                text: "T"
                                            }

                                            CheckBox {
                                                text: "Q"
                                            }
                                        }
                                    }

                                    Rectangle {
                                        width: parent.width * 0.5 - 6
                                        height: parent.height * 0.7
                                        border.width: 2
                                        anchors.bottom: parent.bottom
                                        Text {
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            text: "PERIOD"
                                        }

                                        Row {
                                            leftPadding: 10
                                            anchors.centerIn: parent
                                            width: parent.width

                                            CheckBox {
                                                checked: true
                                                text: "CALIBRATION"
                                                rightPadding: 5
                                            }

                                            CheckBox {
                                                text: "VALIDATION"
                                            }
                                        }
                                    }
                                }
                            }
                        }
                    }

                    Rectangle {
                        id: plot
                        width: parent.width
                        height: parent.height * 0.85
                        border.width: 2

                        Rectangle {
                            width: parent.width
                            height: 25
                            border.width: 1
                            anchors.top: parent.top

                            Row {
                                spacing: 20
                                anchors.fill: parent
                                padding: 5

                                Label {
                                    leftPadding: 10
                                    rightPadding: 10
                                    text: "STATISTICS"
                                }

                                Row {
                                    width: parent.width * 0.8
                                    height: parent.height
                                    spacing: 25

                                    Label {
                                        text: "Min :     "
                                        verticalAlignment: Text.AlignVCenter
                                    }

                                    Label {
                                        text: "Max :    "
                                        verticalAlignment: Text.AlignVCenter
                                    }

                                    Label {
                                        text: "Sum:     "
                                        verticalAlignment: Text.AlignVCenter
                                    }

                                    Label {
                                        text: "Mean :    "
                                        verticalAlignment: Text.AlignVCenter
                                    }

                                    Label {
                                        text: "SD :    "
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
