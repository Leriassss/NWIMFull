import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ScrollView {
    background: Rectangle {
        color: "white"
        border.width: 1
    }

    ColumnLayout {
        id: cl
        spacing: 10
        anchors.fill: parent
        anchors.margins: 10 // Marges autour de la colonne

        // Sélecteur de méthode de routage
        ComboBox {
            Layout.fillWidth: true // Prendre toute la largeur disponible
            Layout.preferredHeight: 40 // Ajuster la hauteur si nécessaire
            id: methodSelector
            model: routingModel.availableMethods
            onCurrentIndexChanged: {
                routingModel.setMethod(methodSelector.currentIndex)
            }
        }

        // Section pour les paramètres associés à la méthode sélectionnée
        GridLayout {
            id: parameterGrid
            width: parent.width
            columns: 2 // Deux colonnes : une pour les labels, une pour les TextField
            columnSpacing: 10 // Espacement entre les colonnes
            rowSpacing: 10 // Espacement entre les lignes

            // Répétiteur pour afficher les labels des paramètres
            Repeater {
                model: Object.keys(routingModel.parameterNames)

                delegate: RowLayout {
                    Layout.column: 0 // Première colonne pour les labels
                    Layout.row: index // Ligne correspondante à l'index du paramètre

                    // Label pour chaque paramètre
                    Label {
                        text: routingModel.parameterNames[modelData]
                    }
                }
            }

            // Répétiteur pour afficher les TextField dynamiquement
            Repeater {
                model: Object.keys(routingModel.parameterNames)

                delegate: RowLayout {
                    Layout.column: 1 // Deuxième colonne pour les TextField
                    Layout.row: index // Ligne correspondante à l'index du paramètre

                    // Zone de texte pour la saisie des valeurs
                    TextField {
                        text: routingModel.parameters[modelData]
                        onTextChanged: routingModel.updateParameter(modelData, text)
                        Layout.preferredWidth: 150 // Largeur fixe pour les TextField
                        validator: DoubleValidator {
                            bottom: 0
                            notation: DoubleValidator.StandardNotation
                        }

                        // Gestion de l'erreur de validation (bordure rouge en cas d'erreur)
                        background: Rectangle {
                            color: "white"
                            border.color: routingModel.parameterErrors[modelData] !== "" ? "red" : "gray"
                            border.width: 1
                        }
                    }

                    // Affichage de l'erreur pour chaque paramètre si présent
                    Text {
                        color: "red"
                        text: routingModel.parameterErrors[modelData]
                    }
                }
            }
        }
    }
}
