import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import ".."

Column {
    id: scrollView
    clip: true


    property var parameterModel
    property string factoryName

    Component.onCompleted: {
        parameterModel.setFactory(factoryName)  // Charger la factory au démarrage
    }
    anchors.margins: 10

    ComboBox {
        leftPadding: 10
        width: parent.width * 0.8
        anchors.horizontalCenter: parent.horizontalCenter
        height: 25
        id: methodSelector
        model: parameterModel?.availableMethods
        onCurrentIndexChanged: {
            parameterModel.setMethod(methodSelector.currentIndex)
        }
    }


    // Section pour les paramètres associés à la méthode sélectionnée
    GridLayout {
        id: parameterGrid
        width: parent.width
        columns: 3 // Trois colonnes : label, min et max
        columnSpacing: 10
        rowSpacing: 5

        // Répétiteur pour afficher les paramètres sous forme de plage (min, max)
        Repeater {
            model: Object.keys(parameterModel.parameters)  // Correction ici

            delegate: RowLayout {
                Layout.column: 0
                Layout.row: index
                Layout.preferredWidth: 75

                // Label pour chaque paramètre
                Label {
                    text: modelData
                }
            }
        }

        // Répétiteur pour les champs min
        Repeater {
            model: Object.keys(parameterModel.parameters)

            delegate:CustomTextField {
                Layout.column: 1
                Layout.row: index
                Layout.preferredWidth: 100
                Layout.alignment: Qt.AlignRight
                text: parameterModel.parameters[modelData][0] !== null ? parameterModel.parameters[modelData][0] : ""

                onTextChanged: parameterModel.updateParameter(modelData, text, parameterModel.parameters[modelData][1] !== null ? parameterModel.parameters[modelData][1] : "")

                validator: DoubleValidator {
                    notation: DoubleValidator.StandardNotation
                }

                background : Rectangle {
                    // Fond transparent
                    color: "transparent"

                    // Bordure inférieure seule
                    Rectangle {
                        anchors.bottom: parent.bottom
                        width: parent.width
                        height: 1
                        color:  "#bdbebf"
                        border.color: {
                            let errors = parameterModel.parameterErrors[modelData];
                            return (errors && errors.min) ? "red" : "gray";
                        }
                        border.width: 1
                    }


                 }
            }
        }

        // Répétiteur pour les champs max
        Repeater {
            model: Object.keys(parameterModel.parameters)

            delegate: CustomTextField {
                Layout.column: 2
                Layout.row: index
                Layout.preferredWidth: 100
                Layout.alignment: Qt.AlignRight
                text: parameterModel.parameters[modelData][1] !== null ? parameterModel.parameters[modelData][1] : ""

                onTextChanged: parameterModel.updateParameter(modelData, parameterModel.parameters[modelData][0] !== null ? parameterModel.parameters[modelData][0] : "", text)

                validator: DoubleValidator {
                    notation: DoubleValidator.StandardNotation
                }
                background : Rectangle {
                    // Fond transparent
                    color: "transparent"

                    // Bordure inférieure seule
                    Rectangle {
                        anchors.bottom: parent.bottom
                        width: parent.width
                        height: 1
                        color:  "#bdbebf"
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

