import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

MenuBar {
    signal openFileTriggered
    signal loadDataTriggred
    signal gapTriggered
    Menu {
        title: qsTr("File")
        Action {
            text: qsTr("Open...")
            onTriggered: openFileTriggered()
        }
        MenuSeparator { }
        Action { text: qsTr("Quit") }
    }
    Menu {
        title: qsTr("&Data")
        Action {
            text: qsTr("&Edit")
            onTriggered: loadDataTriggred()
        }
    }
    Menu {
        title: qsTr("&Optimization")
        Action {
            text: qsTr("GAP Optimization")
            onTriggered: gapTriggered()
        }
        Action { text: qsTr("&DE Optimization") }
        Action { text: qsTr("&LatinHypercube Optimization") }
    }
    Menu {
        title: qsTr("&Regression")
        Action { text: qsTr("&Edit") }
    }
    Menu {
        title: qsTr("&Help")
        Action { text: qsTr("&About") }
    }
}
