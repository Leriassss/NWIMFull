import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Rectangle {
    property var parameterModel
    property string factoryName
    property string methodName


    Component.onCompleted: {
        parameterModel.setFactory(factoryName)
        parameterModel.setMethod(methodName)
    }

    ColumnLayout {
        spacing: 10
        anchors.fill: parent

        // Sélecteur de méthode
        Label {
            id: methodSelector
            leftPadding: 10
            width: 75
            text: methodName
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

                delegate: TextField {
                    Layout.column: 1
                    Layout.row: index
                    Layout.preferredWidth: 100
                    Layout.alignment: Qt.AlignRight
                    text: parameterModel.parameters[modelData][0]
                    onTextChanged: parameterModel.updateParameter(modelData, text, parameterModel.parameters[modelData][1])
                    validator: DoubleValidator {
                        notation: DoubleValidator.StandardNotation
                    }
                    background: Rectangle {
                        color: "white"
                        border.color: {
                            let errors = parameterModel.parameterErrors[modelData];
                            if (errors && errors.min) {
                                return "red"; // Erreur sur min
                            } else if (errors && errors.max && parameterModel.parameters[modelData][0] >= parameterModel.parameters[modelData][1]) {
                                return "red"; // min >= max
                            } else {
                                return "gray"; // Valeur correcte
                            }
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
                    text: parameterModel.parameters[modelData][1]
                    onTextChanged: parameterModel.updateParameter(modelData, parameterModel.parameters[modelData][0], text)
                    validator: DoubleValidator {
                        notation: DoubleValidator.StandardNotation
                    }
                    background: Rectangle {
                        color: "white"
                        border.color: {
                            let errors = parameterModel.parameterErrors[modelData];
                            if (errors && errors.max) {
                                return "red"; // Erreur sur max
                            } else if (errors && errors.min && parameterModel.parameters[modelData][0] >= parameterModel.parameters[modelData][1]) {
                                return "red"; // min >= max
                            } else {
                                return "gray"; // Valeur correcte
                            }
                        }
                        border.width: 1
                    }
                }
            }

        }
    }
}
