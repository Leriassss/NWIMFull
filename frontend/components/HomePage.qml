import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Effects

import "."
import "./parameters"
import "./chartsComponents"

//import "../../io/qml"
import io.qml
Rectangle{
    color : "#ebebeb"
    property var parameter_bundle: {
        "pn":production_params.parameters,
        "qb":recession_params.parameters,
        "sim": routing_params.parameters,
        "loss" : loss_params.parameters
    }
    Row {
        anchors.fill: parent
        id: splitView
        //spacing: 5
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
                        font.pointSize: 11
                        padding: 5
                        color: "black"
                        width: parent.width
                        background: Rectangle {
                            radius : 2
                            gradient: Gradient {
                                                GradientStop { position: 0.0; color: "#caf6fc" } // bord haut-gauche
                                                GradientStop { position: 1.0; color: "#c2f4c6" } // bord bas-droit
                                            }
                            layer.enabled: parameters.enabled
                            layer.effect: MultiEffect {
                                shadowEnabled: true
                                shadowHorizontalOffset: 2
                                shadowVerticalOffset: 2
                                shadowColor: parameters.visualFocus ? "#330066ff" : "#aaaaaa"
                            }
                        }
                        /*background: Rectangle{
                            color: "#d2d2d2"
                            width: parent.width
                            height: parent.height
                        }*/
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
                                color : "#ebebeb"
                                Column {
                                    anchors.fill: parent
                                    spacing: 5
                                    padding: 10

                                    Label {
                                        width: parent.width
                                        text: "Production Methods"
                                        font.bold: true
                                        font.pointSize: 11
                                        padding: 5
                                        color: "black"
                                        horizontalAlignment: Qt.AlignHCenter
                                    }

                                    Parameters {
                                        id : production_params
                                        height: childrenRect.height
                                        spacing: 10
                                        width: parent.width - 2*parent.padding
                                        parameterModel: TestQML{}
                                        factoryName: "Production"
                                    }

                                    Parameters {
                                        id : loss_params
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
                                color : "#ebebeb"
                                Column {
                                    spacing: 5
                                    padding: 10
                                    anchors.fill: parent

                                    Label {
                                        width: parent.width
                                        text: "Routing Methods"
                                        font.bold: true
                                        font.pointSize: 11
                                        padding: 5
                                        color: "black"
                                        horizontalAlignment: Qt.AlignHCenter
                                    }

                                    Parameters {
                                        id : routing_params
                                        height: childrenRect.height
                                        spacing: 10
                                        width: parent.width - 2*parent.padding
                                        parameterModel: TestQML{}
                                        factoryName: "Routing"
                                    }
                                }

                            }

                            Rectangle{
                                color : "#ebebeb"
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
                                        font.pointSize: 11
                                        padding: 5
                                        color: "black"
                                        horizontalAlignment: Qt.AlignHCenter
                                    }

                                    Parameters {
                                        id : recession_params
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
                /*gradient: Gradient {
                    GradientStop { position: 0.0; color: "#cecece" } // bord haut-gauche
                    GradientStop { position: 1.0; color: "#f0f0f0" } // bord bas-droit
                }*/
                Column {
                    width: parent.width
                    height: parent.height

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
                                width: parent.width
                                height: parent.height *0.25
                                color : "transparent"
                                Label {
                                    id : outputLabel
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "OUTPUT"
                                    horizontalAlignment: Qt.AlignHCenter
                                    font.bold: true
                                    font.pointSize: 11
                                    padding: 5
                                    color: "black"
                                    width: parent.width
                                    background: Rectangle {
                                        radius : 2
                                        //gradient: Gradient.AboveTheSky
                                        gradient: Gradient {
                                                            GradientStop { position: 0.0; color: "#caf6fc" } // bord haut-gauche
                                                            GradientStop { position: 1.0; color: "#c2f4c6" } // bord bas-droit
                                                        }
                                        layer.enabled: outputLabel.enabled
                                        layer.effect: MultiEffect {
                                            shadowEnabled: true
                                            shadowHorizontalOffset: 2
                                            shadowVerticalOffset: 2
                                            shadowColor: outputLabel.visualFocus ? "#330066ff" : "#aaaaaa"
                                        }
                                    }
                                }
                            }
                            Row {
                                id: parameterGrid
                                width: parent.width
                                height: parent.height *0.75
                                spacing : 0
                                Rectangle{
                                    width: parent.width * 0.5
                                    height:  parent.height
                                    border.width: 1
                                    border.color: "grey"
                                    color: "transparent"
                                    Column{
                                        anchors.fill: parent
                                        Rectangle{
                                            color: "transparent"
                                            width: parent.width
                                            height:  35
                                            border.width: 1
                                            border.color: "grey"
                                            CustomCheckDelegate{
                                                text: "CALIBRATION"
                                                checked: true
                                                anchors.centerIn: parent
                                                font.bold: true
                                                font.pointSize: 10

                                            }
                                        }
                                        Grid{
                                            width: parent.width
                                            height:  parent.height * 0.7
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
                                                        width: 20
                                                    }
                                                    Label{
                                                        id : calibration_rainfall_sum
                                                        width: 20
                                                    }
                                                    Label{
                                                        text: "I"
                                                        width: 20
                                                    }
                                                    Label{
                                                        id : calibration_infiltration_sum
                                                        width: 20
                                                    }
                                                    Label{
                                                        text : "DS"
                                                    }
                                                    Label{
                                                        id : calibration_stock_sum
                                                        width: 20
                                                    }
                                                }
                                                Row{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    spacing: 10
                                                    Label{
                                                        text: "NSE"
                                                        width: 20
                                                    }
                                                    Label{
                                                        id : calibration_nse
                                                        width: 20
                                                    }
                                                    Label{
                                                        text: "KGE"
                                                        width: 20
                                                    }
                                                    Label{
                                                        id : calibration_kge
                                                        width: 20
                                                    }
                                                    Label{
                                                        text : "BIAIS"
                                                        width: 20
                                                    }
                                                    Label{
                                                        id : calibration_bias
                                                        width: 20
                                                    }
                                                }
                                            }

                                        }
                                    }

                                }

                                Rectangle{
                                    width: parent.width * 0.5
                                    height:  parent.height
                                    border.width: 1
                                    border.color: "grey"
                                    color: "transparent"
                                    Column{
                                        anchors.fill: parent
                                        Rectangle{
                                            width: parent.width
                                            height:  35
                                            border.width: 1
                                            border.color: "grey"
                                            color: "transparent"

                                            CustomCheckDelegate{
                                                text: "VALIDATION"
                                                checked: true
                                                anchors.centerIn: parent
                                                font.bold: true
                                                font.pointSize: 10

                                            }
                                        }
                                        Grid{
                                            width: parent.width
                                            height:  parent.height * 0.7
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
                        clip : true
                        Row{
                            width: parent.width
                            height: parent.height * 0.1
                            Button {
                                z : 2
                                height: parent.height
                                text: qsTr("💾")
                                hoverEnabled: true
                                ToolTip.visible: hovered
                                ToolTip.text: qsTr("Save Plot")
                                background: Rectangle{
                                    anchors.fill: parent
                                }
                            }
                            Button {
                                z : 2
                                height: parent.height
                                text: qsTr("🔎")
                                hoverEnabled: true
                                ToolTip.visible: hovered
                                ToolTip.text: qsTr("Zoom")
                                background: Rectangle{
                                    anchors.fill: parent
                                }
                            }
                        }

                        SimChart{
                            width: parent.width
                            height: parent.height
                        }
                    }
                }
            }
        }

}

