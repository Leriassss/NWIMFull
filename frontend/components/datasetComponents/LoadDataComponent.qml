import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import ".."
import "../chartsComponents"
import "../customComponents"
import io.qml
import QtQuick.Effects
import Qt5Compat.GraphicalEffects
Rectangle{
    clip: true
    border.width: 1
    border.color: "#ebebeb"

    property var fileData: null
    property var columnMapping: ({})

    FileChoose {
        id: fileChooseComponent
        nameFilters: ["Excel (*.xlsx)","Texte (*.txt)"]
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
        title: "Errors"
        standardButtons: Dialog.Ok
        property string errorText: ""
        Label {
            text: errorDialog.errorText
        }
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        modal: true
        background: Rectangle{
            anchors.fill:parent
            border.color: "red"
            color: "#f0f0f0"
            border.width: 1
        }
    }
    CalendarDialog{
        id : chooseDatePopup
        width: 350
        height: 250
        standardButtons: Dialog.Ok | Dialog.Cancel
        title: qsTr("CHOOSE PERIODS BEGININS")
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        /*calibration_dates : {
            console.log("-*-*-*--*-*-* CALIBRATION LENGTH -*-*-*-*-*-*-*-*-*")
            console.log(JSON.stringify(fileHandler.calendar_dates))
            fileHandler.calendar_dates
        }*/

        onAccepted: {
            console.log("-*-*-*--*-*-* CALIBRATION LENGTH -*-*-*-*-*-*-*-*-*")
            console.log(JSON.stringify(chooseDatePopup.user_calibration))
            fileHandler.updateCalibrationAndValibationDates(chooseDatePopup.user_calibration)

            if(fileHandler.errors.length !==0){

                dataErrorsDialog.open()
            }
        }
    }

    Dialog {
        id: warningDialog
        title: "Warnings"
        standardButtons: Dialog.Ok
        modal: true
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        property string text: ""
        Label {
            text: warningDialog.text
        }
    }

    DataErrorsDialog {
        id: dataErrorsDialog
        title: "❌ ERREURS DETECTEES !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
        errors: fileHandler.errors

    }


    Dialog {
            id: columnMappingDialog
            title: "MAPPING"
            implicitWidth:  350
            implicitHeight: 300
            modal: true
            standardButtons: Dialog.Ok | Dialog.Cancel
            closePolicy : Popup.CloseOnEscape
            x: Math.round((parent.width - width) / 2)
            y: Math.round((parent.height - height) / 2)


            property var headers: fileHandler.headers // En-têtes du fichier chargé

            property var calib_dates : fileHandler.calendar_dates
            onAccepted: {
                columnMapping = {
                    "Dates":datesComboBox.currentText ,
                    "P": pComboBox.currentText,
                    "Q": qComboBox.currentText,
                    "ETP": etpComboBox.currentText
                }
                console.log("---------------- COLUMN MAPPING ------------------")
                console.log(JSON.stringify(columnMapping))
                /*fileHandler.initDatesValues(datesComboBox.currentText)
                fileHandler.initPValues(pComboBox.currentText)
                fileHandler.initTempValues(tComboBox.currentText)
                fileHandler.initQValues(qComboBox.currentText)
                fileHandler.initETPValues(etpComboBox.currentText)*/

                fileHandler.setDictValues(columnMapping)


                if(fileHandler.errors.length !==0){

                    dataErrorsDialog.open()
                    console.log(JSON.stringify(fileHandler.errors))
                }
                else{
                    let qNaN = fileHandler.dataDict["Q"].some(Number.isNaN)
                    let pNaN = fileHandler.dataDict["P"].some(Number.isNaN)
                    let et0NaN = fileHandler.dataDict["ETP"].some(Number.isNaN)
                    if( qNaN || pNaN ||et0NaN){
                        warningDialog.text = "Missing values detected in : \n" +
                                (qNaN ? "Q Series (Ignored for Prediction) " : "\n") +
                                (pNaN ? "Rainfall Series " : " \n") +
                                (et0NaN ? "PET Series " : " \n")
                        columnMappingDialog.close()
                        warningDialog.open()
                    }

                    populateTable(fileHandler.dataDict)
                    //fileHandler.calibrationTime()

                    /*dataTableModel.setData(fileHandler.dataDict)*/
                    //tableView.appendRow(fileHandler.displayData)
                    //transformData(fileHandler.dataDict)
                    //tempChart.updateChart(data_dates,fileHandler.dataDict["T"])
                    //rainChart.updateChart(data_dates,fileHandler.dataDict["P"])

                    let data_dates = fileHandler.dataDict["Dates"]
                    qchart.updateCombinedChart(data_dates,fileHandler.dataDict["Q"], fileHandler.dataDict["P"])
                    etpChart.updateCombinedChart(data_dates,fileHandler.dataDict["ETP"],fileHandler.dataDict["P"])
                    columnMappingDialog.close()
                    chooseDatePopup.open()

                }


            }

            Rectangle{
                anchors.fill: parent
                border.width: 1
                border.color: "#ebebeb"
                color : "#fcffff"


                GridLayout {
                    height: parent.height
                    width: parent.width * 0.75
                    columns: 2 // Deux colonnes : une pour les labels, une pour les ComboBox
                    columnSpacing: 10
                    rowSpacing: 10


                    // Ligne pour Dates
                    Label {
                        text: "Dates"
                        Layout.alignment: Qt.AlignRight
                        leftPadding: 5
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


    }

    Row {
        anchors.fill: parent
        spacing: 10
        padding: 5
        clip: true

        Rectangle{
            width: parent.width * 0.3
            height: parent.height - parent.padding - parent.spacing
            color: "#bae7fe"
            layer.enabled: true
            layer.effect: DropShadow {
                horizontalOffset: 1
                verticalOffset: 1
                radius: 4
                samples: 10
                color: "#888888"
            }
            Column {
                width: parent.width
                anchors.centerIn: parent
                height: parent.height
                spacing: 10
                padding: 10

                Label {
                    id : chooseText
                    text: qsTr("Choose file")

                    font.bold: true
                }


                Rectangle{
                    width: parent.width - parent.spacing-parent.padding
                    height: parent.height * 0.1
                    color : "#fcffff"
                    radius : 5
                    Row {
                        anchors.fill: parent
                        spacing: 0
                        leftPadding: 10

                        TextField {
                            id: fileLocation
                            width: parent.width * 0.6
                            height: 30
                            text: fileChooseComponent.fileName
                            anchors.verticalCenter: parent.verticalCenter
                            placeholderText: "Location"
                            background: Rectangle{
                                anchors.fill: parent
                                topLeftRadius: 5
                                bottomLeftRadius: 5
                                border.color: "#2e2f30"
                                border.width: 1
                            }
                        }

                        Button {
                            width: 50
                            text: "Browse..."
                            height: 30
                            anchors.verticalCenter: parent.verticalCenter
                            background: Rectangle{
                                anchors.fill: parent
                                color: "#29888b"
                                topRightRadius: 5
                                bottomRightRadius: 5
                            }

                            onClicked: {
                                fileChooseComponent.open()
                            }
                        }
                    }

                }


                Label {
                    id : periodLength
                    text: qsTr("Periods length")

                    font.bold: true
                }
                Rectangle{
                    width: parent.width - parent.spacing-parent.padding
                    height: parent.height * 0.1
                    color : "#fcffff"
                    radius : 5
                    RowLayout{
                        width: parent.width
                        height: parent.height

                        Grid{
                            Layout.preferredWidth:  parent.width * 0.7
                            Layout.preferredHeight:  parent.height
                            columns: 2
                            rowSpacing: 10
                            columnSpacing: 20
                            padding: 10
                            id : calibrationRow


                            Label{
                                text: "CALIBRATION : "
                                font.bold: true
                                width: 100
                            }

                            Label {
                                id: calibrationDate
                                text : fileHandler.calibrationDate
                                width: 150
                            }

                            Label{
                                text: "VALIDATION : "
                                font.bold: true
                                width: 100
                            }

                            Label {
                                id: validationDate
                                text : fileHandler.validationDate
                                width: 150
                            }

                        }



                        Rectangle{
                            Layout.preferredWidth:  parent.width * 0.2
                            Layout.preferredHeight:  parent.height
                            Button{
                                text: qsTr("Define")
                                font.bold: true
                                width: parent.width
                                anchors.centerIn: parent
                                background: Rectangle{
                                    anchors.fill: parent
                                    color: "#29888b"
                                    radius: 5
                                }
                                onClicked: {
                                    chooseDatePopup.open()
                                }

                            }



                        }


                    }

                }

                Label {
                    text: qsTr("Datas")

                    font.bold: true
                }
                Rectangle{
                    width: 350 //parent.width - parent.spacing-parent.padding
                    height: parent.height * 0.6 - parent.padding - parent.spacing*6
                    color : "#fcffff"

                    HorizontalHeaderView {
                        id: horizontalHeader
                        anchors.left: tableView.left
                        anchors.top: parent.top
                        syncView: tableView
                        model: [ "Dates","P","T", "Q", "ETP"]
                        clip: true
                        delegate: Label {
                            color: "#000000"
                            width: 50
                            leftPadding: 5
                            font.bold: true
                            text: modelData
                            background: Rectangle{
                                color: "#c6f3fe"
                                anchors.fill: parent
                                border.color: "#000000"
                                border.width: 1
                            }
                        }


                    }

                    TableView {
                        id: tableView
                        width: parent.width
                        height: parent.height
                        anchors.left: parent.left
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
                            //rows : fileHandler.displayData
                        }
                        //model: dataTableModel

                        delegate: Item {
                            implicitWidth: 70
                            implicitHeight: 20

                            Rectangle {
                                anchors.fill: parent
                                border.width: 0.5
                                color: "#ffffff"

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

        }


        Rectangle {
            id: simulationPane
            width: parent.width * 0.7 -parent.spacing-2*parent.padding
            height: parent.height -2*parent.padding
            Grid {
                id: grid
                anchors.centerIn: parent
                width: parent.width
                height: parent.height
                rows: 2
                QobsChart{
                    id : qchart
                    width: parent.width
                    height: parent.height/2
                }
                ETPChart{
                    id : etpChart
                    width: parent.width
                    height: parent.height /2
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
        const keys = ["Dates", "P", "T", "Q", "ETP"];

        // Trouver la longueur maximale en une seule passe
        const maxLength = keys.reduce((max, key) => Math.max(max, columnMapping[key]?.length || 0), 0);

        // Remplir le modèle de données
        for (let i = 0; i < maxLength; i++) {
            let rowData = {};
            keys.forEach(key => rowData[key] = columnMapping[key]?.[i] ?? "");
            tableModel.appendRow(rowData);
        }
    }

    function transformData(data) {
        tableModel.clear();
        const keys = ["Dates", "P", "T", "Q", "ETP"];

        // Trouver la longueur des tableaux
        const length = data[keys[0]].length;

        // Construction du tableau transformé
        tableModel.rows =  Array.from({ length }, (_, i) =>
            Object.fromEntries(keys.map(key => [key, data[key][i]]))
        );
    }

}
