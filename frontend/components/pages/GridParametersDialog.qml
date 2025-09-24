import QtQuick
import QtQuick.Controls
import QtQuick.Layouts

import "../parameters"
import "../customComponents"
import io.qml

Dialog {
    id : gridZone
    title: "GRID OPTIMIZATION"
    implicitWidth:  1300
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    topInset : 5
    closePolicy : Popup.CloseOnEscape
    padding: 5
    background:  Rectangle{
        anchors.fill: parent
        color : "#ffffff"
    }
    property real weightNSE : 1
    property real weightKGE : 0


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
                spacing: 20
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
                    /*enabled: {

                        console.log(grid_calibration_bundle.every((bundle) => bundle.length > 0))
                        grid_calibration_bundle.every((bundle) => bundle.length > 0)
                    }*/
                    onClicked: {
                        if(!fileHandler.activate){
                            gridCalibrationErrors.errors  = ["No data load for optimization. See Data Import"]
                            gridCalibrationErrors.open()
                            return
                        }
                        //console.log(grid_calibration_bundle.every((bundle) => bundle.length > 0))
                        let grid_calibration_bundle =  {
                                    "pn" : factoryRepeater.itemAt(0).children[1].children.
                                                filter(function(e){return e.activated === true}).
                                                map(function(e){return e.parameterModel}),
                                    "loss" :  factoryRepeater.itemAt(1).children[1].children.
                                                filter(function(e){return e.activated === true}).
                                                map(function(e){return e.parameterModel}),
                                    "sim" : factoryRepeater.itemAt(2).children[1].children.
                                                filter(function(e){return e.activated === true}).
                                                map(function(e){return e.parameterModel}),
                                    "qb" : factoryRepeater.itemAt(3).children[1].children.
                                            filter(function(e){return e.activated === true}).
                                            map(function(e){return e.parameterModel})
                                    }
                        if(!Object.values(grid_calibration_bundle).every((bundle) => bundle.length > 0)){
                            gridCalibrationErrors.errors = ["Required methods need all to be provided"]
                            gridCalibrationErrors.open()
                            return
                        }
                        try{
                            gridCalibration.gridCalibration(grid_calibration_bundle, [optimizationParameter.parameterModel], weightNSE, weightKGE, fileHandler.ptq)
                        }catch(e){
                            gridCalibrationErrors.errors = [e+""]
                            gridCalibrationErrors.open()
                            console.log(e)
                        }

                    }




                }
            }



       }

    DataErrorsDialog {
        id: gridCalibrationErrors
        title: "❌ ERRORS FOUNDS !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
    }

    FileChoose {
         id: saveGridResultsDialog
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["JSON (*.json)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(saveGridResultsDialog.file.toString());
             gridCalibration.saveSimulationResults(fileName)

         }
         onRejected: {
            console.log("Canceled")
         }
     }
    SplitView {
        id: splitView
        anchors.fill: parent
        background:  Rectangle{
            anchors.fill: parent
            color : "#eaf6f4"
        }

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
            SplitView.minimumWidth:  parent.width*0.3
            SplitView.preferredWidth: parent.width*0.5
            clip : true
            ColumnLayout{
                width: parent.width - 5
                height: parent.height - 5
                anchors.centerIn: parent
                spacing : 10
                //border.width: 1
                Label{
                    id : gridText
                    Layout.preferredWidth: parent.width
                    text: "Grid optimization options"
                    font.bold: true
                    font.pointSize: 10
                    padding: 5
                    color: "black"
                    horizontalAlignment:  Text.AlignHCenter
                    background: Rectangle {
                        anchors.fill: parent
                        topLeftRadius: 5
                        topRightRadius : 5
                        color : "#bae7fe"
                    }
                }
                ScrollView {
                    id: scrollView
                    Layout.preferredWidth: parent.width
                    Layout.preferredHeight: parent.height - gridText.height - parent.spacing
                    clip: true
                    ColumnLayout {
                        width: parent.width
                        height: parent.height
                        spacing: 20

                        Repeater {
                            id: factoryRepeater
                            model: [
                                factoryManager.productionMethods,
                                factoryManager.initialLossMethods,
                                factoryManager.routingMethods,
                                factoryManager.recessionMethods
                            ]
                            property var factoryNames: ["Production", "InitialLoss" , "Routing", "Recession"]

                            delegate: Column {
                                id: contentColumn
                                width: parent.width
                                clip: true
                                spacing: 5

                                property string factoryName: factoryRepeater.factoryNames[model.index]
                                property var methodsList: modelData  // Liste des méthodes pour cette catégorie

                                Label {
                                    text: factoryName + " Methods"
                                    font.bold: true
                                    font.pointSize: 10
                                    padding: 5
                                    color: "black"
                                    horizontalAlignment: Qt.AlignHCenter
                                }
                                Grid {
                                    width: 600
                                    spacing: 10
                                    columns: 2
                                    columnSpacing: 20
                                    rowSpacing: 5
                                    Repeater {
                                        model: methodsList

                                        delegate: GridParameters {
                                            width: 250
                                            height: 150
                                            parameterModel: GridParametersQML{}
                                            factoryName: contentColumn.factoryName
                                            methodName: modelData
                                            border.width: 1
                                            radius: 3
                                            border.color : "grey"
                                        }
                                    }

                                }

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
                    text: "Algorithms"
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

                Row{
                    spacing: 5
                    width: parent.width
                    height: parent.height * 0.2
                    leftPadding: 10
                    Column{
                        height: parent.height
                        width: parent.width*0.5
                        spacing : 10

                        Label{
                            text : "Criteria & Weight"
                            font.bold: true
                        }

                        Rectangle{
                            height: 100
                            width: parent.width *0.7
                            radius: 5
                            color: "#fcffff"
                            border.color: "#ebebeb"
                            border.width: 1
                            Grid{
                                width : parent.width * 0.9
                                height: childrenRect.height
                                anchors.centerIn: parent
                                columns: 2
                                Label {
                                    width: 75
                                    height:  25
                                    text : "NSE"
                                }
                                TextField{
                                    width : 75
                                    height:  25
                                    text : weightNSE + ""
                                    id: metric1
                                    horizontalAlignment: Text.AlignHCenter
                                    validator: DoubleValidator {
                                        bottom: 0
                                        top: 1
                                        notation: DoubleValidator.StandardNotation
                                    }
                                    onTextChanged: {
                                        weightKGE = (1- ( text === "" ? 0 : parseFloat(text))).toFixed(getDigits(text))
                                    }
                                }
                                Label {
                                    width: 75
                                    height:  25
                                    text : "KGE"
                                }
                                TextField{
                                    width : 75
                                    height:  25
                                    text : weightKGE +""
                                    id: metric2
                                    horizontalAlignment: Text.AlignHCenter
                                    validator: DoubleValidator {
                                        bottom: 0
                                        top: 1
                                        notation: DoubleValidator.StandardNotation
                                    }
                                    onTextChanged: {

                                        weightNSE = (1- ( text === "" ? 0 : parseFloat(text))).toFixed(getDigits(text))

                                    }
                                }
                            }



                        }



                    }


                    Column{

                        height: parent.height
                        width: parent.width*0.5 - parent.spacing -2*parent.leftPadding
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
                            model : [gridCalibration?.optimParams]
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
                                            wrapMode: Text.Wrap
                                            font.bold: true
                                            width: parent.width
                                        }


                                        Text {
                                            text: {
                                                let index = Object.keys(pn)[0]
                                                let value = JSON.stringify(pn[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            wrapMode: Text.Wrap
                                            font.bold: true
                                            width: parent.width
                                        }

                                        Text {
                                            text: {
                                                let index = Object.keys(sim)[0]
                                                let value = JSON.stringify(sim[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            wrapMode: Text.Wrap
                                            font.bold: true
                                            width: parent.width
                                        }


                                        Text {
                                            text: {
                                                let index = Object.keys(qb)[0]
                                                let value = JSON.stringify(qb[index]).replace(/"/g, " ");
                                                index + " : " + value
                                            }
                                            wrapMode: Text.Wrap
                                            font.bold: true
                                            width: parent.width
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
                                text : gridCalibration.bestMetrics[0]
                            }
                            Text{
                                text: "Validation : "
                                font.bold: true
                            }
                            Text{
                                width: 50
                                text : gridCalibration.bestMetrics[1]
                            }
                        }



                        Button{
                            id : runOptim
                            anchors.horizontalCenter:  parent.horizontalCenter
                            enabled: Object.keys(gridCalibration?.optimParams).length > 0 ? true : false
                            opacity: enabled ? 1 : 0.7
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
                                console.log("gridCalibration?.optimParams ", JSON.stringify(gridCalibration?.optimParams))
                                saveGridResultsDialog.open()
                            }

                        }


                    }


                }

            }

        }

    }
    function getDigits(nombre){
        let chaineNombre = nombre.toString(); // chaineNombre devient "123.4567"
        let parties = chaineNombre.split('.'); // parties devient ["123", "4567"]

        let nombreDecimal = 0;
        if (parties.length > 1) {
          nombreDecimal = parties[1].length;

        }
        return nombreDecimal
    }
}
