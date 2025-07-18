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
    standardButtons: Dialog.Ok | Dialog.Cancel
    closePolicy : Popup.CloseOnEscape

    background:Rectangle{
        anchors.fill: parent
        color: "#fcffff"
    }
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
                            ToolTip.text: qsTr("Load Parameters")
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
                                            width: 90
                                            height: 30
                                            radius: 5
                                            color: run.pressed ? run.pressedColor :run.defaultColor
                                            anchors.centerIn: parent
                                            border.width: run.pressed  ? 1 : 0
                                            border.color: run.pressed ? run.borderColor : "transparent"
                                        }


                                        onClicked: {


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
                            text: qsTr("▶️")
                            ToolTip.text: qsTr("Optimize")
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

                        }

                    }
                }
            }
        }


    function chartMapping(){
        //console.log("------------- SIMCHART RUNNIG---------------")
        //console.log(JSON.stringify(manualCalibration.simulationValues))
        let dates = manualCalibration.simulationValues["DATES"]
        let q_obs = manualCalibration.simulationValues["OBS"]
        let q_sim = manualCalibration.smoothnessValues

        baseflowChart.updateChart([...dates["VALIDATION"]],
                    [...q_obs["VALIDATION"]],
                    [...q_sim["VALIDATION"]])
    }


}
