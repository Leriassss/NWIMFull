import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import "./parameters"
import "../../io/qml"
import io.qml
import Qt5Compat.GraphicalEffects
import Qt.labs.qmlmodels
Dialog {
    title: "ETP Computation"
    implicitWidth:  1000
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    id: dialogOptim

    standardButtons: Dialog.Cancel
    closePolicy : Popup.CloseOnEscape
    //padding: 5
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    header: ToolBar {
            id: toolBar
            height: 30
            //implicitHeight: 35
            implicitWidth:  200

            clip: true
            Rectangle{
                //gradient: Gradient.AboveTheSky
                color:"#ebebeb"
                //border.color: "#6b6b6b"
                //border.width: 1

                anchors.fill: parent
                Row{
                    anchors.fill: parent
                    spacing: 1
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("📥")
                        ToolTip.text: qsTr("Load Parameters")
                        onClicked: {
                            loadETPparams.open()
                        }
                    }
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("⚙️")
                        ToolTip.text: qsTr("Compute")
                        onClicked: {
                             // En-têtes du fichier chargé
                            let columnMapping = {
                                    "dates" : datesComboBox.currentText,
                                    "tmean":tMeanComboBox.currentText,
                                    "tmin" : tMinComboBox.currentText,
                                    "tmax" : tMaxComboBox.currentText,
                                    "rh" : rhComboBox.currentText,
                                    "rn" : rsComboBox.currentText,
                                    "wind" : u2ComboBox.currentText,
                                    "lat" : lat.text,
                                    "elevation" : elevation.text
                                }
                                etoManager.setDictValues(columnMapping)

                                if(etoManager.errors.length !==0){

                                    dataErrorsDialog.open()
                                }
                                else{
                                    try {
                                        etoManager.computeETo()

                                    } catch (error) {
                                        errorDialog.text = "Les paramètres requis n'ont pas étét fournis "
                                        errorDialog.open()
                                    }
                                    populateTable(etoManager.etpComputed)

                                }

                        }
                    }
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("💾")
                        ToolTip.text: qsTr("Save Data")
                    }
                }
            }


       }

    Dialog {
        id: dataErrorsDialog
        title: "❌ ERREURS DETECTEES !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)

        property var errors: etoManager.errors

        Rectangle{
            anchors.fill: parent
            border.width: 1
            ListView {
                id: errorListView
                model: dataErrorsDialog.errors
                anchors.fill: parent
                delegate: Item {
                    width: errorListView.width
                    height: 20
                    Rectangle {
                        width: parent.width
                        height: parent.height
                        //color: "lightgray"
                        border.color: "gray"
                        Text {
                            anchors.left: parent.left
                            anchors.verticalCenter: parent.verticalCenter
                            padding: 5
                            text: modelData
                            wrapMode: Text.WordWrap
                        }
                    }
                }
            }

            }
    }

    FileChoose {
        id: loadETPparams
        nameFilters: ["Excel (*.xlsx)","Texte (*.txt)"]
        property string fileName: ""

        onAccepted: {
            fileName = cleanFilePath(loadETPparams.file.toString());
            if (fileName) {
                try {
                    etoManager.readFile(fileName)
                    var headers = etoManager.headers
                    columnMappingDialog.headers = headers
                } catch (error) {
                    errorDialog.text = "Erreur lors du chargement du fichier : " + error
                    errorDialog.open()
                }
            }
        }
        onRejected: {
            console.log("Sélection annulée");
        }

    }

    Dialog {
        id: errorDialog
        title: "Errors"
        standardButtons: Dialog.Ok
        property string text: ""
        Label {
            text: errorDialog.text
        }
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        modal: true
        background: Rectangle{
            anchors.fill:parent
            border.color: "red"
            color: "#f0f0f0"
            border.width: 1
        }
    }



    SplitView {
        id: splitView
        anchors.fill: parent

        handle: Rectangle {
            implicitWidth: 4
            implicitHeight: 4
            color: SplitHandle.pressed ? "#81e889"
                : (SplitHandle.hovered ? Qt.lighter("#c2f4c6", 1.1) : "#c2f4c6")
            border.width: 1
            border.color: "grey"
        }

        Rectangle{
            id : columnMappingDialog
            color: "#ebebeb"
            border.width: 1
            border.color: "grey"
            SplitView.minimumWidth:  parent.width*0.5
            SplitView.preferredWidth: parent.width*0.5

            property var headers: etoManager.headers
            //width: parent.width*0.4
            //height: parent.height
            Column{
                width: parent.width - 5
                height: parent.height - 5
                anchors.centerIn: parent
                spacing: 2
                clip: true
                Label {
                    id : methodsLabel
                    anchors.margins: 5
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "DATA MAPPING"
                    horizontalAlignment: Qt.AlignHCenter
                    font.bold: true
                    font.pointSize: 10
                    padding: 5
                    color: "black"
                    width: parent.width
                    background: Rectangle {
                        border.width: 1
                        border.color: "#17a81a"
                        radius : 2
                        color : "transparent"
                        layer.enabled: true
                        layer.effect: MultiEffect {
                            shadowEnabled: true
                            shadowHorizontalOffset: 2
                            shadowVerticalOffset: 2
                            shadowColor: methodsLabel.visualFocus ? "#330066ff" : "#aaaaaa"
                        }
                    }
                }

                RowLayout{
                    width: parent.width *0.9
                    height: parent.height *0.9
                    spacing: 10


                    GridLayout {
                        Layout.preferredHeight:  parent.height
                        Layout.preferredWidth:  parent.width * 0.5
                        columns: 2
                        columnSpacing: 10
                        rowSpacing: 10

                        Label {
                            text: "Dates"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: datesComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }

                        Label {
                            text: "Teméprature Moy. [°C]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: tMeanComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }

                        // Ligne pour Dates
                        Label {
                            text: "Température Min. [°C]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: tMinComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }
                        // Ligne pour Dates
                        Label {
                            text: "Température Max. [°C]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: tMaxComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }
                        Label {
                            text: "Humidité relative de l'air [%]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: rhComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }

                        Label {
                            text: "Rad. Solaire/ \nRad. Net/\nNb Heures d'Enso."
                            Layout.alignment: Qt.AlignLeft
                            Layout.preferredWidth: 100
                            wrapMode: Text.Wrap
                        }
                        ComboBox {
                            id: rsComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }

                        Label {
                            text: "Vitesse moy. [m/s]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: u2ComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.fillWidth: true
                        }

                        // Ligne pour ETP
                        Label {
                            text: "Latitude [rad]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        TextField {
                            id: lat
                            text : "5"
                            Layout.fillWidth: true
                            validator: DoubleValidator {
                                bottom: 0
                                notation: DoubleValidator.StandardNotation
                            }
                        }
                        Label {
                            text: "Altitude [m]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        TextField {
                            id: elevation
                            Layout.fillWidth: true
                            text : "150"
                            validator: DoubleValidator {
                                bottom: 0
                                notation: DoubleValidator.StandardNotation
                            }
                        }
                    }



                }


            }


        }

        Rectangle{
            border.width: 1
            border.color: "grey"
            width: parent.width*0.6
            height: parent.height
            color: "#ebebeb"
            Column{
                width: parent.width - 5
                height: parent.height - 5
                anchors.centerIn: parent
                spacing: 2
                clip: true
                Label {
                    id : dataLabel
                    anchors.margins: 5
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: "CALCULATION"
                    horizontalAlignment: Qt.AlignHCenter
                    font.bold: true
                    font.pointSize: 10
                    padding: 5
                    color: "black"
                    width: parent.width
                    background: Rectangle {
                        border.width: 1
                        border.color: "#17a81a"
                        radius : 2
                        color : "transparent"
                        layer.enabled: true
                        layer.effect: MultiEffect {
                            shadowEnabled: true
                            shadowHorizontalOffset: 2
                            shadowVerticalOffset: 2
                            shadowColor: dataLabel.visualFocus ? "#330066ff" : "#aaaaaa"
                        }
                    }
                }
                ColumnLayout{
                    height:   100
                    width:  parent.width *0.7

                    ComboBox {
                        leftPadding: 10
                        Layout.preferredWidth:  150
                        Layout.preferredHeight: 40
                        id: methodSelector
                        model: etoManager.availableMethods
                        onCurrentTextChanged: {
                            etoManager.setMethod(methodSelector.currentText)
                        }
                        Component.onCompleted: {
                            etoManager.setMethod(methodSelector.currentText)
                        }
                    }
                    Label{
                        id : requiredParams
                        text : "PARAMETRES REQUIS : " + etoManager.methodParameters
                        Layout.fillWidth: true
                        Layout.preferredHeight: 50
                        wrapMode: Text.Wrap
                        font.bold: true


                    }
                }

                Rectangle {
                    id: simParameters
                    width: parent.width
                    height: parent.height * 0.8
                    color : "transparent"

                    HorizontalHeaderView {
                        id: horizontalHeader
                        anchors.left: tableView.left
                        anchors.top: parent.top
                        syncView: tableView
                        model: [ "Dates", "ETP"]
                        clip: true
                    }

                    VerticalHeaderView {
                        id: verticalHeader
                        anchors.top: tableView.top
                        anchors.left: parent.left
                        syncView: tableView
                        clip: true
                    }

                    TableView {
                        id: tableView
                        width: parent.width
                        height: parent.height
                        anchors.left: verticalHeader.right
                        anchors.top: horizontalHeader.bottom
                        anchors.right: parent.right
                        anchors.bottom: parent.bottom
                        clip: true

                        columnSpacing: 0
                        rowSpacing: 0

                        model: TableModel {
                            id: tableModel
                            TableModelColumn { display: "Dates" }
                            TableModelColumn { display: "ETP" }

                            rows: [
                                    { Dates : "", ETP : ""},
                                    {  Dates : "", ETP : ""}
                                ]
                        }

                        delegate: Item {
                            implicitWidth: 70
                            implicitHeight: 20

                            Rectangle {
                                anchors.fill: parent
                                border.width: 0.5
                                color: "#fafafa"

                                Text {
                                    anchors.centerIn: parent
                                    text: model.display
                                    font.pixelSize: 10
                                    wrapMode: Text.WordWrap
                                    horizontalAlignment: Text.AlignHCenter
                                }
                            }
                        }
                    }


                }


            }


        }


    }
    function cleanFilePath(filePath) {
        if (filePath.startsWith("file:///")) {
            return filePath.substring(8);
        }
        return filePath;
    }

    function populateTable(columnMapping) {
        tableModel.clear();
        const mykeys = ["Dates","ETP"];

        // Trouver la longueur maximale en une seule passe
        const maxLength = mykeys.reduce((max, key) => Math.max(max, columnMapping[key]?.length || 0), 0);
        // Remplir le modèle de données
        for (let i = 0; i < maxLength; i++) {
            let rowData = {};
            mykeys.forEach(key => rowData[key] = columnMapping[key]?.[i] ?? "");
            tableModel.appendRow(rowData);
        }
    }
}
