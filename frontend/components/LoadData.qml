import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import "."
import "datasetComponents"
import io.qml



Dialog{
    //visible: true
    id: loadDataDialog
    title: "DATA"
    implicitWidth:  1300
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    topInset : 5
    standardButtons: Dialog.Ok | Dialog.Cancel
    closePolicy : Popup.CloseOnEscape

    header:TabBar {
        id: bar
        width: parent.width

        TabButton {
            text: qsTr("Load")
        }
        TabButton {
            text: qsTr("P")
        }
        TabButton {
            text: qsTr("T")
        }
        TabButton {
            text: qsTr("Q")
        }
        TabButton {
            text: qsTr("ETP")
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
                anchors.centerIn: parent
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
            RainComponent{
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
            TempComponent{
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
