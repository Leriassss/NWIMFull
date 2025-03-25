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
    width: 1300
    height: 700
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
            anchors.centerIn: parent
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
            anchors.centerIn: parent
            anchors.fill: parent
            color: "white"
            border.width: 1
            QobsComponent{
                anchors.centerIn: parent
                width: parent.width
                height: parent.height *0.9
                padding: 10
            }

        }
        Item {
            id: temp
        }
        Item {
            id: q
        }
        Item {
            id: etp
        }
    }


}
