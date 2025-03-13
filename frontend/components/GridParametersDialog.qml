import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./parameters"
import "../../io/qml"
import io.qml

Dialog {
    title: "OPTIMIZATION"
    modal: true
    width: 1000
    height: 700
    standardButtons: Dialog.Ok | Dialog.Cancel
    padding: 5


    Rectangle {
        anchors.fill: parent
        border.width: 1
        Row{
            anchors.fill: parent
            spacing : 5
            Column{
                id : productionColumn
                height: parent.height
                width: parent.width * 0.25
                padding: 10
                spacing : 10

                Row{
                    padding: 30
                    anchors.bottom: parent.bottom
                    height: parent.height *0.9
                    width: parent.width
                    spacing : 5
                    GridParameters{
                        parameterModel : GridParametersQML{}
                        factoryName : "Production"
                        methodName : "SCS"
                    }
                }

            }

        }



    }
}
