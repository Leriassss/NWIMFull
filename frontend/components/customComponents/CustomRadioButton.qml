import QtQuick
import QtQuick.Controls.Basic

RadioButton {
    id: control

    indicator: Rectangle {
        implicitWidth: 26
        implicitHeight: 26
        x: control.leftPadding
        y: parent.height / 2 - height / 2
        radius: 13
        border.color:  "#0b7878"

        Rectangle {
            width: 14
            height: 14
            x: 6
            y: 6
            radius: 7
            color: "#0b7878"
            visible: control.checked
        }
    }

    contentItem: Text {
        text: control.text
        font: control.font
        opacity: enabled ? 1.0 : 0.3
        verticalAlignment: Text.AlignVCenter
        leftPadding: control.indicator.width + control.spacing
    }
}
