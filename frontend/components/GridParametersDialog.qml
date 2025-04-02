import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./parameters"
import io.qml

Dialog {
    title: "GRID OPTIMIZATION"
    implicitWidth:  1300
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    topInset : 5
    standardButtons: Dialog.Ok | Dialog.Cancel
    closePolicy : Popup.CloseOnEscape
    padding: 5

    SplitView {
        id: splitView
        anchors.fill: parent

        handle: Rectangle {
            implicitWidth: 4
            implicitHeight: 4
            color: SplitHandle.pressed ? "#81e889"
                : (SplitHandle.hovered ? Qt.lighter("#c2f4c6", 1.1) : "#c2f4c6")
            border.width: 1
            border.color: "grey"
        }

        ColumnLayout{
            width: parent.width *0.7
            height: parent.height
            //border.width: 1
            Label{
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height * 0.1
                text: "Methods"
                font.bold: true
                font.pointSize: 12
                padding: 5
                color: "black"
                Layout.alignment: Text.AlignHCenter
                background: Rectangle {
                    anchors.fill: parent
                    border.width: 1
                }
            }
            ScrollView {
                id: scrollView
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height * 0.9
                clip: true

                ColumnLayout {
                    width: parent.width
                    height: parent.height
                    spacing: 20

                    Repeater {
                        id: factoryRepeater
                        model: [
                            factoryManager.productionMethods,
                            factoryManager.recessionMethods,
                            factoryManager.routingMethods,
                            factoryManager.initialLossMethods
                        ]
                        property var factoryNames: ["Production", "Recession", "Routing", "InitialLoss"]

                        delegate: Column {
                            id: contentColumn
                            width: parent.width
                            clip: true
                            spacing: 5

                            property string factoryName: factoryRepeater.factoryNames[model.index]
                            property var methodsList: modelData  // Liste des méthodes pour cette catégorie

                            Label {
                                text: factoryName + " Methods"
                                font.bold: true
                                font.pointSize: 12
                                padding: 5
                                color: "black"
                                horizontalAlignment: Qt.AlignHCenter
                            }
                            Grid {
                                width: 1500
                                spacing: 10
                                columns: 3
                                columnSpacing: 20
                                rowSpacing: 5
                                Repeater {
                                    model: methodsList

                                    delegate: GridParameters {
                                        width: 350
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


        }

        ColumnLayout{
            width: parent.width *0.3 - parent.spacing
            height: parent.height
            Label{
                Layout.preferredWidth: parent.width
                Layout.preferredHeight:  parent.height * 0.1
                text: "Algorithms"
                font.bold: true
                font.pointSize: 12
                padding: 5
                color: "black"
                //horizontalAlignment: Qt.AlignHCenter
                Layout.alignment: Text.AlignHCenter
                background: Rectangle {
                    anchors.fill: parent
                    border.width: 1
                }
            }
            Rectangle {
                Layout.preferredWidth: parent.width
                Layout.preferredHeight: parent.height * 0.9
                border.width: 1
                Column{
                    width: parent.width
                    height: parent.height
                    Parameters{
                        height: parent.height
                        width: parent.width
                        parameterModel : TestQML{}
                        factoryName : "Optimization"
                    }

                }

            }

        }

    }

}
