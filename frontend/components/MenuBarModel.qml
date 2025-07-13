import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

MenuBar {
    signal openFileTriggered
    signal loadDataTriggred
    signal gapTriggered
    signal gridTriggered
    signal regressionTriggered
    signal petTriggered
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
        title: qsTr("Data")
        Action {
            text: qsTr("Import")
            onTriggered: loadDataTriggred()
        }
    }
    Menu {
        title: qsTr("Optimization")
        Action {
            text: qsTr("Algorithms")
            onTriggered: gapTriggered()
        }
        Action {
            text: qsTr("Grid Optimization")
            onTriggered: gridTriggered()
        }
    }
    Menu {
        title: qsTr("Tools")
        Action {
            text: qsTr("PET Computing")
            onTriggered: petTriggered()
        }
        Action {
            text: qsTr("Baseflow Computing")
        }
        Action {
            text: qsTr("Machine Learning")
            onTriggered: regressionTriggered()
        }
        Action {
            text: qsTr("Smoothness")
        }
    }
    Menu {
        title: qsTr("&Help")
        Action { text: qsTr("About") }
    }
}
