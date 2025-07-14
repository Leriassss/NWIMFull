import QtQuick
import QtQuick.Controls


TextField{

    background : Rectangle {
        // Fond transparent
        color: "transparent"

        // Bordure inférieure seule
        Rectangle {
            anchors.bottom: parent.bottom
            width: parent.width
            height: 1
            color:  "#bdbebf"
            border.color: "grey"
            border.width: 1
        }


     }
}
