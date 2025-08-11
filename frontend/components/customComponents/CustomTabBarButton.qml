import QtQuick
import QtQuick.Controls

TabButton {
    property string buttonText: ""
    property string buttonIconSource: ""
    property string buttonIconColor: ""
    property string backgroundColor:""
    anchors.verticalCenter: parent.verticalCenter
    background: Rectangle{
        height: parent.height
        width: parent.width - 1
        color: "#fcffff"

        Rectangle{
            anchors.fill: parent
            border.color: parent.parent.focus ? "#3b7772" : "#fcffff"
            border.width: 1
            Button{
                text: qsTr("  PET")
                icon.source: "../icons/pet.png"
                icon.height: 15
                icon.width: 50
                icon.color: "#000000"
                anchors.centerIn: parent
                width: 75
                background: Rectangle{
                    anchors.fill: parent
                    radius: 5
                    color: "#29888b"
                }
            }
        }
    }
}
