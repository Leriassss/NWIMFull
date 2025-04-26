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
    id: dialogOptim

    standardButtons: Dialog.Ok | Dialog.Cancel
    closePolicy : Popup.CloseOnEscape
    padding: 5
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    property var parameters_bundle: {
        "pn":productionRange.parameterModel,
        "qb":recessionRange.parameterModel,
        "sim": routingRange.parameterModel,
        "loss" : initialLossRange.parameterModel
    }
    property var optimization_bundle: [optimizationParameter.parameterModel]

    Dialog {
        id: errorDialog
        title: "Errors"
        standardButtons: Dialog.Ok
        property string text: ""
        Label {
            text: errorDialog.text
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

        Rectangle{
            color: "#ebebeb"
            SplitView.minimumWidth:  parent.width*0.2
            SplitView.preferredWidth: parent.width*0.4
            //width: parent.width*0.4
            //height: parent.height
            Column{
                anchors.fill: parent
                anchors.left: parent.left
                spacing : 20
                GroupBox{
                    height: parent.height *0.2
                    width: parent.width
                    title: "TARGETTING"
                    bottomInset: 10

                    ColumnLayout{
                        anchors.fill: parent
                        //border.width: 1
                        spacing : 10
                        CheckBox {
                            checked: true
                            text: "OBJECTIF"
                        }

                        Row{
                            padding: 30
                            Layout.preferredHeight: parent.height *0.9
                            Layout.preferredWidth: parent.width
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

                }
                GroupBox{
                    height: parent.height *0.2
                    width: parent.width
                    label: Label{
                        text: "CRITERIA"
                        color: "grey"
                        font.bold: true
                        font.pointSize: 10
                    }

                    ColumnLayout{
                        anchors.fill: parent
                        //border.width: 1
                        spacing : 10
                        ComboBox {
                            leftPadding: 10
                            Layout.preferredWidth: parent.width
                            Layout.preferredHeight: 40
                            id: methodSelector
                            model: automaticCalibration.metrics

                            background: Rectangle{
                                anchors.fill: parent
                                color: "#ebebeb"
                                border.width: 1
                                border.color: "grey"
                            }
                            popup: Popup {
                                y: methodSelector.height - 1
                                width: methodSelector.width
                                height: Math.min(contentItem.implicitHeight, methodSelector.Window.height - topMargin - bottomMargin)
                                padding: 1

                                contentItem: ListView {
                                    clip: true
                                    implicitHeight: contentHeight
                                    model: methodSelector.popup.visible ? methodSelector.delegateModel : null
                                    currentIndex: methodSelector.highlightedIndex


                                    ScrollIndicator.vertical: ScrollIndicator { }
                                }

                                background: Rectangle {
                                    id : rec
                                    border.color: "#21be2b"
                                }

                            }

                            indicator: Canvas {
                                   id: canvas
                                   x: methodSelector.width - width - methodSelector.rightPadding
                                   y: methodSelector.topPadding + (methodSelector.availableHeight - height) / 2
                                   width: 12
                                   height: 8
                                   contextType: "2d"

                                   Connections {
                                       target: methodSelector
                                       function onPressedChanged() { canvas.requestPaint(); }
                                   }

                                   onPaint: {
                                       context.reset();
                                       context.moveTo(0, 0);
                                       context.lineTo(width, 0);
                                       context.lineTo(width / 2, height);
                                       context.closePath();
                                       context.fillStyle = methodSelector.pressed ? "#17a81a" : "#21be2b";
                                       context.fill();
                                   }
                               }


                            onCurrentTextChanged: {
                                automaticCalibration.setMetric(methodSelector.currentText)
                            }
                        }


                    }

                }

                GroupBox{
                    height: parent.height *0.2
                    width: parent.width
                    title: "OPTIMIZATION PARAMETERS"


                    ColumnLayout{
                        anchors.fill: parent
                        //border.width: 1
                        spacing : 10
                        Parameters{
                            id : optimizationParameter
                            Layout.preferredHeight: childrenRect.height
                            Layout.preferredWidth: parent.width
                            height: childrenRect.height
                            spacing: 10
                            parameterModel : TestQML{}
                            factoryName : "Optimization"
                        }
                    }


                    }


                Button{
                    text: "Optimize"
                    width: 100
                    font.bold: true
                    font.pointSize: 10
                    //enabled: fileHandler.activate
                    onClicked: {
                        if(!fileHandler.activate){
                            errorDialog.text = "No data load for optimization. See Option Load"
                            errorDialog.open()
                            return
                        }

                        console.log("--------- OPTIMIZE -----------------")
                        console.log(JSON.stringify(dialogOptim.parameters_bundle))
                        automaticCalibration.setParameters(dialogOptim.parameters_bundle, dialogOptim.optimization_bundle,fileHandler.ptq)
                    }
                }

            }

        }

        Rectangle{
            width: parent.width*0.6
            height: parent.height
            color: "#ebebeb"
            Column{
                anchors.fill: parent

                anchors.right: parent.right
                RangeParameters{
                    id : productionRange
                    parameterModel : RangeParametersQML{}
                    factoryName : "Production"
                    height: parent.height *0.25
                    width: parent.width
                }
                RangeParameters{
                    id : initialLossRange
                    anchors.right: parent.right
                    parameterModel : RangeParametersQML{}
                    factoryName : "InitialLoss"
                    height: parent.height *0.25
                    width: parent.width
                }
                RangeParameters{
                    id : routingRange
                    parameterModel : RangeParametersQML{}
                    factoryName : "Routing"
                    height: parent.height *0.25
                    width: parent.width
                }
                RangeParameters{
                    id : recessionRange
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

}
