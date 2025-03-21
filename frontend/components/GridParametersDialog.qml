import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./parameters"
import io.qml

Dialog {
    title: "OPTIMIZATION"
    modal: true
    width: 1300
    height: 700
    standardButtons: Dialog.Ok | Dialog.Cancel
    padding: 5

    /*ScrollView {
        id: productionColumn
        contentWidth: -1 // Désactiver la gestion automatique de la largeur
        height: parent.height * 0.8
        width: parent.width *0.25
        */

        /*ColumnLayout {
            id: contentColumn
            spacing: 10
            Layout.preferredWidth: parent.width *0.25
            Layout.preferredHeight:  parent.height
            Repeater {
                model: ["Holtan", "SCS"] // Liste des méthodes à afficher

                delegate: GridParameters {
                    width: parent.width // Prendre toute la largeur disponible
                    height: childrenRect.height // Hauteur implicite basée sur le contenu
                    parameterModel: GridParametersQML{} // Passer le modèle
                    factoryName: "Production" // Nom de la factory
                    methodName: modelData // Nom de la méthode
                    border.width: 1
                }
            }
        }*/
    //}
    ColumnLayout{
        spacing: 10
        Layout.preferredWidth: parent.width *0.25
        Layout.preferredHeight:  parent.height
        GridParameters {
            width: parent.width // Prendre toute la largeur disponible
            height: childrenRect.height // Hauteur implicite basée sur le contenu
            parameterModel: GridParametersQML{} // Passer le modèle
            factoryName: "Production" // Nom de la factory
            methodName: "Horton" // Nom de la méthode
            border.width: 1
        }
        GridParameters {
            width: parent.width // Prendre toute la largeur disponible
            height: childrenRect.height // Hauteur implicite basée sur le contenu
            parameterModel: GridParametersQML{} // Passer le modèle
            factoryName: "Production" // Nom de la factory
            methodName: "SCS" // Nom de la méthode
            border.width: 1
        }
    }

}
