import QtQuick
import QtQuick.Controls
Row{
    spacing: 6
    Button{
        text: "Load"
        width: parent.width*0.3
        anchors.verticalCenter: parent.verticalCenter
    }
    Button{
        text : "Save"
         width: parent.width*0.3
         anchors.verticalCenter: parent.verticalCenter

    }
    Button{
        text : "Run"
         width: parent.width*0.3
         anchors.verticalCenter: parent.verticalCenter

    }
}
