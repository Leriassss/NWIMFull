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
        target: fileHandler
        function onDataDictChanged() {
            populateTable({"CDates" : fileHandler.datesInfos["data_cal"],
                           "Calibration" : fileHandler.pInfos["data_cal"],
                            "VDates" : fileHandler.datesInfos["data_val"],
                            "Validation" : fileHandler.pInfos["data_val"]
                          })
            pCalibrationChart.updateChart(fileHandler.datesInfos["data_cal"],fileHandler.pInfos["data_cal"])
            pValidationChart.updateChart(fileHandler.datesInfos["data_val"],fileHandler.pInfos["data_val"])
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
            width: parent.width * 0.3 - parent.spacing
            height: parent.height
            spacing: 5

            Rectangle{
                width: parent.width
                height: parent.height * 0.6
                //border.width: 1
                color : "transparent"

                HorizontalHeaderView {
                    id: horizontalHeader
                    anchors.left: tableView.left
                    anchors.top: parent.top
                    syncView: tableView
                    model: [ "Dates","P Calibration","Dates","P Validation"]
                    clip: true

                    /*delegate: Rectangle {
                         width: 70
                         height: 20
                         color: "#fafafa"
                         Label {
                             text: modelData
                             anchors.centerIn: parent
                             font.bold: true
                         }
                     }*/
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
                                    "min" : fileHandler.pInfos["min_cal"],
                                    "max" : fileHandler.pInfos["max_cal"],
                                    "mean" : fileHandler.pInfos["mean_cal"],
                                    "sum" : fileHandler.pInfos["sum_cal"],
                                    "std" : fileHandler.pInfos["std_cal"]
                                }
                                periodLabel : "CALIBRATION"
                            }
                            StatisticsComponent{
                                spacing: 20
                                width: parent.width
                                height: parent.height *0.3
                                padding: 5
                                statistics: {
                                    "min" : fileHandler.pInfos["min_val"],
                                    "max" : fileHandler.pInfos["max_val"],
                                    "mean" : fileHandler.pInfos["mean_val"],
                                    "sum" : fileHandler.pInfos["sum_val"],
                                    "std" : fileHandler.pInfos["std_val"]
                                }
                                periodLabel : "VALIDATION"
                            }
                            StatisticsComponent{
                                spacing: 20
                                width: parent.width
                                height: parent.height *0.3
                                padding: 5
                                statistics: {
                                    "min" : fileHandler.pInfos["min"],
                                    "max" : fileHandler.pInfos["max"],
                                    "mean" : fileHandler.pInfos["mean"],
                                    "sum" : fileHandler.pInfos["sum"],
                                    "std" : fileHandler.pInfos["std"]
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

                            RainChart{
                                id : pCalibrationChart
                                Layout.preferredWidth: parent.width / 2
                                Layout.preferredHeight:parent.height
                                chartName : "Rainfall Calibration"

                            }
                            RainChart{
                                id : pValidationChart
                                Layout.preferredWidth: parent.width / 2
                                Layout.preferredHeight:parent.height
                                chartName : "Rainfall Validation"
                            }

                        }


                    }
                }
            }
        }
    }

}
