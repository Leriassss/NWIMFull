import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

import "frontend/components"
//import "./frontend/components/parameters"
//import io.qt.test 1.0 as TestModule
//import "io/qt/rangeqarameterqml"
//import io.qt.rangeqarameterqml

ApplicationWindow {
    visible: true
    minimumWidth: 1350
    minimumHeight: 750
    maximumWidth: 1350
    maximumHeight: 750
    title: qsTr("NWIM")
    Material.theme: Material.Light
    Material.accent: Material.Blue

    menuBar:MenuBarModel{
        width: parent.width
        id: nwimMenuBar
        onOpenFileTriggered: {
            fileChooseComponent.openDialog()
        }
        onLoadDataTriggred: {
            //loadDataDialog.show()
            loadDataDialog.open()
        }
        onGapTriggered: {
            gapOptim.open()
        }
        onGridTriggered: {
            gridOptim.open()
        }
    }
    header: ToolBar {
            id: toolBar
            height: 30
            //implicitHeight: 35
            clip: true
            Rectangle{
                color:"#ebebeb"
                border.color: "#6b6b6b"
                border.width: 1

                anchors.fill: parent
                DataErrorsDialog {
                    id: runningErrors
                    title: "❌ ERREURS DETECTEES !!!"
                    standardButtons: Dialog.Ok
                    width: 400
                    height: 300
                    errors : manualCalibration.errors
                }
                Row{
                    anchors.fill: parent
                    spacing: 1
                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("📥")
                        hoverEnabled: true
                        ToolTip.delay: 500
                        ToolTip.timeout: 5000
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Load Parameters")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("💾")
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Save Parameters")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }
                    ToolButton {
                        id: run
                        width: 50
                        height: parent.height
                        hoverEnabled: true
                        checkable: true
                        enabled: fileHandler.activate && homepage.activate === 0 ? true : false
                        text: qsTr("▶️")
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Run Model")

                        property color defaultColor: "transparent"
                        property color hoverColor: "#d6f5e5"
                        property color pressedColor: "#a9e0c2"
                        property color borderColor: "#1fa869"

                        background: Rectangle {
                            id: bg
                            anchors.fill: parent
                            color: run.pressed ? run.pressedColor :
                                   run.hovered ? run.hoverColor :
                                   run.defaultColor
                            border.width: run.hovered  ? 1 : 0
                            border.color: run.hovered ? run.borderColor : "transparent"
                            opacity: 1

                            Behavior on color {
                                ColorAnimation { duration: 75 }
                            }
                            Behavior on border.width {
                                NumberAnimation { duration: 100 }
                            }
                        }

                        // Optionnel : effet visuel à l'appui
                        onPressedChanged: {
                            if (pressed) {
                                bg.scale = 0.95
                            } else {
                                bg.scale = 1.0
                            }
                        }

                        layer.enabled: run.hovered
                        layer.effect: DropShadow {
                            horizontalOffset: 0
                            verticalOffset: 2
                            radius: 4
                            samples: 10
                            color: "#888888"
                        }

                        onClicked: {

                            console.log("------------ HOME PAGE ---------------")
                            console.log(JSON.stringify(homepage.parameter_bundle))
                            //console.log(JSON.stringify(homepage.parameter_bundle2))
                            manualCalibration.setParameters(homepage.parameter_bundle2, fileHandler.ptq)
                            if(manualCalibration.errors.length !==0){
                                console.log(JSON.stringify(manualCalibration.errors))
                                runningErrors.open()
                            }
                            else{
                                homepage.runningClicked()
                            }
                        }
                    }
                    ToolSeparator {}
                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("📆")
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Calibration Length")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                        onClicked: {
                            chooseDatePopup.open()
                        }

                        CalendarDialog{
                            id : chooseDatePopup
                            width: 500
                            height: 200
                            standardButtons: Dialog.Ok | Dialog.Cancel
                            title: qsTr("CHOOSE PERIODS BEGININS")
                            calibration_dates : fileHandler.calendar_dates
                            onAccepted: {
                                fileHandler.updateCalibrationAndValibationDates(chooseDatePopup.user_calibration)
                                if(fileHandler.errors.length !==0){

                                    dataErrorsDialog.open()

                                }
                            }
                        }

                        DataErrorsDialog {
                            id: dataErrorsDialog
                            title: "❌ ERREURS DETECTEES !!!"
                            standardButtons: Dialog.Ok
                            width: 400
                            height: 300
                            errors: fileHandler.errors


                        }

                    }
                    ToolSeparator {}

                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("🧮")
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("ETP Computing")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                        onClicked : {
                            etpComputing.open()
                        }
                    }
                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("🌊")
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("BaseFlow Computing")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }
                    ToolSeparator {}
                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("📈")
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Prediction")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }

                    ToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("🛠️")
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Machine Learning Algorithms")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                        }
                    }
                }
            }


       }

    HomePage{
        id : homepage
        anchors.top: toolBar.bottom
        width: parent.width
        height: parent.height
    }

    footer : Rectangle{
        height: 35
        width: parent.width
        color: "#c0c0ff"
        gradient: Gradient.AwesomePine
    }

    FileChoose{
        id: fileChooseComponent
    }
    LoadData {
        id: loadDataDialog
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
    }
    Optimization{
        id: gapOptim
    }
    GridParametersDialog{
        id:  gridOptim
    }

    ETPComputing{
        id : etpComputing
    }




}
