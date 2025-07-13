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




    Row {
        anchors.fill: parent
        spacing: 5
        padding: 5

        Column {
            width: parent.width * 0.4
            height: parent.height
            spacing: 5

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
                    delegate: Label {
                        color: "#000000"
                        width: 70
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

                VerticalHeaderView {
                    id: verticalHeader
                    anchors.top: tableView.top
                    anchors.left: parent.left
                    syncView: tableView
                    clip: true
                    delegate: Label {
                        color: "#000000"
                        width: 70
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
                        implicitWidth: 100
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
            width: parent.width * 0.6 - parent.spacing -parent.padding
            height: parent.height
            spacing: 5

            Rectangle {
                id: simulationPane
                width: parent.width *0.9
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
