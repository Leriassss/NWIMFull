import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import Qt5Compat.GraphicalEffects
import ".."
Column {
    id : control
    Component.onCompleted: {
        parameterModel.setFactory(factoryName)
        console.log(" --------- CC -----------")
        console.log(JSON.stringify(parameters))
    }


    property var parameterModel
    property string factoryName

    // Get the parameters and the values typed by user
    property var parameters: parameterModel?.parameters
    property bool checkPassed: parameterModel?.desactivated

    // Sélecteur de méthode
    CustomComboBox {
        leftPadding: 10
        anchors.horizontalCenter: parent.horizontalCenter
        width: parent.width
        height: 30
        id: methodSelector
        model: parameterModel?.availableMethods
        onCurrentIndexChanged: {
            console.log("-------------CC----------------")
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
            model: parameterModel.parameterNames

            delegate: RowLayout {
                Layout.column: 0 // Première colonne pour les labels
                Layout.row: index // Ligne correspondante à l'index du paramètre
                Layout.preferredWidth: parent.width * 0.5
                // Label pour chaque paramètre
                Label {
                    text: modelData
                }
            }
        }

        // Répétiteur pour afficher les TextField dynamiquement
        Repeater {
            model: {
                console.log("*-*-* RES1 *-*-")
                console.log(parameterModel.parameterValues)
                parameterModel.parameterValues
            }

            delegate: RowLayout {
                Layout.column: 1 // Deuxième colonne pour les TextField
                Layout.row: index // Ligne correspondante à l'index du paramètre
                Layout.preferredWidth: parent.width * 0.5


                // Zone de texte pour la saisie des valeurs
                TextField {
                    id : param_value
                    property string modelName: parameterModel.parameterNames[index]
                    property var errors: parameterModel.parameterErrors[modelName]
                    ToolTip.delay: 500
                    ToolTip.timeout: 5000
                    ToolTip.visible: hovered &&  errors !== "" ? true : false
                    ToolTip.text: qsTr(parameterModel.parameterErrors[modelName])
                    text: modelData
                    onTextChanged: {
                        parameterModel.updateParameter(modelName, text)
                        console.log("----------------- RESULTATS -----------------------")
                        console.log(JSON.stringify(parameterModel.parameters))
                        focus = true
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
                            console.log("----------------- RESULTATS1 -----------------------")
                            console.log(JSON.stringify(parameterModel.parameterErrors))
                            param_value.errors !== "" ? "red" : "gray"
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
