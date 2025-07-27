import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import ".."

Rectangle {
    property var parameterModel
    property string factoryName
    property string methodName
    property bool activated: enableParams.checked
    property var parameters: parameterModel.parameters


    Component.onCompleted: {
        parameterModel.setFactory(factoryName)
        parameterModel.setMethod(methodName)
    }

    Column {
        anchors.fill: parent

        Row{
            spacing: 5
            //Layout.preferredWidth: parent.width
            //Layout.preferredHeight: 50
            width: parent.width
            height : 30
            id : rowLabel
            CustomCheckDelegate{
                id : enableParams
                checked: true
                font.pointSize: 10
                anchors.verticalCenter:  parent.verticalCenter
                topPadding: 5

            }
            // Sélecteur de méthode
            Label {
                id: methodSelector
                bottomPadding:  5
                width: 100
                text: methodName
                anchors.verticalCenter:  parent.verticalCenter

                font.bold: true
            }
        }



        // Section pour les paramètres associés à la méthode sélectionnée
        GridLayout {
            enabled: enableParams.checked
            opacity: enabled ? 1 : 0.7
            id: parameterGrid
            //Layout.preferredWidth:  parent.width *0.9
            //Layout.alignment: Qt.AlignCenter
            //Layout.preferredHeight: parent.height - rowLabel.height - rowSpacing
            width: parent.width * 0.9
            anchors.horizontalCenter: parent.horizontalCenter
            height : parent.height - rowLabel.height - 10
            columns: 3
            columnSpacing: 10
            rowSpacing: 5

            // Répétiteur pour afficher les paramètres sous forme de plage (min, max)
            Repeater {
                model: parameterModel.parameterNames  // Correction ici

                delegate: Text {
                    Layout.column: 0
                    Layout.row: index
                    Layout.preferredWidth: 100
                    text: modelData
                    leftPadding: 10

                }
            }

            // Répétiteur pour les champs min
            Repeater {
                model: {console.log("parameterModel.parameterNames : ",parameterModel.parameterNames)

                    parameterModel.parameterNames}


                delegate: TextField {
                    Layout.column: {
                        console.log("modelData : ",modelData)
                        console.log("parameterModel.parameters[modelData] : ", parameters[modelData])
                        1
                    }
                    Layout.row: index
                    Layout.preferredWidth: 50
                    Layout.alignment: Qt.AlignRight
                    text: parameters[modelData][0]
                    onTextChanged: {
                        parameterModel.updateParameter(modelData, text, parameters[modelData][1])
                    }
                    validator: DoubleValidator {
                        notation: DoubleValidator.StandardNotation
                    }
                    background: Rectangle {
                            // Fond transparent
                            color: "transparent"

                            // Bordure inférieure seule
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 1
                                color: "#ffffff"
                                border.color: {
                                    if(parameterModel.parameterErrors){
                                        let errors = parameterModel.parameterErrors[modelData];
                                        if (errors && errors.min) {
                                            return "red"; // Erreur sur min
                                        } else if (errors && errors.max && parameterModel.parameters[modelData][0] >= parameterModel.parameters[modelData][1]) {
                                            return "red"; // min >= max
                                        } else {
                                            return "gray";
                                        }
                                    }
                                }
                                border.width: 1
                            }


                        }

                }
            }

            // Répétiteur pour les champs max
            Repeater {
                model: parameterModel.parameterNames

                delegate: TextField {
                    Layout.column: 2
                    Layout.row: index
                    Layout.preferredWidth: 50
                    Layout.alignment: Qt.AlignRight
                    text: parameters[modelData][1]
                    onTextChanged: parameterModel.updateParameter(modelData, parameters[modelData][0], text)
                    validator: DoubleValidator {
                        notation: DoubleValidator.StandardNotation
                    }
                    background: Rectangle {
                            // Fond transparent
                            color: "transparent"

                            // Bordure inférieure seule
                            Rectangle {
                                anchors.bottom: parent.bottom
                                width: parent.width
                                height: 1
                                color: "#ffffff"
                                border.color: {
                                    let errors = parameterModel.parameterErrors[modelData];
                                    if (errors && errors.max) {
                                        return "red"; // Erreur sur max
                                    } else if (errors && errors.min && parameters[modelData][0] >= parameters[modelData][1]) {
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
}
