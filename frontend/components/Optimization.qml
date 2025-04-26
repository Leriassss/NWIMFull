import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
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
            border.width: 1
            border.color: "grey"
            SplitView.minimumWidth:  parent.width*0.2
            SplitView.preferredWidth: parent.width*0.4
            //width: parent.width*0.4
            //height: parent.height
            Column{
                width: parent.width - 5
                height: parent.height - 5
                anchors.centerIn: parent
                spacing : 20
                Rectangle {
                    width: parent.width
                    height: 15
                    color : "transparent"
                    Label {
                        id : outputLabel
                        anchors.margins: 5
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "OPTIMIZATION OPTIONS"
                        horizontalAlignment: Qt.AlignHCenter
                        font.bold: true
                        font.pointSize: 11
                        padding: 5
                        color: "black"
                        width: parent.width
                        background: Rectangle {
                            border.width: 1
                            border.color: "#17a81a"
                            radius : 2
                            color : "transparent"
                            layer.enabled: true
                            layer.effect: MultiEffect {
                                shadowEnabled: true
                                shadowHorizontalOffset: 2
                                shadowVerticalOffset: 2
                                shadowColor: outputLabel.visualFocus ? "#330066ff" : "#aaaaaa"
                            }
                        }
                    }
                }

                GroupBox{
                    height: parent.height *0.2
                    width: parent.width
                    title: "TARGETTING"
                    bottomInset: 10

                    ColumnLayout{
                        anchors.fill: parent
                        //border.width: 1
                        spacing : 10
                        CustomCheckDelegate{
                            checked: true
                            text: "OBJECTIF"
                        }

                        Row{
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
                    title: "CRITERIA"

                    ColumnLayout{
                        anchors.fill: parent
                        //border.width: 1
                        spacing : 10
                        CustomComboBox {
                            leftPadding: 10
                            Layout.preferredWidth: parent.width
                            Layout.preferredHeight: 40
                            id: methodSelector
                            model: automaticCalibration?.metrics
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

                Button {
                    id: control
                    text: qsTr("Optimize")
                    font.bold: true
                    font.pointSize: 10
                    anchors.right: parent.right
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
                    contentItem: Text {
                        text: control.text
                        font: control.font
                        opacity: enabled ? 1.0 : 0.3
                        //color: control.down ? "#17a81a" : "#21be2b"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        elide: Text.ElideRight
                    }

                    background: Rectangle {
                        implicitWidth: 100
                        implicitHeight: 40
                        opacity: enabled ? 1 : 0.3
                        border.color: control.down ? "#17a81a" : "#21be2b"
                        border.width: 1
                        radius: 2
                    }
                }

            }

        }

        Rectangle{
            border.width: 1
            border.color: "grey"
            width: parent.width*0.6
            height: parent.height
            color: "#ebebeb"
            Column{
                width: parent.width - 5
                height: parent.height - 5
                anchors.centerIn: parent
                spacing: 2
                clip: true
                Label {
                    id : methodsLabel
                    anchors.margins: 5
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "PARAMETERS"
                    horizontalAlignment: Qt.AlignHCenter
                    font.bold: true
                    font.pointSize: 11
                    padding: 5
                    color: "black"
                    width: parent.width
                    background: Rectangle {
                        border.width: 1
                        border.color: "#17a81a"
                        radius : 2
                        color : "transparent"
                        layer.enabled: true
                        layer.effect: MultiEffect {
                            shadowEnabled: true
                            shadowHorizontalOffset: 2
                            shadowVerticalOffset: 2
                            shadowColor: methodsLabel.visualFocus ? "#330066ff" : "#aaaaaa"
                        }
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

                                RangeParameters{
                                    id : productionRange
                                    parameterModel : RangeParametersQML{}
                                    factoryName : "Production"
                                    height: childrenRect.height
                                    width: parent.width - 2*parent.padding
                                    spacing: 10
                                }

                                RangeParameters{
                                    id : initialLossRange
                                    parameterModel : RangeParametersQML{}
                                    factoryName : "InitialLoss"
                                    height: 75
                                    width: parent.width - 2*parent.padding
                                    spacing: 10
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
                                    height: 15
                                    text: "Routing Methods"
                                    font.bold: true
                                    font.pointSize: 11
                                    padding: 5
                                    color: "black"
                                    horizontalAlignment: Qt.AlignHCenter
                                }

                                RangeParameters{
                                    id : routingRange
                                    parameterModel : RangeParametersQML{}
                                    factoryName : "Routing"
                                    height: childrenRect.height
                                    width: parent.width - 2*parent.padding
                                    spacing: 10
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
                                RangeParameters{
                                    id : recessionRange
                                    parameterModel : RangeParametersQML{}
                                    factoryName : "Recession"
                                    height: childrenRect.height
                                    width: parent.width - 2*parent.padding
                                    spacing: 10
                                }
                            }

                        }


                    }

                }


            }


        }


    }

}
