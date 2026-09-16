import QtQuick
import Qt5Compat.GraphicalEffects
import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
ToolButton {
    id: run
    hoverEnabled: true
    checkable: true
    enabled: true
    ToolTip.visible: hovered

    property color defaultColor: "transparent"
    property color hoverColor: "#d6f5e5"
    property color pressedColor: "#a9e0c2"
    property color borderColor: "#1fa869"

    background: Rectangle {
        id: bg
        anchors.fill: parent
        color: run.pressed && run.enabled ? run.pressedColor :
               run.hovered && run.enabled ? run.hoverColor :
               run.defaultColor
        border.width: run.hovered && run.enabled ? 1 : 0
        border.color: run.hovered && run.enabled ? run.borderColor : "transparent"
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
        if (pressed && enabled) {
            bg.scale = 0.95
        } else {
            bg.scale = 1.0
        }
    }

    layer.enabled: run.hovered && run.enabled
    layer.effect: DropShadow {
        horizontalOffset: 0
        verticalOffset: 2
        radius: 4
        samples: 10
        color: "#888888"
    }
}
