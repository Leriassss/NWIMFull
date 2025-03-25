import QtQuick
import QtQuick.Controls

Row {

    property var statistics:{
        "min" : "",
        "max" : "",
        "mean" : "",
        "std" : ""
    }
    property string periodLabel
    Grid{
        width: parent.width * 0.8
        height: parent.height
        spacing: 25
        columns: 2
        rowSpacing: 0
        columnSpacing: 0
        Column{
            width: parent.width*0.3
            height: parent.height
            Label {
                text: periodLabel
                verticalAlignment: Text.AlignVCenter
            }
        }
        Row {
            width: parent.width*0.7
            height: parent.height
            spacing: 25

            Label {
                text: "Min : "
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: parseFloat(statistics["min"]).toFixed(3)
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: "Max : "
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: parseFloat(statistics["max"]).toFixed(3)
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: "Sum : "
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: parseFloat(statistics["sum"]).toFixed(3)
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: "SD : "
                verticalAlignment: Text.AlignVCenter
            }
            Label {
                text: parseFloat(statistics["std"]).toFixed(3)
                verticalAlignment: Text.AlignVCenter
            }
        }

    }


}
