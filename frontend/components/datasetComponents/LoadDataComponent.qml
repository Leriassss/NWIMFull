import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import ".."
import "../chartsComponents"
import io.qml

Column{

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

    Dialog {
        id: dataErrorsDialog
        title: "Erreurs détectées"
        standardButtons: Dialog.Ok
        modal: true
        width: 400
        height: 300

        property var errors: fileHandler.errors

        ListView {
            id: errorListView
            model: dataErrorsDialog.errors
            anchors.fill: parent
            delegate: Item {
                width: errorListView.width
                height: 20
                Rectangle {
                    width: parent.width
                    height: parent.height
                    //color: "lightgray"
                    border.color: "gray"
                    Text {
                        anchors.left: parent.left
                        anchors.verticalCenter: parent.verticalCenter
                        padding: 5
                        text: modelData
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }
    }

    function cleanFilePath(filePath) {
        if (filePath.startsWith("file:///")) {
            return filePath.substring(8);
        }
        return filePath;
    }

    function populateTable(columnMapping) {
        tableModel.clear();

        // Trouver la longueur maximale parmi toutes les colonnes
        var maxLength = Math.max(
            columnMapping.Dates ? columnMapping.Dates.length : 0,
            columnMapping.P ? columnMapping.P.length : 0,
            columnMapping.T ? columnMapping.T.length : 0,
            columnMapping.Q ? columnMapping.Q.length : 0,
            columnMapping.ETP ? columnMapping.ETP.length : 0
        );

        // Remplir le modèle avec les données
        for (var i = 0; i < maxLength; i++) {
            tableModel.appendRow({
                Dates: columnMapping.Dates && i < columnMapping.Dates.length ? columnMapping.Dates[i] : "",
                P: columnMapping.P && i < columnMapping.P.length ? columnMapping.P[i] : "",
                T: columnMapping.T && i < columnMapping.T.length ? columnMapping.T[i] : "",
                Q: columnMapping.Q && i < columnMapping.Q.length ? columnMapping.Q[i] : "",
                ETP: columnMapping.ETP && i < columnMapping.ETP.length ? columnMapping.ETP[i] : ""
            });
        }
    }

    Dialog {
            id: columnMappingDialog
            title: "Mapping des colonnes"
            modal: true
            width: 600
            height: 400
            standardButtons: Dialog.Ok | Dialog.Cancel

            property var headers: fileHandler.headers // En-têtes du fichier chargé

            onAccepted: {
                columnMapping = {
                    "Dates":datesComboBox.currentText ,
                    "P": pComboBox.currentText,
                    "T": tComboBox.currentText,
                    "Q": qComboBox.currentText,
                    "ETP": etpComboBox.currentText
                }
                fileHandler.setDictValues(columnMapping)

                if(fileHandler.errors.length !==0){

                    dataErrorsDialog.open()
                }
                else{
                    populateTable(fileHandler.dataDict)
                    tempChart.updateChart()
                    qchart.updateChart()
                    rainChart.updateChart()
                    etpChart.updateChart()
                    columnMappingDialog.close()
                }

            }

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
                height: parent.height * 0.1
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
                height: parent.height * 0.9 - 5
                border.width: 1

                HorizontalHeaderView {
                    id: horizontalHeader
                    anchors.left: tableView.left
                    anchors.top: parent.top
                    syncView: tableView
                    model: [ "Dates","P","T", "Q", "ETP"]
                    clip: true


                }

                VerticalHeaderView {
                    id: verticalHeader
                    anchors.top: tableView.top
                    anchors.left: parent.left
                    syncView: tableView
                    clip: true
                }

                TableView {
                    id: tableView
                    width: parent.width
                    height: parent.height
                    anchors.left: verticalHeader.right
                    anchors.top: horizontalHeader.bottom
                    anchors.right: parent.right
                    anchors.bottom: parent.bottom
                    clip: true

                    columnSpacing: 0
                    rowSpacing: 0

                    model: TableModel {
                        id: tableModel
                        TableModelColumn { display: "Dates" }
                        TableModelColumn { display: "P" }
                        TableModelColumn { display: "T" }
                        TableModelColumn { display: "Q" }
                        TableModelColumn { display: "ETP" }
                        rows: [
                                { Dates: "", P: "", T: "", Q: "", ETP: "" },
                                { Dates: "", P: "", T: "", Q: "", ETP: "" },
                                { Dates: "", P: "", T: "", Q: "", ETP: "" },
                                { Dates: "", P: "", T: "", Q: "", ETP: "" },
                                { Dates: "", P: "", T: "", Q: "", ETP: "" },
                                { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            ]
                    }

                    delegate: Item {
                        implicitWidth: 70
                        implicitHeight: 20

                        Rectangle {
                            anchors.fill: parent
                            border.width: 0.5
                            color: "#fafafa"

                            Text {
                                anchors.centerIn: parent
                                text: model.display
                                font.pixelSize: 10
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
                border.width: 1

                Column {
                    width: parent.width
                    height: parent.height

                    Rectangle {
                        id: plotOptions
                        width: parent.width
                        height: parent.height * 0.1
                        border.width: 1

                        Row {
                            width: parent.width
                            height: parent.height
                            spacing: 0

                            Rectangle {
                                width: parent.width * 0.5
                                height: parent.height
                                border.width: 1
                                Text {
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "CALIBRATION TIME"
                                }
                            }

                            Rectangle {
                                width: parent.width * 0.5
                                height: parent.height
                                border.width: 1
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

                    Rectangle {
                        id: plot
                        width: parent.width-10
                        height: parent.height * 0.85
                        //anchors.centerIn: parent
                        border.width: 1
                        Column{
                            anchors.fill: parent

                            Grid {
                                id: grid
                                anchors.fill: parent
                                columns: 2
                                rowSpacing: 1
                                columnSpacing: 1
                                QobsChart{
                                    id : qchart
                                    width: parent.width / 2
                                    height: parent.height / 2
                                }
                                TempChart{
                                    id : tempChart
                                    width: parent.width / 2
                                    height: parent.height / 2
                                }
                                ETPChart{
                                    id : etpChart
                                    width: parent.width / 2
                                    height: parent.height / 2
                                }
                                RainChart{
                                    id : rainChart
                                    width: parent.width / 2
                                    height: parent.height / 2
                                }
                            }

                        }


                    }
                }
            }
        }
    }

}
