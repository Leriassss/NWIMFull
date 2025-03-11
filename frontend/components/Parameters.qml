import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
Rectangle {
    id: parameter
    property var comboModel: ["Wmin", "Horton", "Green&Ampt", "Holtan", "Phi"]

    ComboBox {
        id: parameterCombo
        width: parent.width
        height: parent.height * 0.25
        model: parameter.comboModel
    }

    Rectangle {
        id: paramsBox
        anchors.top: parameterCombo.bottom
        width: parent.width
        height: parent.height * 0.75
        border.width: 1
        border.color: "red"
    }
}
