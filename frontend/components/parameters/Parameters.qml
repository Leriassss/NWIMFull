import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

Column {

    Component.onCompleted: {
        parameterModel.setFactory(factoryName)
    }


    property var parameterModel
    property string factoryName

    // Get the parameters and the values typed by user
    property var parameters: parameterModel?.parameters

    // Sélecteur de méthode
    ComboBox {
        leftPadding: 10
        width: parent.width
        height: 40
        id: methodSelector
        background: Rectangle{
            anchors.fill: parent
            color: "#ebebeb"
            border.width: 1
            border.color: "grey"
        }

        indicator: Canvas {
               id: canvas
               x: methodSelector.width - width - methodSelector.rightPadding
               y: methodSelector.topPadding + (methodSelector.availableHeight - height) / 2
               width: 12
               height: 8
               contextType: "2d"

               Connections {
                   target: methodSelector
                   function onPressedChanged() { canvas.requestPaint(); }
               }

               onPaint: {
                   context.reset();
                   context.moveTo(0, 0);
                   context.lineTo(width, 0);
                   context.lineTo(width / 2, height);
                   context.closePath();
                   context.fillStyle = methodSelector.pressed ? "#17a81a" : "#21be2b";
                   context.fill();
               }
           }

        model: parameterModel?.availableMethods
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
                    text: parameterModel?.parameterNames[modelData]
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
                    id : param_value
                    property string modelName: parameterModel?.parameterNames[modelData]
                    text: parameterModel?.parameters[modelData]
                    onTextChanged: {
                        parameterModel.updateParameter(modelName, text)
                        console.log("----------------- RESULTATS -----------------------")
                        console.log(JSON.stringify(parameterModel.parameters))
                    }
                    Layout.preferredWidth: 100 // Largeur fixe pour les TextField
                    Layout.alignment: Qt.AlignRight
                    validator: DoubleValidator {
                        bottom: 0
                        notation: DoubleValidator.StandardNotation
                    }

                    // Gestion de l'erreur de validation (bordure rouge en cas d'erreur)
                    background: Rectangle {
                        color: "#ebebeb"
                        border.color: {
                            parameterModel.parameterErrors[param_value.modelName] !== "" ? "red" : "gray"
                        }
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
