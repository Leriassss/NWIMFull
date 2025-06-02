import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import "./parameters"
import "../../io/qml"
import io.qml
import Qt5Compat.GraphicalEffects
Dialog {
    title: "OPTIMIZATION"
    implicitWidth:  1000
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    id: dialogOptim

    standardButtons: Dialog.Cancel
    closePolicy : Popup.CloseOnEscape
    //padding: 5
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    header: ToolBar {
            id: toolBar
            height: 30
            //implicitHeight: 35
            implicitWidth:  200

            clip: true
            Rectangle{
                //gradient: Gradient.AboveTheSky
                color:"#ebebeb"
                //border.color: "#6b6b6b"
                //border.width: 1

                anchors.fill: parent
                Row{
                    anchors.fill: parent
                    spacing: 1
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("📥")
                        ToolTip.text: qsTr("Load Parameters")
                        onClicked: {
                            loadRangeParams.open()
                        }
                    }

                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("💾")
                        ToolTip.text: qsTr("Save Parameters")
                        onClicked: {
                            saveResultsDialog.open()
                        }
                    }
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("▶️")
                        ToolTip.text: qsTr("Optimize")
                        onClicked: {
                            console.log("------------ HOME PAGE ---------------")
                            console.log(JSON.stringify(homepage.parameter_bundle))
                        }
                    }
                }
            }


       }

    property var parameters_bundle: {
        "pn":productionRange.parameterModel,
        "qb":recessionRange.parameterModel,
        "sim": routingRange.parameterModel,
        "loss" : initialLossRange.parameterModel
    }
    property var optimization_bundle: [optimizationParameter.parameterModel]

    FileChoose {
        id: loadRangeParams
        fileMode: FileDialog.SaveFile
        nameFilters: ["JSON (*.json)"]
        folder: shortcuts.home
        property string fileName: ""

        onAccepted: {
            fileName = cleanFilePath(loadRangeParams.file.toString());
            if (fileName) {
                try {
                    console.log("------ OPTIM NAME------")
                    console.log(fileName)
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

    FileChoose {
         id: saveResultsDialog
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["JSON (*.json)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(saveResultsDialog.file.toString());
             automaticCalibration.saveSimulationResults(fileName)

         }
         onRejected: {
            console.log("Canceled")
         }
     }

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
            SplitView.minimumWidth:  parent.width*0.5
            SplitView.preferredWidth: parent.width*0.5
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
                        font.pointSize: 10
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
                    title: "Objective"
                    bottomInset: 10

                    ColumnLayout{
                        anchors.fill: parent
                        //border.width: 1
                        spacing : 10
                        CustomCheckDelegate{
                            checked: true
                            text: "Set"
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

                Row{
                    spacing: 5
                    width: parent.width
                    height: parent.height * 0.2
                    GroupBox{
                        height: parent.height
                        width: parent.width * 0.5
                        title: "Criteria"

                        ColumnLayout{
                            height: parent.height
                            width: parent.width
                            ComboBox {
                                leftPadding: 10
                                Layout.preferredWidth: parent.width
                                Layout.preferredHeight: 40
                                id: metricsComboBox
                                model: automaticCalibration.metrics
                                onCurrentTextChanged: {
                                    //console.log("-----------------------------")
                                    automaticCalibration?.setMetric(metricsComboBox.currentText)
                                }
                                /*onCurrentIndexChanged: {
                                    console.log("-----------------------------")
                                }*/
                            }


                        }

                    }

                    GroupBox{
                        height: parent.height
                        width: parent.width * 0.5 - parent.spacing
                        title: "Optimizator"


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
                    font.pointSize: 10
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
                                width: parent.width
                                height: parent.height
                                spacing: 2
                                padding: 5

                                Label {
                                    width: parent.width
                                    text: "Production Methods"
                                    font.bold: true
                                    font.pointSize: 10
                                    padding: 1
                                    color: "black"
                                    horizontalAlignment: Qt.AlignHCenter
                                    background: Rectangle{
                                        anchors.fill: parent
                                        color: Qt.lighter("#c2f4c6", 1.1)
                                        opacity: 0.7
                                    }
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
                                spacing: 2
                                padding: 5
                                anchors.fill: parent

                                Label {
                                    width: parent.width
                                    text: "Routing Methods"
                                    font.bold: true
                                    font.pointSize: 10
                                    padding: 1
                                    color: "black"
                                    horizontalAlignment: Qt.AlignHCenter
                                    background: Rectangle{
                                        anchors.fill: parent
                                        color: Qt.lighter("#c2f4c6", 1.1)
                                        opacity: 0.7
                                    }
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
                                spacing: 2
                                padding: 5

                                Label {
                                    width: parent.width
                                    text: "Recession Methods"
                                    font.bold: true
                                    font.pointSize: 10
                                    padding: 1
                                    color: "black"
                                    horizontalAlignment: Qt.AlignHCenter
                                    background: Rectangle{
                                        anchors.fill: parent
                                        color: Qt.lighter("#c2f4c6", 1.1)
                                        opacity: 0.7
                                    }
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
    function cleanFilePath(filePath) {
        if (filePath.startsWith("file:///")) {
            return filePath.substring(8);
        }
        return filePath;
    }
}
