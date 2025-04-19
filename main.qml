import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

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
                        width: 50
                        height: parent.height
                        hoverEnabled: true
                        ToolTip.visible: hovered
                        ToolTip.text: qsTr("Run Model")
                        text: qsTr("▶️")
                        background: Rectangle{
                            anchors.fill: parent
                            color: "transparent"
                            opacity: ToolButton.hovered ? 1 : 0.3
                        }
                        onClicked: {
                            console.log("------------ HOME PAGE ---------------")
                            console.log(JSON.stringify(homepage.parameter_bundle))
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
    }
    Optimization{
        id: gapOptim
    }
    GridParametersDialog{
        id:  gridOptim
    }




}
