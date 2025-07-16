import QtQuick
import QtQuick.Controls
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

    closePolicy : Popup.CloseOnEscape
    //padding: 5
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    background: Rectangle{
        anchors.fill: parent
        color : "#fcffff"
    }

    header: ToolBar {
            id: toolBar
            height: 30
            background: Rectangle{
                anchors.fill : parent
                color:"#fcffff"
            }

            clip: true
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
                    text: qsTr("▶️")
                    ToolTip.text: qsTr("Optimize")
                    onClicked: {
                        if(!fileHandler.activate){
                            errorDialog.errorText = "No data load for optimization. See Data Import"
                            errorDialog.open()
                            return
                        }

                        console.log("--------- OPTIMIZE -----------------")
                        automaticCalibration.setParameters(dialogOptim.parameters_bundle, dialogOptim.optimization_bundle,fileHandler.ptq)
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
        fileMode: FileChoose.SaveFile
        nameFilters: ["JSON (*.json)"]
        property string fileName: ""

        onAccepted: {
            fileName = cleanFilePath(loadRangeParams.file.toString());
            if (fileName) {
                try {
                    console.log("------ OPTIM NAME------")
                    console.log(fileName)
                } catch (error) {
                    errorDialog.errorText = "Erreur lors du chargement du fichier : " + error
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
        property string errorText: ""
        Label {
            text: errorDialog.errorText
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
            color: "#eaf6f4"
            border.width: 1
            border.color: "gray"
            topLeftRadius: 5
            topRightRadius : 5
            SplitView.minimumWidth:  parent.width*0.5
            SplitView.preferredWidth: parent.width*0.5
            //width: parent.width*0.4
            //height: parent.height
            Column{
                width: parent.width - 5
                height: parent.height - 5
                anchors.centerIn: parent
                spacing : 10
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
                        anchors.fill: parent
                        topLeftRadius: 5
                        topRightRadius : 5
                        color : "#bae7fe"
                    }
                }

                CustomCheckDelegate{
                    id : setGoal
                    checked: true
                    text: "Set Goal"
                    font.bold: true
                }

                Rectangle{
                    enabled: setGoal.checked ? true : false
                    height: 70
                    width: parent.width *0.5
                    radius: 5
                    anchors.left:  parent.left
                    color: "#fcffff"
                    border.color: "#ebebeb"
                    border.width: 1
                    Grid{
                        leftPadding:10
                        columns: 2
                        rowSpacing: 10
                        columnSpacing: 10
                        Label{
                            text: "Nb iterations "
                        }
                        CustomTextField{
                            id : nbIter
                            width : 75
                            bottomPadding: 5
                        }
                        Label{
                            text: "Target "
                        }
                        CustomTextField{
                            id : target
                            width : 75
                        }

                    }
                }


                Row{
                    spacing: 5
                    width: parent.width
                    height: parent.height * 0.2
                    leftPadding: 10
                    Column{
                        height: parent.height
                        width: parent.width*0.3
                        spacing : 10

                        Label{
                            text : "Criteria"
                            font.bold: true
                        }

                        Rectangle{
                            height: 100
                            width: parent.width *0.8
                            radius: 5
                            color: "#fcffff"
                            border.color: "#ebebeb"
                            border.width: 1
                            ComboBox {
                                leftPadding: 10
                                width: parent.width * 0.8
                                height:  25
                                id: metricsComboBox
                                model: automaticCalibration.metrics
                                anchors.centerIn: parent
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


                    Column{

                        height: parent.height
                        width: parent.width*0.7 - parent.spacing -2*parent.leftPadding
                        //border.width: 1
                        spacing : 10
                        Label{
                            text : "Optimizer"
                            font.bold: true
                        }
                        Rectangle{
                            height: 100
                            width: parent.width
                            radius: 5
                            color: "#fcffff"
                            border.color: "#ebebeb"
                            border.width: 1
                            ScrollView{
                                leftPadding: 10
                                width: parent.width
                                height: 100
                                contentHeight : 200
                                Rectangle{
                                    height: parent.height * 0.9
                                    width: parent.width  * 0.8
                                    anchors.centerIn: parent
                                    Parameters{
                                        id : optimizationParameter
                                        width: parent.width
                                        height: childrenRect.height
                                        spacing: 10
                                        parameterModel : TestQML{}
                                        factoryName : "Optimization"
                                    }

                                }
                            }




                        }
                    }


                }

                Label{
                    id : test
                    text : "Optimization results"
                    font.bold: true
                    leftPadding: 10
                    /*property var model_opt:  [{"loss":{"eto_loss":{"alpha":"0.2671801616179113"}},
                        "pn":{"SCS":{"curve_number":"94.97770026982717","i_a":"0.6771343264440949"}},
                        "qb":{"Chapman":{"alpha":"0.3131980868925507"}},
                        "sim":{"HUN":{"time_base":"20.129501239494967"}}}]*/
                }

                Rectangle{
                    height: parent.height*0.4
                    width: parent.width *0.9
                    anchors.horizontalCenter: parent.horizontalCenter
                    radius: 5
                    color: "#fcffff"
                    border.color: "grey"
                    border.width: 1
                    Column{
                        width: parent.width
                        height: parent.height
                        spacing: 5

                        ListView {
                            width: parent.width
                            height: 125
                            model : [automaticCalibration.optimParams]
                            delegate:Rectangle {
                                width: parent.width
                                height: parent.height
                                color: "#fcffff"
                                border.color: "grey"
                                border.width: 1
                                required property var loss
                                required property var pn
                                required property var sim
                                required property var qb
                                Row{
                                    anchors.fill: parent
                                    Column {
                                        spacing: 6
                                        width: parent.width
                                        padding: 10
                                        Text {
                                            text: {
                                                console.log("*Myoptimoptions")
                                                console.log(Object.keys(loss)[0])
                                                let index = Object.keys(loss)[0]
                                                let value = JSON.stringify(loss[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            font.bold: true
                                        }


                                        Text {
                                            text: {
                                                let index = Object.keys(pn)[0]
                                                let value = JSON.stringify(pn[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            font.bold: true
                                        }

                                        Text {
                                            text: {
                                                let index = Object.keys(sim)[0]
                                                let value = JSON.stringify(sim[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            font.bold: true
                                        }


                                        Text {
                                            text: {
                                                let index = Object.keys(qb)[0]
                                                let value = JSON.stringify(qb[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            font.bold: true
                                        }
                                    }

                                    }

                            }

                        }



                        Grid{
                            leftPadding: 10
                            width: parent.width
                            height: 75
                            columns: 2
                            rowSpacing:  10
                            Text{
                                text: "Calibration : "
                                font.bold: true
                            }
                            Text{
                                width: 50
                                text : automaticCalibration.bestMetrics[0]
                            }
                            Text{
                                text: "Validation : "
                                font.bold: true
                            }
                            Text{
                                width: 50
                                text : automaticCalibration.bestMetrics[1]
                            }
                        }



                        Button{
                            id : runOptim
                            anchors.horizontalCenter:  parent.horizontalCenter
                            enabled: true
                            /*icon.source: "../icons/save.png"
                            icon.height: 15
                            icon.width: 55
                            icon.color: "#ffffff"*/
                            text: "💾   Save"
                            width: 100
                            height: 30
                            font.bold: true
                            property color defaultColor: "#0b7878"
                            property color pressedColor: "#a9e0c2"
                            property color borderColor: "#1fa869"

                            background: Rectangle {
                                anchors.fill: parent
                                radius: 5
                                color: parent.pressed ? parent.pressedColor :parent.defaultColor
                                border.width: parent.pressed  ? 1 : 0
                                border.color: parent.pressed ? parent.borderColor : "transparent"
                            }
                            hoverEnabled: false
                            onClicked: {
                                if(!fileHandler.activate){
                                    errorDialog.errorText = "No data load for optimization. See Data Import"
                                    errorDialog.open()
                                    return
                                }
                                saveResultsDialog.open()
                            }


                        }


                    }


                }

            }

        }

        Rectangle{
            color: "#eaf6f4"
            border.width: 1
            border.color: "gray"
            topLeftRadius: 5
            topRightRadius : 5
            width: parent.width*0.6
            height: parent.height
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
                        anchors.fill: parent
                        topLeftRadius: 5
                        topRightRadius : 5
                        color : "#bae7fe"
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
                            color : "#eaf6f4"
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
                            color : "#eaf6f4"
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
                            color : "#eaf6f4"
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
