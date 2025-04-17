import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts


import "."
import "./parameters"

//import "../../io/qml"
import io.qml
Rectangle{
    gradient: Gradient {
        GradientStop { position: 0.0; color: "#cecece" } // bord haut-gauche
        GradientStop { position: 1.0; color: "#f0f0f0" } // bord bas-droit
    }
    Row {
        anchors.fill: parent
        id: splitView
        spacing: 5
        clip: true
            Rectangle{
                width: parent.width * 0.25
                height: parent.height
                anchors.left: parent.left
                clip: true
                border.width: 1
                border.color: "grey"
                color: "transparent"
                Column {
                    id: parameterPane
                    width: parent.width *0.99
                    anchors.centerIn: parent
                    height: parent.height - 1

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
                        color : "transparent"

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
                                color : "transparent"
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
                                color : "transparent"
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
                                color : "transparent"
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
                color: "transparent"
                id: simulationPane
                width: parent.width * 0.75 - parent.spacing
                height: parent.height
                //border.width: 1
                anchors.right: parent.right
                //color: "#d2d2d2"
                gradient: Gradient {
                    GradientStop { position: 0.0; color: "#cecece" } // bord haut-gauche
                    GradientStop { position: 1.0; color: "#f0f0f0" } // bord bas-droit
                }
                Column {
                    width: parent.width
                    height: parent.height
                    spacing: 25

                    Rectangle {
                        id: plotOptions
                        width: parent.width
                        height: parent.height * 0.2
                        border.width: 1
                        border.color: "grey"
                        color : "transparent"

                        Column {
                            width: parent.width
                            height: parent.height
                            Rectangle {
                                border.width: 1
                                anchors.margins: 20
                                width: parent.width
                                height: parent.height *0.2
                                color : "transparent"
                                Text {
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "OUTPUT"
                                    horizontalAlignment: Qt.AlignHCenter
                                    font.bold: true
                                    font.pointSize: 12
                                    padding: 5
                                    color: "black"
                                    width: parent.width
                                }
                            }
                            Row {
                                id: parameterGrid
                                width: parent.width
                                height: parent.height *0.8
                                spacing : 0
                                Column{
                                    width: parent.width * 0.5
                                    height:  parent.height
                                    Rectangle{
                                        width: parent.width
                                        height:  35
                                        border.width: 1
                                        border.color: "#3d3d3d"
                                        color : "transparent"

                                        CheckBox{
                                            text: "CALIBRATION"
                                            checked: true
                                            anchors.centerIn: parent

                                        }
                                    }
                                    Grid{
                                        width: parent.width
                                        height:  parent.height
                                        columns: 2
                                        leftPadding: 10
                                        Column{
                                            width: parent.width*0.3
                                            height:  parent.height
                                            Label{
                                                width: parent.width
                                                height:  parent.height *0.5
                                                text: "Bilan : "
                                                font.bold: true
                                                font.pointSize: 10
                                                color: "black"
                                            }
                                            Label{
                                                width: parent.width
                                                height:  parent.height *0.5
                                                text: "Criteria : "
                                                font.bold: true
                                                font.pointSize: 10
                                                color: "black"
                                            }
                                        }
                                        Column{
                                            width: parent.width*0.7
                                            height:  parent.height
                                            Row{
                                                width: parent.width
                                                height:  parent.height *0.5
                                                spacing: 10

                                                Label{
                                                    text: "P"
                                                }
                                                Label{
                                                    text: "I"
                                                }
                                                Label{
                                                    text : "DS"
                                                }
                                            }
                                            Row{
                                                width: parent.width
                                                height:  parent.height *0.5
                                                spacing: 10
                                                Label{
                                                    text: "NSE"
                                                }
                                                Label{
                                                    text: "KGE"
                                                }
                                                Label{
                                                    text : "BIAIS"
                                                }
                                            }
                                        }
                                    }





                                }

                                ColumnLayout {
                                    Layout.preferredWidth: parent.width * 0.5

                                }

                            }

                        }
                    }

                    Rectangle {
                        id: plot
                        width: parent.width
                        height: parent.height * 0.8 - parent.spacing
                        border.width: 1
                        border.color: "grey"
                    }
                }
            }
        }

}

