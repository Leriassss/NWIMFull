import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import ".."
import "../chartsComponents"
import io.qml

Column{
    clip: true

    Connections {
        target: etoManager
        function onComputationChanged(){
            fileHandler.setEToValues(etoManager.etpComputed)
            populateTable(fileHandler.dataDict)
            console.log("Connexion ------------------------")
            console.log(JSON.stringify(fileHandler.dataDict))
            etpChart.updateChart(fileHandler.datesInfos["data"],fileHandler.etpInfos["data"])
        }
    }
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
        title: "❌ ERREURS DETECTEES !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)

        property var errors: fileHandler.errors

        Rectangle{
            anchors.fill: parent
            border.width: 1
            ListView {
                id: errorListView
                model: dataErrorsDialog.errors
                anchors.fill: parent
                delegate: Item {
                    width: errorListView.width
                    height: 30
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
        onAccepted:{
            columnMappingDialog.open()
        }
    }


    Dialog {
            id: columnMappingDialog
            title: "MAPPING"
            implicitWidth:  600
            implicitHeight: 400
            modal: true
            popupType: Popup.Window
            //topInset : 5
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
                    "T": tComboBox.currentText,
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
                }
                else{
                    populateTable(fileHandler.dataDict)
                    fileHandler.calibrationTime()

                    /*dataTableModel.setData(fileHandler.dataDict)*/
                    //tableView.appendRow(fileHandler.displayData)
                    //transformData(fileHandler.dataDict)
                    let data_dates = fileHandler.dataDict["Dates"]
                    tempChart.updateChart(data_dates,fileHandler.dataDict["T"])
                    qchart.updateChart(data_dates,fileHandler.dataDict["Q"])
                    rainChart.updateChart(data_dates,fileHandler.dataDict["P"])
                    etpChart.updateChart(data_dates,fileHandler.dataDict["ETP"])
                    columnMappingDialog.close()
                }

            }

            Rectangle{
                anchors.fill: parent
                border.width: 1

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


    }

    Row {
        anchors.fill: parent
        spacing: 5
        padding: 5
        clip: true

        Column {
            width: parent.width * 0.3
            height: parent.height - parent.padding
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
                color: "transparent"

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
                        //rows : fileHandler.displayData
                    }
                    //model: dataTableModel

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

        Rectangle {
            id: simulationPane
            width: parent.width * 0.7 -parent.spacing-parent.padding
            height: parent.height -parent.padding
            border.width: 2
            border.color: "red"
            clip : true

            Column {
                width: parent.width
                height: parent.height

                Rectangle {
                    width: parent.width
                    height: parent.height * 0.15
                    border.width: 1
                    border.color: "grey"
                    ColumnLayout{
                        width: parent.width
                        height: parent.height
                        Row{
                            padding: 5
                            spacing: 5
                            id : calibrationRow
                            Layout.preferredWidth:  parent.width * 0.5
                            Layout.preferredHeight:  parent.height *0.1

                            Label{
                                text: "FROM : "
                                font.bold: true
                                width: 100
                            }

                            Label {
                                id: calibrationDate
                                text : fileHandler.calibrationDate
                                width: 150
                            }

                            Label{
                                text: "TO : "
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
                            border.width: 1
                            border.color: "grey"
                            Layout.preferredWidth:  parent.width * 0.5
                            Layout.preferredHeight:  50
                            Button{
                                leftPadding: 5
                                text: qsTr("Define")
                                font.bold: true
                                width: 100
                                anchors.centerIn: parent
                                onClicked: {
                                    chooseDatePopup.open()
                                }

                            }

                            Dialog{
                                id : chooseDatePopup
                                width: 500
                                height: 200
                                standardButtons: Dialog.Ok | Dialog.Cancel
                                title: qsTr("CHOOSE PERIODS BEGININS")

                                CalibrationLength{
                                    id : calibrationLength
                                    anchors.fill: parent
                                    calibration_dates:columnMappingDialog.calib_dates
                                }
                                onAccepted: {
                                    console.log("-*-*-*--*-*-* CALIBRATION LENGTH -*-*-*-*-*-*-*-*-*")
                                    console.log(calibrationLength.user_calibration)
                                    fileHandler.updateCalibrationAndValibationDates(calibrationLength.user_calibration)
                                }
                            }
                        }


                    }
                }

                Rectangle {
                    id: plot
                    width: parent.width
                    height: parent.height * 0.85
                    //anchors.centerIn: parent
                    border.width: 2


                    Grid {
                        id: grid
                        width: parent.width -padding
                        height: parent.height - padding
                        columns: 2
                        rowSpacing: 0
                        columnSpacing: 0
                        padding: 10
                        clip : true
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
