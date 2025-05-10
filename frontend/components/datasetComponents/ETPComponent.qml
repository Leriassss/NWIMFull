import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import ".."
import "../chartsComponents"
import io.qml



Column{
    clip: true

    property var fileData: null
    property var columnMapping: ({})
    Connections {
        target: fileHandler
        function onEtpInfosChanged() {
            populateTable({"CDates" : fileHandler.datesInfos["data_cal"],
                           "Calibration" : fileHandler.etpInfos["data_cal"],
                            "VDates" : fileHandler.datesInfos["data_val"],
                            "Validation" : fileHandler.etpInfos["data_val"]
                          })
            /*console.log("--------------ETPCOMPONENT")
            console.log(JSON.stringify(fileHandler.datesInfos))
            console.log(JSON.stringify(fileHandler.etpInfos))*/
            etpCalibrationChart.updateChart(fileHandler.datesInfos["data_cal"],fileHandler.etpInfos["data_cal"])
            etpValidationChart.updateChart(fileHandler.datesInfos["data_val"],fileHandler.etpInfos["data_val"])
        }
    }

    function populateTable(columnMapping) {
        tableModel.clear();
        const mykeys = ["CDates","Calibration","VDates","Validation"];

        // Trouver la longueur maximale en une seule passe
        const maxLength = mykeys.reduce((max, key) => Math.max(max, columnMapping[key]?.length || 0), 0);
        // Remplir le modèle de données
        for (let i = 0; i < maxLength; i++) {
            let rowData = {};
            mykeys.forEach(key => rowData[key] = columnMapping[key]?.[i] ?? "");
            tableModel.appendRow(rowData);
        }
    }
    FileChoose {
        id: fileChooseComponent
        property string fileName: ""

        onAccepted: {
            fileName = cleanFilePath(fileChooseComponent.file.toString());
            if (fileName) {
                try {
                    etoManager.readFile(fileName)
                    var headers = etoManager.headers
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
        title: "❌ ERREURS DETECTEES !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)

        property var errors: etoManager.errors

        Rectangle{
            anchors.fill: parent
            border.width: 1
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
    }
    function cleanFilePath(filePath) {
        if (filePath.startsWith("file:///")) {
            return filePath.substring(8);
        }
        return filePath;
    }

    Dialog {
        id: columnMappingDialog
        title: "MAPPING"
        implicitWidth:  800
        implicitHeight: 450
        modal: true
        popupType: Popup.Window
        //topInset : 5
        standardButtons: Dialog.Ok | Dialog.Cancel
        closePolicy : Popup.CloseOnEscape
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)

            property var headers: etoManager.headers // En-têtes du fichier chargé

            onAccepted: {
                columnMapping = {
                    "dates" : datesComboBox.currentText,
                    "tmean":tMeanComboBox.currentText,
                    "tmin" : tMinComboBox.currentText,
                    "tmax" : tMaxComboBox.currentText,
                    "rh" : rhComboBox.currentText,
                    "rn" : rsComboBox.currentText,
                    "wind" : u2ComboBox.currentText,
                    "lat" : lat.text,
                    "elevation" : elevation.text
                }
                etoManager.setDictValues(columnMapping)

                if(etoManager.errors.length !==0){

                    dataErrorsDialog.open()
                }
                else{
                    try {
                        etoManager.computeETo()

                    } catch (error) {
                        errorDialog.text = "Les paramètres requis n'ont pas étét fournis "
                        errorDialog.open()
                    }
                    populateTable({"CDates" : fileHandler.datesInfos["data_cal"],
                                   "Calibration" : fileHandler.etpInfos["data_cal"],
                                    "VDates" : fileHandler.datesInfos["data_val"],
                                    "Validation" : fileHandler.etpInfos["data_val"]
                                  })
                    etpCalibrationChart.updateChart(fileHandler.datesInfos["data_cal"],fileHandler.etpInfos["data_cal"])
                    etpValidationChart.updateChart(fileHandler.datesInfos["data_val"],fileHandler.etpInfos["data_val"])
                }

            }
            RowLayout{
                anchors.fill: parent
                spacing: 10

                GridLayout {
                    Layout.preferredHeight:  parent.height
                    Layout.preferredWidth:  parent.width * 0.5
                    columns: 2
                    columnSpacing: 10
                    rowSpacing: 10

                    Label {
                        text: "Dates"
                        Layout.alignment: Qt.AlignLeft
                    }
                    ComboBox {
                        id: datesComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }

                    Label {
                        text: "Teméprature Moy. [°C]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    ComboBox {
                        id: tMeanComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }

                    // Ligne pour Dates
                    Label {
                        text: "Température Min. [°C]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    ComboBox {
                        id: tMinComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }
                    // Ligne pour Dates
                    Label {
                        text: "Température Max. [°C]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    ComboBox {
                        id: tMaxComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }
                    Label {
                        text: "Humidité relative de l'air [%]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    ComboBox {
                        id: rhComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }

                    Label {
                        text: "Rad. Solaire/ \nRad. Net/\nNb Heures d'Enso."
                        Layout.alignment: Qt.AlignLeft
                        Layout.preferredWidth: 100
                        wrapMode: Text.Wrap
                    }
                    ComboBox {
                        id: rsComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }

                    Label {
                        text: "Vitesse moy. [m/s]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    ComboBox {
                        id: u2ComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }

                    // Ligne pour ETP
                    Label {
                        text: "Latitude [rad]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    TextField {
                        id: lat
                        text : "5"
                        Layout.fillWidth: true
                        validator: DoubleValidator {
                            bottom: 0
                            notation: DoubleValidator.StandardNotation
                        }
                    }
                    Label {
                        text: "Altitude [m]"
                        Layout.alignment: Qt.AlignLeft
                    }
                    TextField {
                        id: elevation
                        Layout.fillWidth: true
                        text : "150"
                        validator: DoubleValidator {
                            bottom: 0
                            notation: DoubleValidator.StandardNotation
                        }
                    }
                }

                Rectangle {
                    width: 1  // Épaisseur de la barre
                    height: parent.height * 0.9
                    color: "gray"  // Couleur de la barre
                }

                ColumnLayout{
                    Layout.preferredHeight:  100
                    Layout.preferredWidth:  parent.width * 0.5

                    ComboBox {
                        leftPadding: 10
                        Layout.preferredWidth:  150
                        Layout.preferredHeight: 40
                        id: methodSelector
                        model: etoManager.availableMethods
                        onCurrentTextChanged: {
                            etoManager.setMethod(methodSelector.currentText)
                        }
                        Component.onCompleted: {
                            etoManager.setMethod(methodSelector.currentText)
                        }
                    }
                    Label{
                        id : requiredParams
                        text : "PARAMETRES REQUIS : " + etoManager.methodParameters
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        wrapMode: Text.Wrap
                        font.bold: true


                    }
                }
            }

    }




    Row {
        anchors.fill: parent
        spacing: 5
        padding: 5

        Column {
            width: parent.width * 0.3 - parent.spacing
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
                height: parent.height * 0.6 -parent.spacing
                //border.width: 1
                color : "transparent"

                HorizontalHeaderView {
                    id: horizontalHeader
                    anchors.left: tableView.left
                    anchors.top: parent.top
                    syncView: tableView
                    model: [ "Dates","ETP Calibration","Dates","ETP Validation"]
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
                        TableModelColumn { display: "CDates" }
                        TableModelColumn { display: "Calibration" }
                        TableModelColumn { display: "VDates" }
                        TableModelColumn { display: "Validation" }
                        rows: [
                                { CDates : "", Calibration: "", VDates : "", Validation : ""},
                                { CDates : "", Calibration: "", VDates : "", Validation : ""},
                                { CDates : "", Calibration: "", VDates : "", Validation : ""},
                                { CDates : "", Calibration: "", VDates : "", Validation : ""}
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
                                wrapMode: Text.WordWrap
                                horizontalAlignment: Text.AlignHCenter
                            }
                        }
                    }
                }

            }


        }

        Column {
            width: parent.width * 0.7 - parent.spacing
            height: parent.height
            spacing: 5

            Rectangle {
                id: simulationPane
                width: parent.width
                height: parent.height
                border.width: 1

                Column {
                    anchors.fill: parent
                    Rectangle {
                        id: plotOptions
                        width: parent.width
                        height: parent.height * 0.2
                        border.width: 1

                        Column{
                            anchors.fill: parent
                            spacing: 5
                            StatisticsComponent{
                                spacing: 20
                                width: parent.width
                                height: parent.height *0.3
                                padding: 5
                                statistics: {
                                    "min" : fileHandler.etpInfos["min_cal"],
                                    "max" : fileHandler.etpInfos["max_cal"],
                                    "mean" : fileHandler.etpInfos["mean_cal"],
                                    "sum" : fileHandler.etpInfos["sum_cal"],
                                    "std" : fileHandler.etpInfos["std_cal"]
                                }
                                periodLabel : "CALIBRATION"
                            }
                            StatisticsComponent{
                                spacing: 20
                                width: parent.width
                                height: parent.height *0.3
                                padding: 5
                                statistics: {
                                    "min" : fileHandler.etpInfos["min_val"],
                                    "max" : fileHandler.etpInfos["max_val"],
                                    "mean" : fileHandler.etpInfos["mean_val"],
                                    "sum" : fileHandler.etpInfos["sum_val"],
                                    "std" : fileHandler.etpInfos["std_val"]
                                }
                                periodLabel : "VALIDATION"
                            }
                            StatisticsComponent{
                                spacing: 20
                                width: parent.width
                                height: parent.height *0.3
                                padding: 5
                                statistics: {
                                    "min" : fileHandler.etpInfos["min"],
                                    "max" : fileHandler.etpInfos["max"],
                                    "mean" : fileHandler.etpInfos["mean"],
                                    "sum" : fileHandler.etpInfos["sum"],
                                    "std" : fileHandler.etpInfos["std"]
                                }
                                periodLabel : "SERIES"
                            }
                        }
                    }


                    Rectangle {
                        id: plot
                        width: parent.width
                        height: parent.height * 0.8
                        //anchors.centerIn: parent
                        border.width: 1
                        clip: true
                        GridLayout {
                            id: grid
                            anchors.fill: parent
                            anchors.centerIn: parent

                            columns: 2
                            rowSpacing: 0
                            columnSpacing: 0

                            ETPChart{
                                id : etpCalibrationChart
                                Layout.preferredWidth: parent.width / 2
                                Layout.preferredHeight:parent.height
                                chartName : "ETP Calibration"

                            }
                            ETPChart{
                                id : etpValidationChart
                                Layout.preferredWidth: parent.width / 2
                                Layout.preferredHeight:parent.height
                                chartName : "ETP Validation"
                            }

                        }


                    }
                }
            }
        }
    }

}
