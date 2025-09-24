import QtQuick
import QtQuick.Controls
Dialog {
    id: dataErrorsDialog
    standardButtons: Dialog.Ok
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    property var errors: []

    Rectangle{
        anchors.fill: parent
        border.width: 1
        ListView {
            id: errorListView
            model: dataErrorsDialog.errors
            anchors.fill: parent
            delegate: Item {
                width: errorListView.width
                height: 30
                Rectangle {
                    width: parent.width
                    height: parent.height
                    //color: "lightgray"
                    border.color: "gray"
                    Text {
                        width: parent.width
                        anchors.left: parent.left
                        anchors.verticalCenter: parent.verticalCenter
                        padding: 5
                        text: modelData
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }

        }
}
