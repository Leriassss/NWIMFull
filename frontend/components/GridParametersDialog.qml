import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./parameters"
import io.qml

Dialog {
    title: "OPTIMIZATION"
    implicitWidth:  1300
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    topInset : 5
    standardButtons: Dialog.Ok | Dialog.Cancel
    closePolicy : Popup.CloseOnEscape
    padding: 5

    ScrollView {
        id: scrollView
        width: parent.width *0.6
        height: parent.height
        clip: true

        ColumnLayout {
            width: parent.width
            height: parent.height

            Repeater {
                id: factoryRepeater
                model: [
                    factoryManager.productionMethods,
                    factoryManager.recessionMethods,
                    factoryManager.routingMethods,
                    factoryManager.initialLossMethods
                ]
                property var factoryNames: ["Production", "Recession", "Routing", "InitialLoss"]

                delegate: Row {
                    id: contentColumn
                    width: parent.width * 0.25
                    clip: true

                    property string factoryName: factoryRepeater.factoryNames[model.index]
                    property var methodsList: modelData  // Liste des méthodes pour cette catégorie

                    /*Label {
                        text: factoryName + " Methods"
                        font.bold: true
                        font.pointSize: 12
                        padding: 5
                        color: "black"
                        horizontalAlignment: Qt.AlignHCenter
                    }*/
                    Repeater {
                        model: methodsList

                        delegate: GridParameters {
                            width: 400
                            height: 150
                            parameterModel: GridParametersQML{}
                            factoryName: contentColumn.factoryName
                            methodName: modelData
                            border.width: 1
                        }
                    }
                }
            }
        }
    }
}
