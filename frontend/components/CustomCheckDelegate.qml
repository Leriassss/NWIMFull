import QtQuick
import QtQuick.Controls.Basic

CheckDelegate {
    id: control
    text: qsTr("CheckDelegate")
    checked: true

    contentItem: Text {
        rightPadding: control.indicator.width + control.spacing
        text: control.text
        font: control.font
        opacity: enabled ? 1.0 : 0.3
        color: "black"
        elide: Text.ElideRight
        verticalAlignment: Text.AlignVCenter
    }

    indicator: Rectangle {
        implicitWidth: 22
        implicitHeight: 22
        x: control.width - width - control.rightPadding
        y: control.topPadding + control.availableHeight / 2 - height / 2
        radius: 3
        color: "transparent"
        border.color: "#17a81a"

        Rectangle {
            width: 10
            height: 10
            x: 6
            y: 6
            radius: 2
            color:"#21be2b"
            visible: control.checked
        }
    }

    background: Rectangle {
        implicitWidth: 100
        implicitHeight: 40
        visible: control.down || control.highlighted
        color: "transparent"
    }
}
