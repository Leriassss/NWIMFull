import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

ScrollView {
    id: scrollView
    contentWidth: -1
    //contentHeight: cl.implicitHeight

    background: Rectangle {
        color: "white"
        border.width: 1
    }

    ColumnLayout {
        id: cl
        spacing: 10
        anchors.fill: parent
        anchors.margins: 10

        // Sélecteur de méthode
        ComboBox {
            leftPadding: 10
            Layout.fillWidth: true
            Layout.preferredHeight: 40
            id: methodSelector
            model: productionModel.availableMethods
            onCurrentIndexChanged: {
                productionModel.setMethod(methodSelector.currentIndex)
            }
        }


        GridLayout {
            id: parameterGrid
            width: parent.width
            columns: 2
            columnSpacing: 10
            rowSpacing: 10


            Repeater {
                model: Object.keys(productionModel.parameterNames)

                delegate: RowLayout {
                    Layout.column: 0 // Première colonne pour les labels
                    Layout.row: index // Ligne correspondante à l'index du paramètre
                    Layout.alignment: Qt.AlignRight // Aligner les labels à droite

                    // Label pour chaque paramètre
                    Label {
                        text: productionModel.parameterNames[modelData]
                    }
                }
            }

            // Répétiteur pour afficher les TextField dynamiquement
            Repeater {
                model: Object.keys(productionModel.parameterNames)

                delegate: RowLayout {
                    Layout.column: 1 // Deuxième colonne pour les TextField
                    Layout.row: index // Ligne correspondante à l'index du paramètre

                    // Zone de texte pour la saisie des valeurs
                    TextField {
                        text: productionModel.parameters[modelData]
                        onTextChanged: productionModel.updateParameter(modelData, text)
                        Layout.preferredWidth: 150 // Largeur fixe pour les TextField
                        validator: DoubleValidator {
                            bottom: 0
                            notation: DoubleValidator.StandardNotation
                        }

                        // Gestion de l'erreur de validation (bordure rouge en cas d'erreur)
                        background: Rectangle {
                            color: "white"
                            border.color: productionModel.parameterErrors[modelData] !== "" ? "red" : "gray"
                            border.width: 1
                        }
                    }

                    // Affichage de l'erreur pour chaque paramètre si présent
                    Text {
                        color: "red"
                        text: productionModel.parameterErrors[modelData]
                        Layout.alignment: Qt.AlignLeft // Aligner les messages d'erreur à gauche
                    }
                }
            }
        }
    }
}
