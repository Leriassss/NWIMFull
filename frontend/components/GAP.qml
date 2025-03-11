import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15


Dialog {
    title: "GAP OPTIMIZATION"
    modal: true
    width: 1000
    height: 700
    standardButtons: Dialog.Ok | Dialog.Cancel
    padding: 5
    onOpened: {
        gaModel.setMethod(methodSelector.currentIndex)
    }

    ScrollView {
        anchors.fill: parent
        RowLayout {
            width: parent.width
            spacing: 10

            ColumnLayout {
                width: parent.width * 0.5
                spacing: 10

                // Genetic Algorithm Parameters
                GroupBox {
                    title: "GA Parameters"
                    Layout.fillWidth: true

                    ColumnLayout {
                        width: parent.width
                        spacing: 10
                        TextField{
                            text: methodSelector.currentText
                        }
                        ComboBox {
                            id: methodSelector

                            model: gaModel.availableMethods
                            onCurrentIndexChanged: {
                                gaModel.setMethod(methodSelector.currentIndex)
                            }
                        }


                        Repeater {
                            model: Object.keys(gaModel.parameterNames)

                            delegate: RowLayout {
                                Label {
                                    text: gaModel.parameterNames[modelData]
                                }
                                TextField {
                                    text: gaModel.parameters[modelData]
                                    onTextChanged: {
                                        gaModel.updateParameter(modelData, text)
                                    }
                                }
                            }
                        }
                    }

                }
            }

            ColumnLayout {
                width: parent.width * 0.5
                spacing: 10

                // Vegetation Zone Parameters
                GroupBox {
                    title: "Vegetation zone parameters"
                    Layout.fillWidth: true

                    GridLayout {
                        columns: 3
                        width: parent.width
                        columnSpacing: 10
                        rowSpacing: 5

                        Label { text: "Parameter" }
                        Label { text: "Lower Limit" }
                        Label { text: "Upper Limit" }

                        Repeater {
                            model: ListModel {
                                ListElement { param: "TT"; lower: "-2"; upper: "0.5" }
                                ListElement { param: "CFMAX"; lower: "0.5"; upper: "4" }
                                ListElement { param: "SP"; lower: "0.1"; upper: "0.9" }
                                ListElement { param: "SFCF"; lower: "0.05"; upper: "0.05" }
                                ListElement { param: "CFR"; lower: "0.1"; upper: "1" }
                                ListElement { param: "CWH"; lower: "0.1"; upper: "0.1" }
                                ListElement { param: "FC"; lower: "100"; upper: "550" }
                                ListElement { param: "LP"; lower: "0.3"; upper: "1" }
                                ListElement { param: "BETA"; lower: "1"; upper: "5" }
                            }

                            delegate: RowLayout {
                                Label { text: model.param; Layout.preferredWidth: 80 }
                                TextField { text: model.lower; Layout.preferredWidth: 60 }
                                TextField { text: model.upper; Layout.preferredWidth: 60 }
                            }
                        }
                    }
                }

                // Catchment Parameters
                GroupBox {
                    title: "Catchment parameters"
                    Layout.fillWidth: true

                    GridLayout {
                        columns: 3
                        width: parent.width
                        columnSpacing: 10
                        rowSpacing: 5

                        Label { text: "Parameter" }
                        Label { text: "Lower Limit" }
                        Label { text: "Upper Limit" }

                        Repeater {
                            model: ListModel {
                                ListElement { param: "PERC"; lower: "0"; upper: "4" }
                                ListElement { param: "UZL"; lower: "0"; upper: "1" }
                                ListElement { param: "K0"; lower: "0.01"; upper: "0.2" }
                                ListElement { param: "K1"; lower: "0.01"; upper: "0.2" }
                                ListElement { param: "K2"; lower: "0.005"; upper: "0.1" }
                                ListElement { param: "MAXBAS"; lower: "1"; upper: "2.5" }
                                ListElement { param: "PCALT"; lower: "10"; upper: "10" }
                                ListElement { param: "TCALT"; lower: "0.6"; upper: "0.6" }
                                ListElement { param: "Elev. of P"; lower: "0"; upper: "0" }
                                ListElement { param: "Elev. of T"; lower: "0"; upper: "0" }
                            }

                            delegate: RowLayout {
                                Label { text: model.param; Layout.preferredWidth: 80 }
                                TextField { text: model.lower; Layout.preferredWidth: 60 }
                                TextField { text: model.upper; Layout.preferredWidth: 60 }
                            }
                        }
                    }
                }
            }
        }
    }
}
