import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15

import "./parameters"
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

        ParametersModel{
            height: parent.height
            width: parent.width * 0.4
            parameterModel : optimizationModel
        }
        Column{
            width: parent.width*0.6
            height: parent.height
            anchors.right: parent.right
            RangeParameters{
                parameterModel : productionrangeModel
                factoryName : "Production"
                height: parent.height *0.2
                width: parent.width
            }
            RangeParameters{
                anchors.right: parent.right
                parameterModel : initialLossrangeModel
                factoryName : "Routing"
                height: parent.height *0.2
                width: parent.width
            }
        }



    }
}
