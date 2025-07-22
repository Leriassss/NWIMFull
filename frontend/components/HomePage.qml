import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import QtQuick.Effects
import Qt5Compat.GraphicalEffects
import "."
import "./parameters"
import "./chartsComponents"

//import "../../io/qml"
import io.qml
Rectangle{
    id: homePage
    color : "#ffffff"
    border.color: "#ebebeb"
    border.width: 1
    clip: true
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

    property color siderbarColor: "#bae7fe"
    property color sidebarTextColor: "black"

    DataErrorsDialog {
        id: runningErrors
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
                width: parent.width * 0.17
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
                        text: "PARAMETERS"
                        //font.bold: true
                        font.pointSize: 10
                        //topPadding: 20
                        padding: 5
                        color: "black"
                        width: parent.width

                        /*background: Rectangle{
                            color: "#d2d2d2"
                            width: parent.width
                            height: parent.height
                        }*/
                    }




                    Rectangle{
                        width: parent.width*0.9
                        height: 1
                        color: "#aaaaaa"
                        anchors.horizontalCenter: parent.horizontalCenter
                    }


                    Rectangle {
                        id: simParameters
                        width: parent.width
                        height: parent.height * 0.8
                        //color : siderbarColor
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
                                color : siderbarColor
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
                                        color: sidebarTextColor
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
                                color : siderbarColor
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
                                        color: sidebarTextColor
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
                                color : siderbarColor
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
                                }

                            }


                        }
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
                            enabled: true
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
                                width: 100
                                height: 50
                                radius: 5
                                color: run.pressed ? run.pressedColor :run.defaultColor
                                border.width: run.pressed  ? 1 : 0
                                border.color: run.pressed ? run.borderColor : "transparent"
                            }


                            onClicked: {

                                console.log("------------ HOME PAGE ---------------")
                                console.log(JSON.stringify(homepage.parameter_bundle))
                                //console.log(JSON.stringify(homepage.parameter_bundle2))
                                console.log("STEP 0-0 FRONT ", Date(Date.now()))
                                manualCalibration.setParameters(homepage.parameter_bundle2, fileHandler.ptq)
                                console.log("STEP 0-1 FRONT ", Date(Date.now()))
                                if(manualCalibration.errors.length !==0){
                                    console.log(JSON.stringify(manualCalibration.errors))
                                    runningErrors.errors = manualCalibration.errors
                                    runningErrors.open()
                                }
                                else{
                                    runningClicked()
                                }
                                console.log("STEP F FRONT ", Date(Date.now()))
                            }
                        }


                    }
                }
            }


            Rectangle {
                color: "#fcffff"
                id: simulationPane
                width: parent.width * 0.83 - parent.spacing
                height: parent.height
                //border.width: 1
                anchors.right: parent.right
                //color: "#d2d2d2"
                /*gradient: Gradient {
                    GradientStop { position: 0.0; color: "#cecece" } // bord haut-gauche
                    GradientStop { position: 1.0; color: "#f0f0f0" } // bord bas-droit
                }*/
                ColumnLayout {
                    width: parent.width
                    height: parent.height
                    spacing: 25

                    Rectangle {
                        id: plotOptions
                        Layout.preferredWidth:  parent.width
                        Layout.preferredHeight:  parent.height*0.2
                        Column {
                            width: parent.width
                            height: parent.height
                            Rectangle {
                                width: parent.width
                                height: parent.height *0.25
                                color : "#fcffff"
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
                                }
                            }
                            Row {
                                id: parameterGrid
                                width: parent.width
                                height: parent.height *0.75
                                spacing : 20
                                Rectangle{
                                    width: parent.width * 0.5
                                    height:  parent.height
                                    color: "#dbf3fe"
                                    radius : 5
                                    border.color: "#ebebeb"
                                    border.width: 1
                                    //layer.enabled: true
                                    layer.effect: DropShadow {
                                        horizontalOffset: 0
                                        verticalOffset: 1
                                        radius: 4
                                        samples: 10
                                        color: "#888888"
                                    }
                                    /*layer.enabled: true
                                    layer.effect: MultiEffect {
                                        shadowEnabled: true
                                        shadowColor: "#ebebeb"
                                    }*/
                                    Column{
                                        anchors.fill: parent
                                        spacing: 10
                                        Rectangle{
                                            color: "transparent"
                                            width: parent.width
                                            height:  35
                                            CustomCheckDelegate{
                                                id : calibrationCheckBox
                                                text: "Calibration"
                                                checked: true
                                                anchors.centerIn: parent
                                                font.bold: true
                                                font.pointSize: 10
                                                onCheckedChanged: {
                                                    homepage.runningClicked()
                                                }

                                            }
                                        }
                                        Row{
                                            width: parent.width
                                            height:  parent.height * 0.7
                                            spacing: 10
                                            leftPadding:  10
                                            Rectangle{
                                                color: "#ffffff"
                                                width: (parent.width -parent.spacing-parent.leftPadding) * 0.5
                                                height:  parent.height * 0.7
                                                radius : 5
                                                Grid{
                                                    width: parent.width * 0.5
                                                    height:  parent.height * 0.7
                                                    rowSpacing: 10
                                                    columns: 4
                                                    leftPadding: 10
                                                    property real labWidth: 40
                                                        //spacing: 5
                                                        Text{
                                                            text: "NSE : "

                                                        }
                                                        Label{
                                                            text: manualCalibration.simulationValues["CRITERIA"]["CALIBRATION"]["NSE"]
                                                            width: parent.labWidth
                                                        }
                                                        Text{
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
                                                            text : "RMSE : "
                                                        }
                                                        Label{
                                                            text : manualCalibration.simulationValues["CRITERIA"]["CALIBRATION"]["RMSE"]
                                                            width: parent.labWidth
                                                        }
                                                }

                                            }
                                            Rectangle{
                                                color: "white"
                                                width: (parent.width -parent.spacing-parent.leftPadding) * 0.5 -parent.spacing
                                                height:  parent.height * 0.7
                                                radius : 5
                                                Grid{
                                                    width: parent.width * 0.5
                                                    height:  parent.height * 0.7
                                                    columns : 4
                                                    leftPadding: 10
                                                    property real labWidth: 40
                                                    rowSpacing: 10
                                                        Label{
                                                            text: "P : "
                                                        }
                                                        Label{
                                                            text: ""
                                                            width: parent.labWidth
                                                        }
                                                        Label{
                                                            text: "I : "
                                                        }
                                                        Label{
                                                            text: ""
                                                            width: parent.labWidth
                                                        }
                                                        Label{
                                                            text : "R : "
                                                        }
                                                        Label{
                                                            text : ""
                                                            width: parent.labWidth
                                                        }
                                                        Label{
                                                            text : "DS : "
                                                        }
                                                        Label{
                                                            text : ""
                                                            width: parent.labWidth
                                                        }
                                                }

                                            }

                                        }

                                    }

                                }

                                Rectangle{
                                    width: parent.width * 0.5 - parent.spacing * 2
                                    height:  parent.height
                                    color: "#e2f7f4"
                                    border.color: "#ebebeb"
                                    border.width: 1
                                    radius : 5
                                    //layer.enabled: true
                                    layer.effect: DropShadow {
                                        horizontalOffset: 0
                                        verticalOffset: 1
                                        radius: 4
                                        samples: 10
                                        color: "#888888"
                                    }
                                    Column{
                                        anchors.fill: parent
                                        spacing: 10
                                        Rectangle{
                                            color: "transparent"
                                            width: parent.width
                                            height:  35
                                            CustomCheckDelegate{
                                                id : validationCheckBox
                                                text: "Validation"
                                                checked: true
                                                anchors.centerIn: parent
                                                font.bold: true
                                                font.pointSize: 10
                                                onCheckedChanged: {
                                                    homepage.runningClicked()
                                                }

                                            }
                                        }
                                        Row{
                                            width: parent.width
                                            height:  parent.height * 0.7
                                            spacing: 10
                                            leftPadding:  10
                                            Rectangle{
                                                color: "#fcffff"
                                                width: (parent.width -parent.spacing-parent.leftPadding) * 0.5
                                                height:  parent.height * 0.7
                                                radius : 5
                                                Grid{
                                                    width: parent.width * 0.5
                                                    height:  parent.height * 0.7
                                                    columns: 4
                                                    leftPadding: 10
                                                    property real labWidth: 40
                                                    rowSpacing: 10
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
                                                            text : "RMSE : "
                                                        }
                                                        Label{
                                                            text : manualCalibration.simulationValues["CRITERIA"]["VALIDATION"]["RMSE"]
                                                            width: parent.labWidth
                                                        }
                                                }

                                            }
                                            Rectangle{
                                                color: "white"
                                                width: (parent.width -parent.spacing-parent.leftPadding) * 0.5 -parent.spacing
                                                height:  parent.height * 0.7
                                                radius : 5
                                                Grid{
                                                    width: parent.width * 0.5
                                                    height:  parent.height * 0.7
                                                    rows: 2
                                                    leftPadding: 10
                                                    property real labWidth: 40
                                                    rowSpacing: 10
                                                        Label{
                                                            text: "P : "
                                                        }
                                                        Label{
                                                            text: ""
                                                            width: parent.labWidth
                                                        }
                                                        Label{
                                                            text: "I : "
                                                        }
                                                        Label{
                                                            text: ""
                                                            width: parent.labWidth
                                                        }
                                                        Label{
                                                            text : "R : "
                                                        }
                                                        Label{
                                                            text : ""
                                                            width: parent.labWidth
                                                        }
                                                        Label{
                                                            text : "DS : "
                                                        }
                                                        Label{
                                                            text : ""
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

                    RowLayout{
                        id : smoothness
                        Layout.preferredWidth:  parent.width
                        Layout.preferredHeight:  5
                        spacing : 50
                        CustomCheckDelegate{
                            id: smoothChecked
                            checked: false
                            anchors.verticalCenter:  parent.verticalCenter
                        }

                        CustomSlider{
                            id :slideSmoothing
                            enabled: smoothChecked.checked
                            Layout.preferredWidth: 300
                            Layout.preferredHeight: parent.height
                            step: 0.5
                            from: 0
                            to: 100
                            text: "Smoothing"
                            anchors.verticalCenter:  parent.verticalCenter
                            onReleasedAfterPressed: {
                                console.log("**********")
                                console.log(value)
                                chartMapping()
                            }

                        }
                        CustomCheckDelegate{
                            id: slideChecked
                            checked: false
                            anchors.verticalCenter:  parent.verticalCenter
                        }
                        CustomSlider{
                            id :slideRolling
                            enabled: slideChecked.checked
                            Layout.preferredWidth: 300
                            Layout.preferredHeight: parent.height
                            step: 1
                            from: 1
                            to: 100
                            //value: 25
                            text: "Rolling"
                            anchors.verticalCenter:  parent.verticalCenter
                            onReleasedAfterPressed: {
                                console.log("**********")
                                console.log(value)
                                chartMapping()
                            }

                        }
                    }

                    Column {
                        id: plot
                        Layout.preferredWidth:  parent.width
                        Layout.preferredHeight:  parent.height * 0.8 - parent.spacing - smoothness.height
                        clip : true

                        SimChart{
                            id: simChart
                            width: parent.width
                            height: parent.height

                            Connections {
                                target: homePage
                                function onRunningClicked(){
                                    chartMapping()
                                }
                            }

                        }

                    }
                }
            }
        }


    function chartMapping(){
        //console.log("------------- SIMCHART RUNNIG---------------")
        //console.log(JSON.stringify(manualCalibration.simulationValues))
        let rolling = slideRolling.enabled ? parseInt(slideRolling.value) : 0
        let smoothing = slideSmoothing.enabled ? parseFloat(slideSmoothing.value) : 0
        manualCalibration.smoothness(manualCalibration.simulationValues, smoothing, rolling)
        let dates = manualCalibration.simulationValues["DATES"]
        let q_obs = manualCalibration.simulationValues["OBS"]
        let q_sim = manualCalibration.smoothnessValues

        console.log("STEP 2 FRONT ", Date(Date.now()))
        if (calibrationCheckBox.checked && validationCheckBox.checked){
            console.log("STEP 3 FRONT ", Date(Date.now()))
            simChart.updateChart([...dates["CALIBRATION"], ...dates["VALIDATION"]],
                        [...q_obs["CALIBRATION"], ...q_obs["VALIDATION"]],
                        dates["CALIBRATION"],q_sim["CALIBRATION"],
                        dates["VALIDATION"], q_sim["VALIDATION"])

            console.log("STEP 4 FRONT ", Date(Date.now()))
        }
        else if(calibrationCheckBox.checked && !validationCheckBox.checked){
            simChart.updateChart(dates["CALIBRATION"],q_obs["CALIBRATION"],
                                 dates["CALIBRATION"],q_sim["CALIBRATION"],[],[])
        }
        else if(!calibrationCheckBox.checked && validationCheckBox.checked){
            simChart.updateChart(dates["VALIDATION"],q_obs["VALIDATION"],[],[],
                                 dates["VALIDATION"],q_sim["VALIDATION"])
        }
    }
}

