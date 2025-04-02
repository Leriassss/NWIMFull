import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ScrollView {
    id: scrollView
    contentWidth: -1
    clip: true


    property var parameterModel
    property string factoryName

    Component.onCompleted: {
        parameterModel.setFactory(factoryName)  // Charger la factory au démarrage
    }

    ColumnLayout {
        spacing: 10
        anchors.fill: parent
        anchors.margins: 10

        // Sélecteur de méthode
        ComboBox {
            id: methodSelector
            leftPadding: 10
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            model: parameterModel.availableMethods

            onCurrentIndexChanged: {
                parameterModel.setMethod(methodSelector.currentIndex)
            }
        }

        // Section pour les paramètres associés à la méthode sélectionnée
        GridLayout {
            id: parameterGrid
            width: parent.width
            columns: 3 // Trois colonnes : label, min et max
            columnSpacing: 20
            rowSpacing: 5

            // Répétiteur pour afficher les paramètres sous forme de plage (min, max)
            Repeater {
                model: Object.keys(parameterModel.parameters)  // Correction ici

                delegate: RowLayout {
                    Layout.column: 0
                    Layout.row: index
                    Layout.preferredWidth: parent.width * 0.3

                    // Label pour chaque paramètre
                    Label {
                        text: modelData
                    }
                }
            }

            // Répétiteur pour les champs min
            Repeater {
                model: Object.keys(parameterModel.parameters)

                delegate:TextField {
                    Layout.column: 1
                    Layout.row: index
                    Layout.preferredWidth: 100
                    Layout.alignment: Qt.AlignRight
                    text: parameterModel.parameters[modelData][0] !== null ? parameterModel.parameters[modelData][0] : ""

                    onTextChanged: parameterModel.updateParameter(modelData, text, parameterModel.parameters[modelData][1] !== null ? parameterModel.parameters[modelData][1] : "")

                    validator: DoubleValidator {
                        notation: DoubleValidator.StandardNotation
                    }

                    background: Rectangle {
                        color: "white"
                        border.color: {
                            let errors = parameterModel.parameterErrors[modelData];
                            return (errors && errors.min) ? "red" : "gray";
                        }
                        border.width: 1
                    }
                }
            }

            // Répétiteur pour les champs max
            Repeater {
                model: Object.keys(parameterModel.parameters)

                delegate: TextField {
                    Layout.column: 2
                    Layout.row: index
                    Layout.preferredWidth: 100
                    Layout.alignment: Qt.AlignRight
                    text: parameterModel.parameters[modelData][1] !== null ? parameterModel.parameters[modelData][1] : ""

                    onTextChanged: parameterModel.updateParameter(modelData, parameterModel.parameters[modelData][0] !== null ? parameterModel.parameters[modelData][0] : "", text)

                    validator: DoubleValidator {
                        notation: DoubleValidator.StandardNotation
                    }

                    background: Rectangle {
                        color: "white"
                        border.color: {
                            let errors = parameterModel.parameterErrors[modelData];
                            return (errors && errors.max) ? "red" : "gray";
                        }
                        border.width: 1
                    }
                }

            }

        }
    }
}
