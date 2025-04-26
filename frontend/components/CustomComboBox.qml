import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects
import QtQuick.Effects
ComboBox {
    id: methodSelector

    /**/

    background: Rectangle{
        anchors.fill: parent
        //color: "#ebebeb"
        border.width: 1
        border.color: "grey"
        gradient: Gradient {
                            GradientStop { position: 0.0; color: "#dddddd" } // bord haut-gauche
                            GradientStop { position: 1.0; color: "#ebebeb" } // bord bas-droit
                        }
    }
    popup: Popup {
        y: methodSelector.height - 1
        width: methodSelector.width
        height: Math.min(contentItem.implicitHeight, methodSelector.Window.height - topMargin - bottomMargin)
        padding: 1

        contentItem: ListView {
            clip: true
            implicitHeight: contentHeight
            model: methodSelector.popup.visible ? methodSelector.delegateModel : null
            currentIndex: methodSelector.highlightedIndex


            ScrollIndicator.vertical: ScrollIndicator { }
        }

        background: Rectangle {
            id : rec
            border.color: "#21be2b"
            layer.enabled: rec.hovered
            layer.effect: DropShadow {
                horizontalOffset: 1
                verticalOffset: 5
                radius: 4
                samples: 20
                color: "red"//"#888888"
            }
        }

    }

    indicator: Canvas {
           id: canvas
           x: methodSelector.width - width - methodSelector.rightPadding
           y: methodSelector.topPadding + (methodSelector.availableHeight - height) / 2
           width: 12
           height: 8
           contextType: "2d"

           Connections {
               target: methodSelector
               function onPressedChanged() { canvas.requestPaint(); }
           }

           onPaint: {
               context.reset();
               context.moveTo(0, 0);
               context.lineTo(width, 0);
               context.lineTo(width / 2, height);
               context.closePath();
               context.fillStyle = methodSelector.pressed ? "#17a81a" : "#21be2b";
               context.fill();
           }
       }

}
