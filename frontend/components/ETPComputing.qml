import QtQuick
import QtQuick.Controls
import QtQuick.Layouts 1.15
import QtQuick.Effects
import "./parameters"
import "../../io/qml"
import io.qml
import Qt5Compat.GraphicalEffects
import Qt.labs.qmlmodels
Dialog {
    title: "PET Computation"
    implicitWidth:  1000
    implicitHeight: 700
    modal: true
    popupType: Popup.Window
    id: dialogOptim
    background: Rectangle{
        anchors.fill: parent
        color: "#fcffff"
    }
    closePolicy : Popup.CloseOnEscape
    //padding: 5
    x: Math.round((parent.width - width) / 2)
    y: Math.round((parent.height - height) / 2)

    DataErrorsDialog{
        id: petErrorsDialog
        title: "❌ ERREURS DETECTEES !!!"
        standardButtons: Dialog.Ok
        width: 400
        height: 300
        errors: etoManager.errors
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
    FileChoose {
         id: savePET
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["txt (*.txt)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(savePET.file.toString());
             etoManager.savePet(fileName)
         }
         onRejected: {
            console.log("Canceled")
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


    ColumnLayout{
        anchors.fill: parent
        spacing: 10
        SplitView {
            id: splitView
            Layout.preferredHeight: parent.height *0.9
            Layout.preferredWidth: parent.width
            Layout.alignment: Qt.AlignCenter
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
                color: "#eaf6f4"
                border.width: 1
                border.color: "gray"
                topLeftRadius: 5
                topRightRadius : 5
                SplitView.minimumWidth:  parent.width*0.3
                SplitView.preferredWidth: parent.width*0.3

                property var headers: etoManager.headers
                //width: parent.width*0.4
                //height: parent.height
                Column{
                    width: parent.width - 5
                    height: parent.height - 5
                    anchors.centerIn: parent
                    spacing: 2
                    clip: true
                    Row{
                        height: 40
                        width: parent.width
                        spacing: 25
                        Label {

                            id : methodsLabel
                            anchors.margins: 5
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "DATA MAPPING"
                            height: parent.height
                            horizontalAlignment: Qt.AlignHCenter
                            verticalAlignment: Qt.AlignVCenter
                            font.bold: true
                            font.pointSize: 10
                            padding: 5
                            color: "#000000"
                            width: parent.width
                            background: Rectangle {
                                anchors.fill: parent
                                topLeftRadius: 5
                                topRightRadius : 5
                                color : "#bae7fe"
                            }

                        }

                        Button {
                            text : "Load"
                            width: 90
                            height: parent.height
                            flat : true
                            font.bold: true
                            background: Rectangle{
                                anchors.fill: parent
                                radius: 5
                                border.color: "#b4b4b4"
                                border.width: 1
                                color: "#fcffff"
                            }
                            onClicked: {
                                loadETPparams.open()
                            }
                        }

                    }


                    GridLayout {
                        height:   parent.height*0.8
                        width:   parent.width * 0.5
                        columns: 3
                        columnSpacing: 5
                        rowSpacing: 10
                        property real comboBoxWidth: 100
                        Image{
                            source: "../icons/dates.png"
                            sourceSize.height: 20
                            sourceSize.width: 20

                        }
                        Label {
                            text: "Dates"
                            Layout.alignment: Qt.AlignLeft

                        }
                        ComboBox {
                            id: datesComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.preferredWidth: parent.comboBoxWidth
                        }
                        Image{
                            source: "../icons/tmean.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Teméprature Moy. [°C]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: tMeanComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.preferredWidth: parent.comboBoxWidth
                        }

                        Image{
                            source: "../icons/tmin.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Température Min. [°C]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: tMinComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.preferredWidth: parent.comboBoxWidth
                        }
                        Image{
                            source: "../icons/tmax.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Température Max. [°C]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: tMaxComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.preferredWidth: parent.comboBoxWidth
                        }
                        Image{
                            source: "../icons/humidity.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Humidité relative de l'air [%]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: rhComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.preferredWidth: parent.comboBoxWidth
                        }
                        Image{
                            source: "../icons/rad.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
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
                            Layout.preferredWidth: parent.comboBoxWidth
                        }
                        Image{
                            source: "../icons/windSpeed.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Vitesse moy. [m/s]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        ComboBox {
                            id: u2ComboBox
                            model: columnMappingDialog.headers
                            currentIndex: 0
                            Layout.preferredWidth: parent.comboBoxWidth
                        }

                        Image{
                            source: "../icons/latitude.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Latitude [rad]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        TextField {
                            id: lat
                            text : "5"
                            Layout.preferredWidth: parent.comboBoxWidth
                            validator: DoubleValidator {
                                bottom: 0
                                notation: DoubleValidator.StandardNotation
                            }
                        }
                        Image{
                            source: "../icons/elevation.png"
                            sourceSize.height: 20
                            sourceSize.width: 20
                        }
                        Label {
                            text: "Altitude [m]"
                            Layout.alignment: Qt.AlignLeft
                        }
                        TextField {
                            id: elevation
                            Layout.preferredWidth: parent.comboBoxWidth
                            text : "150"
                            validator: DoubleValidator {
                                bottom: 0
                                notation: DoubleValidator.StandardNotation
                            }
                        }
                    }




                }


            }

            Rectangle{
                border.width: 1
                border.color: "gray"
                SplitView.minimumWidth:  parent.width*0.2
                SplitView.preferredWidth: parent.width*0.3
                height: parent.height
                color: "#eaf6f4"
                topLeftRadius: 5
                topRightRadius : 5
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
                        height: 40
                        horizontalAlignment: Qt.AlignHCenter
                        verticalAlignment: Qt.AlignVCenter
                        font.bold: true
                        font.pointSize: 10
                        padding: 5
                        color: "#000000"
                        width: parent.width
                        background: Rectangle {
                            anchors.fill: parent
                            topLeftRadius: 5
                            topRightRadius : 5
                            color : "#bae7fe"
                        }
                    }

                    ColumnLayout{
                        height:   100
                        width:  parent.width *0.7
                        Row{
                            Layout.preferredHeight: 50
                            spacing: 10
                            Label{
                                text: "Methods"
                                font.bold: true
                                 anchors.verticalCenter:  parent.verticalCenter
                            }

                            ComboBox {
                                anchors.verticalCenter:  parent.verticalCenter
                                leftPadding: 10
                                width:  150
                                height:  30
                                id: methodSelector
                                model: etoManager.availableMethods
                                onCurrentValueChanged: {
                                        etoManager?.setMethod(methodSelector.currentText)
                                }
                                Component.onCompleted: {
                                        etoManager.setMethod(methodSelector.currentText)
                                }
                            }

                        }

                        Label{
                            text : "PARAMETRES REQUIS : "
                        }
                        ListView {
                            width: 180
                            height: 120


                            model: etoManager.methodParameters.split(",")
                            delegate:Label{
                                leftPadding: 5
                                text : "- " + modelData
                                Layout.fillWidth: true
                                Layout.preferredHeight: 50
                                wrapMode: Text.Wrap
                                font.bold: true

                            }

                        }

                        Button{
                            id : control
                            Layout.alignment: Qt.AlignRight
                            text: "Compute PET"
                            flat : true
                            font.bold: true
                            Layout.preferredWidth: 150
                            contentItem: Text {
                                text: control.text
                                font: control.font
                                opacity: enabled ? 1.0 : 0.3
                                color: "#fcffff"
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                                elide: Text.ElideRight
                            }
                            background: Rectangle{
                                anchors.fill : parent
                                color : "#3b7772"
                                radius: 5

                                height: 40
                            }
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

                                        petErrorsDialog.open()
                                    }
                                    else{
                                        try {
                                            etoManager.computeETo()

                                        } catch (error) {
                                            petErrorsDialog.errors = ["Required parameters not supplied "]
                                            petErrorsDialog.open()
                                        }
                                        populateTable(etoManager.etpComputed)

                                    }

                            }

                        }
                    }



                }


            }
            Rectangle{
                width: parent.width*0.4
                height: parent.height
                color: "#eaf6f4"
                border.width: 1
                border.color: "gray"
                topLeftRadius: 5
                topRightRadius : 5
                Column{
                    width: parent.width - 5
                    height: parent.height - 5
                    anchors.centerIn: parent
                    spacing: 2
                    clip: true
                    Row{
                        height: 40
                        width: parent.width
                        spacing: 25
                        Label {
                            anchors.margins: 5
                            anchors.horizontalCenter: parent.horizontalCenter
                            text: "RESULTS"
                            height: 40
                            horizontalAlignment: Qt.AlignHCenter
                            verticalAlignment: Qt.AlignVCenter
                            font.bold: true
                            font.pointSize: 10
                            padding: 5
                            color: "#000000"
                            width: parent.width
                            background: Rectangle {
                                anchors.fill: parent
                                topLeftRadius: 5
                                topRightRadius : 5
                                color : "#bae7fe"
                            }
                        }

                        Button {
                            text : "Save"
                            width: 90
                            height: parent.height

                            font.bold: true
                            background: Rectangle{
                                anchors.fill: parent
                                radius: 5
                                border.color: "#b4b4b4"
                                border.width: 1
                                color: "#fcffff"
                            }
                            onClicked:{
                                if(etoManager.etpComputed["Dates"].length ===0){
                                    petErrorsDialog.errors = ["No data found. Please compute a PET method before"]
                                    petErrorsDialog.open()
                                    return
                                }
                                savePET.open()
                            }
                        }
                    }


                    Rectangle {
                    height:  parent.height * 0.9
                    width: parent.width *0.9
                    id: simParameters

                    color : "transparent"

                    HorizontalHeaderView {
                        id: horizontalHeader
                        anchors.left: tableView.left
                        anchors.top: parent.top
                        syncView: tableView
                        width: parent.width
                        model: [ "Dates", "ETP"]
                        clip: true
                        delegate: Label {
                            color: "#000000"
                            width: 50
                            leftPadding: 5
                            font.bold: true
                            text: modelData
                            background: Rectangle{
                                color: "#c6f3fe"
                                anchors.fill: parent
                                border.color: "grey"
                                border.width: 1
                            }
                        }

                    }

                    VerticalHeaderView {
                        id: verticalHeader
                        anchors.top: tableView.top
                        anchors.left: parent.left
                        syncView: tableView
                        clip: true
                        delegate: Label {
                            color: "#000000"
                            width: 50
                            leftPadding: 5
                            font.bold: true
                            text: modelData
                            background: Rectangle{
                                color: "#c6f3fe"
                                anchors.fill: parent
                                border.color: "grey"
                                border.width: 1
                            }
                        }
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

                        delegate: TextField {
                            implicitWidth: simParameters.height * 0.2
                            implicitHeight: 20
                            text: model.display
                            font.pixelSize: 10
                            wrapMode: Text.WordWrap
                            horizontalAlignment: Text.AlignHCenter
                            background: Rectangle {
                                    // Fond transparent
                                    color: "#fafafa"

                                    // Bordure inférieure seule
                                    Rectangle {
                                        anchors.bottom: parent.bottom
                                        width: parent.width
                                        height: 1  // Épaisseur de la bordure
                                        border.color: "gray"
                                        border.width: 1
                                    }

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
