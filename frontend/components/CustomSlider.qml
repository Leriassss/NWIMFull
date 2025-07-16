import QtQuick
import QtQuick.Controls.Basic

Row{
    id:container
    spacing : 5
    property real step: 1
    property real from: 1
    property real to: 100
    //property real value: 25
    property string text :""
    property real value: control.value
    signal releasedAfterPressed

    Label{
        text: container.text
        font.bold: true
        width: 75
        anchors.verticalCenter:  parent.verticalCenter
    }
    Slider {
        id: control
        anchors.verticalCenter:  parent.verticalCenter
        from : container.from
        to : container.to
        stepSize : container.step
        value:50
        onPressedChanged:{
            if(!pressed){
                releasedAfterPressed()
            }

        }

        background: Rectangle {
            x: control.leftPadding
            y: control.topPadding + control.availableHeight / 2 - height / 2
            implicitWidth: 150
            implicitHeight: 4
            width: control.availableWidth
            height: implicitHeight
            radius: 2
            color: "#bdbebf"


            Rectangle {

                width: control.visualPosition * parent.width
                height: parent.height
                color: "#489c9f"
                radius: 2
            }
        }

        handle: Rectangle {
            x: control.leftPadding + control.visualPosition * (control.availableWidth - width)
            y: control.topPadding + control.availableHeight / 2 - height / 2
            implicitWidth: 15
            implicitHeight: 15
            radius: 13
            color: control.pressed ? "#f0f0f0" : "#f6f6f6"
            border.color: "#bdbebf"
        }
    }
    Text{
        anchors.verticalCenter:  parent.verticalCenter
        text : control.value
        width: 50
    }
}

