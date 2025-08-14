import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import ".."
import "../datasetComponents"
import io.qml



Dialog{
    //visible: true
    id: loadDataDialog
    title: "DATA"
    implicitWidth:  1300
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    standardButtons: Dialog.Ok
    closePolicy : Popup.CloseOnEscape
    background:Rectangle{
        anchors.fill: parent
        color: "#bae7fe"
    }

    header:TabBar {
        id: bar
        width: parent.width
        height: 35
        TabButton {
            id : loadTabButton
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter

            background: Rectangle{
                height: parent.height
                width: parent.width - 1
                color: "#fcffff"

                Rectangle{
                    anchors.fill: parent
                    color: parent.parent.focus ? "#bae7fe" : "#fcffff"
                    Button{
                        hoverEnabled: false
                        text: qsTr("    Load")
                        icon.source: "../../icons/load.png"
                        icon.height: 15
                        icon.width: 50
                        icon.color: "#000000"
                        anchors.centerIn: parent
                        width: 75

                        background: Rectangle{
                            anchors.fill: parent
                            radius: 5
                            color: "#fcffff"
                        }
                    }
                }
            }
        }
        TabButton {
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            background: Rectangle{
                height: parent.height
                width: parent.width - 1
                color: "#fcffff"

                Rectangle{
                    anchors.fill: parent
                    color: parent.parent.focus ? "#bae7fe" : "#fcffff"
                    Button{
                        hoverEnabled: false
                        text: qsTr("    P")
                        icon.source: "../../icons/rainfall.png"
                        icon.height: 15
                        icon.width: 50
                        icon.color: "#000000"
                        anchors.centerIn: parent
                        width: 75
                        background: Rectangle{
                            anchors.fill: parent
                            radius: 5
                            color: "#fcffff"
                        }
                    }
                }
            }
        }
        /*TabButton {
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            background: Rectangle{
                height: parent.height
                width: parent.width - 1
                color: "#fcffff"

                Rectangle{
                    anchors.fill: parent
                    color: parent.parent.focus ? "#bae7fe" : "#fcffff"
                    Button{
                        hoverEnabled: false
                        text: qsTr("    T")
                        icon.source: "../icons/tmin.png"
                        icon.height: 15
                        icon.width: 50
                        icon.color: "#000000"
                        anchors.centerIn: parent
                        width: 75
                        background: Rectangle{
                            anchors.fill: parent
                            radius: 5
                            color: "#fcffff"
                        }
                    }
                }
            }
        }
        */
        TabButton {
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            background: Rectangle{
                height: parent.height
                width: parent.width - 1
                color: "#fcffff"

                Rectangle{
                    anchors.fill: parent
                    color: parent.parent.focus ? "#bae7fe" : "#fcffff"
                    Button{
                        hoverEnabled: false
                        text: qsTr("    Q")
                        icon.source: "../../icons/streamflow.png"
                        icon.height: 15
                        icon.width: 50
                        icon.color: "#000000"
                        anchors.centerIn: parent
                        width: 75
                        background: Rectangle{
                            anchors.fill: parent
                            radius: 5
                            color: "#fcffff"
                        }
                    }
                }
            }
        }
        TabButton {
            height: parent.height
            anchors.verticalCenter: parent.verticalCenter
            background: Rectangle{
                height: parent.height
                color: "#fcffff"

                Rectangle{
                    anchors.fill: parent
                    color: parent.parent.focus ? "#bae7fe" : "#fcffff"
                    Button{
                        hoverEnabled: false
                        text: qsTr("  PET")
                        icon.source: "../../icons/pet.png"
                        icon.height: 15
                        icon.width: 50
                        icon.color: "#000000"
                        anchors.centerIn: parent
                        width: 75
                        background: Rectangle{
                            anchors.fill: parent
                            radius: 5
                            color: "#fcffff"
                        }
                    }
                }
            }
        }

    }

    StackLayout {
        anchors.fill: parent
        currentIndex: bar.currentIndex
        anchors.centerIn: parent
        Rectangle{
            Layout.alignment : Qt.AlignCenter
            anchors.fill: parent
            color: "white"
            border.width: 1
            LoadDataComponent{
                width: parent.width
                height: parent.height
            }

        }
        Rectangle{
            Layout.alignment : Qt.AlignCenter
            anchors.fill: parent
            color: "white"
            border.width: 1
            RainComponent{
                width: parent.width
                height: parent.height *0.9
                padding: 10
            }

        }
        /*Rectangle{
            Layout.alignment : Qt.AlignCenter
            anchors.fill: parent
            color: "white"
            border.width: 1
            TempComponent{
                width: parent.width
                height: parent.height *0.9
                padding: 10
            }

        }*/

        Rectangle{
            Layout.alignment : Qt.AlignCenter
            anchors.fill: parent
            color: "white"
            border.width: 1
            QobsComponent{
                width: parent.width
                height: parent.height *0.9
                padding: 10
            }

        }
        Rectangle{
            Layout.alignment : Qt.AlignCenter
            anchors.fill: parent
            color: "white"
            border.width: 1
            ETPComponent{
                width: parent.width
                height: parent.height *0.9
                padding: 10
            }

        }
    }


}
