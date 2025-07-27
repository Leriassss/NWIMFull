import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Effects
import Qt5Compat.GraphicalEffects
import "."
import "./parameters"
import "./chartsComponents"

//import "../../io/qml"
import io.qml
Dialog{

    title: "DATA"
    implicitWidth:  1300
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    closePolicy : Popup.CloseOnEscape

    background:Rectangle{
        anchors.fill: parent
        color: "#fcffff"
    }

    property color siderbarColor: "#bae7fe"
    property color sidebarTextColor: "black"

    Dialog {
        id: saveBaseFlowOptions
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        width: 300
        height: 150
        title: "Save options"
        Rectangle{
            anchors.fill: parent
            /*border.color: "grey"
            border.width: 1*/
            Column{
                anchors.fill: parent

                CustomRadioButton{
                    height: 50
                    width: parent.width
                    text: "Save Plot"

                }
                Rectangle{
                    width: parent.width
                    height: 1
                    color: "#ebebeb"
                }
                CustomRadioButton{
                    height: 50
                    width: parent.width
                    text: "Save Data"
                    onClicked: {
                        saveQBase.open()
                        saveBaseFlowOptions.close()
                    }

                }

            }

        }


    }

    FileChoose {
        id: fileChooseComponent
        nameFilters: ["Excel (*.xlsx)","Texte (*.txt)"]
        property string fileName: ""

        onAccepted: {
            fileName = cleanFilePath(fileChooseComponent.file.toString());
            if (fileName) {
                try {
                    baseFlowSimulation.readFile(fileName)
                    var headers = baseFlowSimulation.headers
                    columnMappingDialog.headers = headers
                    columnMappingDialog.open()
                } catch (error) {
                    baseflowErrors.errors = ["Erreur lors du chargement du fichier : " + error]
                    baseflowErrors.open()
                }
            }
        }

    }

    FileChoose {
         id: saveQBase
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["txt (*.txt)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(saveQBase.file.toString());
            baseFlowSimulation.saveBaseFlow(fileName)

         }
         onRejected: {
            console.log("Canceled")
         }
     }

    Dialog {
            id: columnMappingDialog
            title: "MAPPING"
            implicitWidth:  300
            implicitHeight: 200
            modal: true
            standardButtons: Dialog.Ok | Dialog.Cancel
            closePolicy : Popup.CloseOnEscape
            x: Math.round((parent.width - width) / 2)
            y: Math.round((parent.height - height) / 2)


            property var headers: baseFlowSimulation.headers // En-têtes du fichier chargé

            onAccepted: {
                let columnMapping = {
                    "Dates":datesComboBox.currentText ,
                    "Q": qComboBox.currentText,
                }
                console.log("---------------- COLUMN MAPPING ------------------")
                console.log(JSON.stringify(columnMapping))

                baseFlowSimulation.setDictValues(columnMapping)


                if(baseFlowSimulation.errors.length !==0){
                    baseflowErrors.errors = baseFlowSimulation.errors
                    baseflowErrors.open()
                    console.log(JSON.stringify(baseFlowSimulation.errors))
                }
                else{

                    columnMappingDialog.close()
                    baseflowChart.setChart(
                                baseFlowSimulation.dataDict["Dates"],
                                baseFlowSimulation.dataDict["Q"])

                }


            }

            Rectangle{
                anchors.fill: parent
                border.width: 1
                border.color: "grey"
                color : "#fcffff"


                GridLayout {
                    height: parent.height
                    width: parent.width * 0.5
                    columns: 2 // Deux colonnes : une pour les labels, une pour les ComboBox
                    columnSpacing: 10
                    rowSpacing: 10


                    // Ligne pour Dates
                    Label {
                        text: "Dates"
                        Layout.alignment: Qt.AlignRight
                        leftPadding: 5
                    }
                    ComboBox {
                        id: datesComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }

                    // Ligne pour Q
                    Label {
                        text: "Q"
                        Layout.alignment: Qt.AlignRight
                    }
                    ComboBox {
                        id: qComboBox
                        model: columnMappingDialog.headers
                        currentIndex: 0
                        Layout.fillWidth: true
                    }


                }

            }


    }


    DataErrorsDialog {
        id: baseflowErrors
        title: "❌ ERRORS FOUNDS !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
    }

    Row {
        anchors.fill: parent
        id: splitView
        spacing: 20
        clip: true
            Rectangle{
                width: parent.width * 0.2
                height: parent.height
                anchors.left: parent.left
                clip: true
                border.width: 1
                border.color: "transparent"
                color: siderbarColor
                layer.enabled: true
                layer.effect: DropShadow {
                    horizontalOffset: 1
                    verticalOffset: 1
                    radius: 4
                    samples: 10
                    color: "#888888"
                }
                Column {
                    id: parameterPane
                    width: parent.width *0.99
                    anchors.centerIn: parent
                    height: parent.height - 1

                    spacing: 2
                    clip: true
                    Label {
                        id: parameters
                        horizontalAlignment: Qt.AlignHCenter
                        text: "BASEFLOW"
                        //font.bold: true
                        font.pointSize: 10
                        //topPadding: 20
                        padding: 5
                        color: "black"
                        width: parent.width
                        height: 35

                        CustomToolButton {
                            width: 50
                            height: parent.height
                            text: qsTr("📥")
                            ToolTip.text: qsTr("Load Data")
                            onClicked: {
                                fileChooseComponent.open()
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
                        Rectangle{
                            color : siderbarColor
                            width: parent.width
                            height: childrenRect.height
                            Column {
                                anchors.fill: parent
                                width: parent.width
                                spacing: 5
                                padding: 10

                                Label {
                                    width: parent.width
                                    text: "Methods"
                                    font.bold: true
                                    font.pointSize: 10
                                    padding: 5
                                    color: sidebarTextColor
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

                                Rectangle{
                                    height: 50
                                    width: parent.width - 20
                                    radius: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    //anchors.bottom: parent.bottom
                                    color: "#fcffff"
                                    Button{
                                        id : run
                                        anchors.centerIn: parent
                                        enabled: {
                                            console.log("ACTIVATION", baseFlowSimulation.activated)
                                            baseFlowSimulation.activated
                                        }
                                        flat : true
                                        opacity: enabled ? 1 : 0.7
                                        icon.source: "../icons/run.png"
                                        icon.height: 15
                                        icon.width: 55
                                        icon.color: "#ffffff"
                                        text: "     Run"
                                        font.bold: true
                                        property color defaultColor: "#0b7878"
                                        property color pressedColor: "#a9e0c2"
                                        property color borderColor: "#1fa869"

                                        background: Rectangle {
                                            width: 90
                                            height: 30
                                            radius: 5
                                            color: run.pressed ? run.pressedColor :run.defaultColor
                                            anchors.centerIn: parent
                                            border.width: run.pressed  ? 1 : 0
                                            border.color: run.pressed ? run.borderColor : "transparent"
                                        }

                                        onClicked: {
                                            if(baseFlowSimulation.errors.length !==0){

                                                baseflowErrors.open()
                                                console.log(JSON.stringify(baseFlowSimulation.errors))
                                                return
                                            }
                                            baseFlowSimulation.computeBaseflow(recession_params.parameterModel)
                                            baseflowChart.updateChart(
                                                        baseFlowSimulation.dataDict["Dates"],baseFlowSimulation.baseflowData["Baseflow"],
                                                        [],[])

                                        }
                                    }


                                }

                            }

                        }

                    }


                }
            }


            Rectangle {
                color: "#fcffff"
                id: simulationPane
                width: parent.width * 0.80 - parent.spacing
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
                    spacing: 5
                    Label {
                        id : outputLabel
                        anchors.margins: 5
                        anchors.horizontalCenter: parent.horizontalCenter
                        text: "OUTPUT AREA"
                        horizontalAlignment: Qt.AlignHCenter
                        //font.bold: true
                        font.pointSize: 10
                        padding: 5
                        color: "black"
                        width: parent.width
                        height: 35
                        CustomToolButton {
                            width: 50
                            height: parent.height
                            text: qsTr("💾")
                            ToolTip.text: qsTr("Save Options")
                            onClicked: {
                                saveBaseFlowOptions.open()
                            }
                        }
                    }
                    Column {
                        id: plot
                        width: parent.width
                        height: parent.height - parent.spacing -outputLabel.height
                        clip : true

                        SimChart{
                            id: baseflowChart
                            width: parent.width
                            height: parent.height
                            calibrationName : "Simulation"
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
