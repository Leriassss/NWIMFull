import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


import "."
import "./parameters"

//import "../../io/qml"
import io.qml
Row {
    id: layout
    anchors.top: nwimMenuBar.bottom
    width: parent.width
    height: parent.height * 0.88
    spacing: 6

    Rectangle {
        id: parameterPane
        width: parent.width * 0.25
        height: parent.height
        border.width: 1
        color: "#c8c8c8"
        Text {
            id: parameters
            anchors.margins: 5
            anchors.top: parent.top
            anchors.horizontalCenter: parent.horizontalCenter
            text: "PARAMETERS"
        }

        Rectangle {
            id: simParameters
            anchors.top: parameters.bottom
            width: parent.width
            height: parent.height * 0.85
            //color: "purple"

            Column {
                id: parametersColumn
                height: parent.height
                width: parent.width
                spacing: 5

                // Liste des modèles à afficher
                property var models: ["Production","InitialLoss","Routing", "Recession"]

                // Répétiteur pour afficher chaque modèle
                Repeater {
                    model: parametersColumn.models

                    delegate: Parameters {
                        height: parent.height * 0.25
                        width: parent.width
                        parameterModel : TestQML{}
                        factoryName:  modelData
                        background: Rectangle {
                            color: "white"
                            border.width: 1
                        }
                    }
                }
            }

        }

        HomePageButtons {
            anchors.top: simParameters.bottom
            leftPadding: 10
            width: parent.width
            height: parent.height * 0.15
            id: buttonsRow
        }
    }

    Rectangle {
        id: simulationPane
        width: parent.width * 0.75 - 6
        height: parent.height
        border.width: 1
        Column {
            width: parent.width
            height: parent.height

            Rectangle {
                id: plotOptions
                width: parent.width
                height: parent.height * 0.15
                border.width: 1

                Row {
                    width: parent.width
                    height: parent.height
                    spacing: 6
                    Rectangle {
                        border.width: 1
                        anchors.margins: 20
                        width: parent.width
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
                                border.width: 1
                                Text {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "OUTPUT"
                                }
                                Row {
                                    anchors.centerIn: parent
                                    width: parent.width
                                    RadioButton {
                                        checked: true
                                        text: "Qbase"
                                    }
                                    RadioButton {
                                        text: "Q"
                                    }
                                    RadioButton {
                                        text: "ETP"
                                    }
                                    RadioButton {
                                        text: "P"
                                    }
                                }
                            }
                            Rectangle {
                                width: parent.width * 0.5 - 6
                                height: parent.height * 0.7
                                border.width: 1
                                anchors.bottom: parent.bottom
                                Text {
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "PERIOD"
                                }
                                Row {
                                    anchors.centerIn: parent
                                    width: parent.width
                                    CheckBox {
                                        checked: true
                                        text: "CALIBRATION"
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
                border.width: 1
            }
        }
    }
}
