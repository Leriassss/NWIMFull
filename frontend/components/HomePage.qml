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
    id: homePage
    color : "#ebebeb"
    property var parameter_bundle: {
        "pn":production_params.parameters,
        "qb":recession_params.parameters,
        "sim": routing_params.parameters,
        "loss" : loss_params.parameters
    }
    property var parameter_bundle2: {
        "pn":production_params.parameterModel,
        "qb":recession_params.parameterModel,
        "sim": routing_params.parameterModel,
        "loss" : loss_params.parameterModel
    }
    property int activate: production_params.checkPassed +
                           recession_params.checkPassed +
                           routing_params.checkPassed +
                           loss_params.checkPassed

    signal runningClicked
    Row {
        anchors.fill: parent
        id: splitView
        //spacing: 5
        clip: true
            Rectangle{
                width: parent.width * 0.2
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
                        //enabled: fileHandler.activate ? true : false
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
                                        font.pointSize: 10
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
                                        font.pointSize: 10
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
                                        font.pointSize: 10
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
                width: parent.width * 0.8 - parent.spacing
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
                                                id : calibrationCheckBox
                                                text: "CALIBRATION"
                                                checked: true
                                                anchors.centerIn: parent
                                                font.bold: true
                                                font.pointSize: 10
                                                onCheckedChanged: {
                                                    homepage.runningClicked()
                                                }

                                            }
                                        }
                                        Grid{
                                            width: parent.width
                                            height:  parent.height * 0.7
                                            columns: 2
                                            leftPadding: 10
                                            Column{
                                                width: parent.width*0.15
                                                height:  parent.height
                                                Label{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    text: "Bilan"
                                                    font.bold: true
                                                    font.pointSize: 10
                                                    color: "black"
                                                }
                                                Label{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    text: "Criteria"
                                                    font.bold: true
                                                    font.pointSize: 10
                                                    color: "black"
                                                }
                                            }
                                            Column{
                                                width: parent.width*0.85
                                                height:  parent.height
                                                Row{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    spacing: 10
                                                    property real labWidth: 40

                                                    Label{
                                                        text: "P : "
                                                    }
                                                    Label{
                                                        id : calibration_rainfall_sum
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text: "I : "
                                                    }
                                                    Label{
                                                        id : calibration_infiltration_sum
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text : "DS : "
                                                    }
                                                    Label{
                                                        id : calibration_stock_sum
                                                        width: parent.labWidth
                                                    }
                                                }

                                                Row{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    property real labWidth: 40
                                                    spacing: 5
                                                    Label{
                                                        text: "NSE : "
                                                    }
                                                    Label{
                                                        text: manualCalibration.simulationValues["CRITERIA"]["CALIBRATION"]["NSE"]
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text: "KGE : "
                                                    }
                                                    Label{
                                                        text: manualCalibration.simulationValues["CRITERIA"]["CALIBRATION"]["KGE"]
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text : "MAE : "
                                                    }
                                                    Label{
                                                        text : manualCalibration.simulationValues["CRITERIA"]["CALIBRATION"]["MAE"]
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text : "R2 : "
                                                    }
                                                    Label{
                                                        text : manualCalibration.simulationValues["CRITERIA"]["CALIBRATION"]["R2"]
                                                        width: parent.labWidth
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
                                                id : validationCheckBox
                                                text: "VALIDATION"
                                                checked: true
                                                anchors.centerIn: parent
                                                font.bold: true
                                                font.pointSize: 10
                                                onCheckedChanged: {
                                                    homepage.runningClicked()
                                                }
                                            }
                                        }
                                        Grid{
                                            width: parent.width
                                            height:  parent.height * 0.7
                                            columns: 2
                                            leftPadding: 10
                                            Column{
                                                width: parent.width*0.15
                                                height:  parent.height
                                                Label{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    text: "Bilan"
                                                    font.bold: true
                                                    font.pointSize: 10
                                                    color: "black"
                                                }
                                                Label{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    text: "Criteria"
                                                    font.bold: true
                                                    font.pointSize: 10
                                                    color: "black"
                                                }
                                            }
                                            Column{
                                                width: parent.width*0.85
                                                height:  parent.height
                                                Row{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    spacing: 10
                                                    property real labWidth: 40

                                                    Label{
                                                        text: "P : "
                                                    }
                                                    Label{
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text: "I : "
                                                    }
                                                    Label{
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text : "DS : "
                                                    }
                                                    Label{
                                                        width: parent.labWidth
                                                    }
                                                }

                                                Row{
                                                    width: parent.width
                                                    height:  parent.height *0.5
                                                    property real labWidth: 40
                                                    spacing: 5
                                                    Label{
                                                        text: "NSE : "

                                                    }
                                                    Label{
                                                        text: manualCalibration.simulationValues["CRITERIA"]["VALIDATION"]["NSE"]
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text: "KGE : "

                                                    }
                                                    Label{
                                                        text: manualCalibration.simulationValues["CRITERIA"]["VALIDATION"]["KGE"]
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text : "MAE : "

                                                    }
                                                    Label{
                                                        text : manualCalibration.simulationValues["CRITERIA"]["VALIDATION"]["MAE"]
                                                        width: parent.labWidth
                                                    }
                                                    Label{
                                                        text : "R2 : "

                                                    }
                                                    Label{
                                                        text : manualCalibration.simulationValues["CRITERIA"]["VALIDATION"]["R2"]
                                                        width: parent.labWidth
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
                            id: simChart
                            width: parent.width
                            height: parent.height

                            Connections {
                                target: homePage
                                function onRunningClicked(){
                                    //console.log("------------- SIMCHART RUNNIG---------------")
                                    //console.log(JSON.stringify(manualCalibration.simulationValues))
                                    let dates = manualCalibration.simulationValues["DATES"]
                                    let q_obs = manualCalibration.simulationValues["OBS"]
                                    let q_sim = manualCalibration.simulationValues["SIM"]
                                    if (calibrationCheckBox.checked && validationCheckBox.checked){
                                        simChart.updateChart([...dates["CALIBRATION"], ...dates["VALIDATION"]],
                                                    [...q_obs["CALIBRATION"], ...q_obs["VALIDATION"]],
                                                    [...q_sim["CALIBRATION"], ...q_sim["VALIDATION"]])
                                    }
                                    else if(calibrationCheckBox.checked && !validationCheckBox.checked){
                                        simChart.updateChart([...dates["CALIBRATION"]],
                                                    [...q_obs["CALIBRATION"]],
                                                    [...q_sim["CALIBRATION"]])
                                    }
                                    else if(!calibrationCheckBox.checked && validationCheckBox.checked){
                                        simChart.updateChart([...dates["VALIDATION"]],
                                                    [...q_obs["VALIDATION"]],
                                                    [...q_sim["VALIDATION"]])
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }

}

