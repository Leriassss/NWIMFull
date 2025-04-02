import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./parameters"
import "../../io/qml"
import io.qml

Dialog {
    title: "OPTIMIZATION"
    implicitWidth:  1000
    implicitHeight: 700
    modal: true
    popupType: Popup.Window

    standardButtons: Dialog.Ok | Dialog.Cancel
    closePolicy : Popup.CloseOnEscape
    padding: 5
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    SplitView {
        id: splitView
        anchors.fill: parent

        handle: Rectangle {
            implicitWidth: 4
            implicitHeight: 4
            color: SplitHandle.pressed ? "#81e889"
                : (SplitHandle.hovered ? Qt.lighter("#c2f4c6", 1.1) : "#c2f4c6")
            border.width: 1
            border.color: "grey"
        }

        Column{
            width: parent.width*0.4
            height: parent.height
            anchors.left: parent.left
            Column{
                height: parent.height *0.2
                width: parent.width
                //border.width: 1
                padding: 10
                spacing : 10
                CheckBox {
                    checked: true
                    text: "OBJECTIF"
                }

                Row{
                    padding: 30
                    anchors.bottom: parent.bottom
                    height: parent.height *0.9
                    width: parent.width
                    spacing : 5
                    Row{
                        height: parent.height
                        width: parent.width *0.5
                        spacing : 5
                        Label{
                            text: "Nb iterations "
                        }
                        TextField{
                            width : 75
                        }
                    }
                    Row{
                        height: parent.height
                        width: parent.width *0.5 - 5
                        spacing : 5
                        Label{
                            text: "Target "
                        }
                        TextField{
                            width : 75
                        }
                    }
                }

            }

            Parameters{
                height: parent.height *0.8
                width: parent.width
                parameterModel : TestQML{}
                factoryName : "Optimization"
            }

        }

        Column{
            width: parent.width*0.6
            height: parent.height
            anchors.right: parent.right
            RangeParameters{
                parameterModel : RangeParametersQML{}
                factoryName : "Production"
                height: parent.height *0.25
                width: parent.width
            }
            RangeParameters{
                anchors.right: parent.right
                parameterModel : RangeParametersQML{}
                factoryName : "InitialLoss"
                height: parent.height *0.25
                width: parent.width
            }
            RangeParameters{
                parameterModel : RangeParametersQML{}
                factoryName : "Routing"
                height: parent.height *0.25
                width: parent.width
            }
            RangeParameters{
                anchors.right: parent.right
                parameterModel : RangeParametersQML{}
                factoryName : "Recession"
                height: parent.height *0.25
                width: parent.width
                /*background: Rectangle {
                    color: "white"
                    border.width: 1
                }*/

            }
        }

    }

}
