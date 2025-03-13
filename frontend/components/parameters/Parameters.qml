import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ScrollView {
    id: scrollView
    contentWidth: -1

    Component.onCompleted: {
        parameterModel.setFactory(factoryName)
    }


    property var parameterModel
    property string factoryName


    ColumnLayout {
        spacing: 10
        anchors.fill: parent
        anchors.margins: 10

        // Sélecteur de méthode
        ComboBox {
            leftPadding: 10
            Layout.fillWidth: true // Prendre toute la largeur disponible
            Layout.preferredHeight: 40 // Ajuster la hauteur si nécessaire
            id: methodSelector
            model: parameterModel.availableMethods
            onCurrentIndexChanged: {
                parameterModel.setMethod(methodSelector.currentIndex)
            }
        }

        // Section pour les paramètres associés à la méthode sélectionnée
        GridLayout {
            id: parameterGrid
            width: parent.width
            columns: 2 // Deux colonnes : une pour les labels, une pour les TextField
            columnSpacing: 20 // Espacement entre les colonnes
            rowSpacing: 5 // Espacement entre les lignes

            // Répétiteur pour afficher les labels des paramètres
            Repeater {
                model: Object.keys(parameterModel.parameterNames)

                delegate: RowLayout {
                    Layout.column: 0 // Première colonne pour les labels
                    Layout.row: index // Ligne correspondante à l'index du paramètre
                    Layout.preferredWidth: parent.width * 0.5
                    // Label pour chaque paramètre
                    Label {
                        text: parameterModel.parameterNames[modelData]
                    }
                }
            }

            // Répétiteur pour afficher les TextField dynamiquement
            Repeater {
                model: Object.keys(parameterModel.parameterNames)

                delegate: RowLayout {
                    Layout.column: 1 // Deuxième colonne pour les TextField
                    Layout.row: index // Ligne correspondante à l'index du paramètre
                    Layout.preferredWidth: parent.width * 0.5


                    // Zone de texte pour la saisie des valeurs
                    TextField {
                        text: parameterModel.parameters[modelData]
                        onTextChanged: parameterModel.updateParameter(modelData, text)
                        Layout.preferredWidth: 100 // Largeur fixe pour les TextField
                        Layout.alignment: Qt.AlignRight
                        validator: DoubleValidator {
                            bottom: 0
                            notation: DoubleValidator.StandardNotation
                        }

                        // Gestion de l'erreur de validation (bordure rouge en cas d'erreur)
                        background: Rectangle {
                            color: "white"
                            border.color: parameterModel.parameterErrors[modelData] !== "" ? "red" : "gray"
                            border.width: 1
                        }
                    }

                    // Affichage de l'erreur pour chaque paramètre si présent
                    /*Text {
                        color: "red"
                        text: parameterModel.parameterErrors[modelData]
                    }*/
                }
            }
        }

    }


}
