import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


import "."
import "./parameters"

//import "../../io/qml"
import io.qml
Row {
    id: splitView
    /*handle: Rectangle {
        implicitWidth: 4
        implicitHeight: 4
        color: SplitHandle.pressed ? "#81e889"
            : (SplitHandle.hovered ? Qt.lighter("#c2f4c6", 1.1) : "#c2f4c6")
        border.width: 1
        border.color: "grey"
    }*/
    Rectangle{
        width: parent.width * 0.25
        height: parent.height - spacing
        anchors.left: parent.left
        clip: true
        Column {
            id: parameterPane
            width: parent.width
            height: parent.height
            spacing: 2
            clip: true
            Label {
                id: parameters
                anchors.horizontalCenter: parent.horizontalCenter
                horizontalAlignment: Qt.AlignHCenter
                text: "PARAMETERS"
                font.bold: true
                font.pointSize: 12
                padding: 5
                color: "black"
                width: parent.width
                background: Rectangle{
                    color: "#d2d2d2"
                    width: parent.width
                    height: parent.height
                }
            }

            Rectangle {
                id: simParameters
                width: parent.width
                height: parent.height * 0.8

                SplitView {
                    anchors.fill: parent
                    orientation: Qt.Vertical
                    handle: Rectangle {
                        implicitWidth: 4
                        implicitHeight: 4
                        color: SplitHandle.pressed ? "#81e889"
                            : (SplitHandle.hovered ? Qt.lighter("#c2f4c6", 1.1) : "#c2f4c6")
                        border.width: 1
                        border.color: "grey"
                    }

                    Rectangle{
                        SplitView.minimumHeight: 45
                        SplitView.preferredHeight: 250
                        color: "white"
                        Column {
                            anchors.fill: parent
                            spacing: 5
                            padding: 10

                            Label {
                                width: parent.width
                                text: "Production Methods"
                                font.bold: true
                                font.pointSize: 12
                                padding: 5
                                color: "black"
                                horizontalAlignment: Qt.AlignHCenter
                            }

                            Parameters {
                                height: childrenRect.height
                                spacing: 10
                                width: parent.width - 2*parent.padding
                                parameterModel: TestQML{}
                                factoryName: "Production"
                            }

                            Parameters {
                                height: 75
                                spacing: 10
                                width: parent.width - 2*parent.padding
                                parameterModel: TestQML{}
                                factoryName: "InitialLoss"
                            }
                        }

                    }


                    Rectangle{
                        SplitView.minimumHeight: 45
                        SplitView.preferredHeight: 150
                        color: "white"
                        Column {
                            spacing: 5
                            padding: 10
                            anchors.fill: parent

                            Label {
                                width: parent.width
                                text: "Routing Methods"
                                font.bold: true
                                font.pointSize: 12
                                padding: 5
                                color: "black"
                                horizontalAlignment: Qt.AlignHCenter
                            }

                            Parameters {
                                height: childrenRect.height
                                spacing: 10
                                width: parent.width - 2*parent.padding
                                parameterModel: TestQML{}
                                factoryName: "Routing"
                            }
                        }

                    }

                    Rectangle{
                        color: "white"
                        SplitView.minimumHeight: 100
                        Column {
                            anchors.fill: parent
                            width: parent.width
                            spacing: 5
                            padding: 10

                            Label {
                                width: parent.width
                                text: "Recession Methods"
                                font.bold: true
                                font.pointSize: 12
                                padding: 5
                                color: "black"
                                horizontalAlignment: Qt.AlignHCenter
                            }

                            Parameters {
                                height: childrenRect.height
                                spacing: 10
                                width: parent.width - 2*parent.padding
                                parameterModel: TestQML{}
                                factoryName: "Recession"
                            }
                        }

                    }


                }
            }

        }

    }


    Rectangle {
        id: simulationPane
        width: parent.width * 0.75 - 6
        height: parent.height
        border.width: 1
        anchors.right: parent.right
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
