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
    signal saveTriggered
    signal baseFlowTriggered
    Menu {
        title: qsTr("File")
        Action {
            text: qsTr("Load Parameters File")
            onTriggered: openFileTriggered()
        }
        Action {
            text: qsTr("Save")
            onTriggered: saveTriggered()
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
            onTriggered: baseFlowTriggered()
        }
        Action {
            text: qsTr("Machine Learning")
            onTriggered: regressionTriggered()
        }

    }
    Menu {
        title: qsTr("&Help")
        Action { text: qsTr("About") }
    }
}
