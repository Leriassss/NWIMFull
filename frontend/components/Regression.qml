import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtQuick.Effects
import "./parameters"
import "../../io/qml"
import "./chartsComponents"
import io.qml
import Qt5Compat.GraphicalEffects
import Qt.labs.qmlmodels
Dialog {
    title: "Machine Learning"
    implicitWidth:  1300
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
                        height:parent.height
                        text: qsTr("📥")
                        ToolTip.text: qsTr("Load Regression")
                        onClicked: {
                            loadRegressionDialog.open()
                        }
                    }
                    CustomToolButton {
                        width: 50
                        height:parent.height
                        text: qsTr("➕")
                        ToolTip.text: qsTr("Add Model")
                        onClicked: {
                            loadFileDialog.open()
                        }
                    }
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("🟢")
                        ToolTip.text: qsTr("Compute")
                        onClicked: {

                            regressionFile.singleCalibration(fileHandler.ptq, regComboBox.currentText)

                            regChart.updateChart([...fileHandler.ptq["CALIBRATION"]["Dates"], ...fileHandler.ptq["VALIDATION"]["Dates"]],
                                        [...fileHandler.ptq["CALIBRATION"]["Q"], ...fileHandler.ptq["VALIDATION"]["Q"]],
                                        [...regressionFile.simValues["CALIBRATION"], ...regressionFile.simValues["VALIDATION"]])

                        }
                    }
                    CustomToolButton {
                        width: 50
                        height: parent.height
                        text: qsTr("💾")
                        ToolTip.text: qsTr("Save Regression")
                        onClicked: {
                            saveRegressionDialog.open()
                        }
                    }
                }
            }


       }

    FileChoose {
         id: loadRegressionDialog
         title: "Please choose a folder"
         nameFilters: ["JSON (*.json)"]
         fileMode: FileChoose.OpenFile
         onAccepted: {
            let fileName = cleanFilePath(loadRegressionDialog.file.toString());
            regressionFile.loadParameters(fileName)

            let index = regComboBox.model.indexOf(regressionFile?.currentRegressor)
                 console.log(index)
                 if (index >= 0)
                    regComboBox.currentIndex = index;


         }
         onRejected: {
            console.log("Canceled")
         }
     }

    FileChoose {
         id: loadFileDialog
         title: "Please choose a folder"
         nameFilters: ["JSON (*.json)"]
         fileMode: FileChoose.OpenFiles
         onAccepted: {
            regressionFile.getParameters(loadFileDialog.files)

         }
         onRejected: {
            console.log("Canceled")
         }
     }

    FileChoose {
         id: saveRegressionDialog
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["JSON (*.json)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(saveRegressionDialog.file.toString());
            regressionFile.saveParameters(regComboBox.currentText, fileName)

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
            SplitView.minimumWidth:  parent.width*0.2
            SplitView.preferredWidth: parent.width*0.2

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
                    text: "MODELS"
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

                Rectangle{
                    width: parent.width
                    height: parent.height
                    Component {
                        id : paramsComponent
                        Rectangle {
                        width: parent.width
                        height: 150
                        color: "white"
                        border.color: "gray"
                        border.width: 1
                        required property string id
                        required property var loss
                        required property var pn
                        required property var sim
                        required property var qb

                        Row{
                            anchors.fill: parent
                            Column {
                                spacing: 6
                                width: parent.width
                                padding: 10
                                Button{
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "🗑️"
                                    width: 100
                                    //color : "red"
                                    onClicked: {
                                       regressionFile.deleteModel(id)
                                    }
                                }
                                Text {
                                    anchors.left: parent.left
                                    text: "File : " + id
                                    font.bold: true
                                }

                                Text {
                                    text: {
                                        let index = Object.keys(loss)[0]
                                        let value = JSON.stringify(loss[index]).replace(/"/g, " ");
                                        index + " : " + value
                                    }
                                    font.bold: true
                                }


                                Text {
                                    text: {
                                        let index = Object.keys(pn)[0]
                                        let value = JSON.stringify(pn[index]).replace(/"/g, " ");
                                        index + " : " + value
                                    }
                                    font.bold: true
                                }

                                Text {
                                    text: {
                                        let index = Object.keys(sim)[0]
                                        let value = JSON.stringify(sim[index]).replace(/"/g, " ");
                                        index + " : " + value
                                    }
                                    font.bold: true
                                }


                                Text {
                                    text: {
                                        let index = Object.keys(qb)[0]
                                        let value = JSON.stringify(qb[index]).replace(/"/g, " ");
                                        index + " : " + value
                                    }
                                    font.bold: true
                                }
                            }

                            }

                        }


                    }
                    ListView {
                        anchors.fill: parent
                        model: regressionFile.parametersList
                        delegate: paramsComponent

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
                    text: "PLOT"
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
                Row{
                    spacing: 5
                    width: parent.width
                    height: parent.height * 0.1

                    GroupBox{
                        height: parent.height
                        width: parent.width * 0.3
                        title: "Regressor"


                        ColumnLayout{
                            anchors.fill: parent
                            //border.width: 1

                            spacing : 10
                            ComboBox {
                                leftPadding: 10
                                Layout.preferredWidth: parent.width
                                Layout.preferredHeight: 20
                                id: regComboBox
                                model:regressionFile?.regressors
                            }
                        }


                    }

                    GroupBox{
                        height: parent.height
                        width: parent.width * 0.7 - parent.spacing
                        title: "Criteria"


                        RowLayout{
                            anchors.fill: parent
                            //border.width: 1
                            spacing : 10
                            ComboBox {
                                leftPadding: 10
                                Layout.preferredWidth: 90
                                Layout.preferredHeight: 20
                                id: criteriaComboBox
                                model: Object.keys(regressionFile?.metricsSummary)
                            }

                            Label{
                                Layout.preferredWidth: 100
                                text: "Calibration : "
                                font.bold: true
                            }
                            Text{
                                Layout.preferredWidth: 50
                                text: (regressionFile?.metricsSummary[criteriaComboBox.currentText][0])?.toFixed(3)
                            }
                            Label{
                                Layout.preferredWidth: 100
                                text: "Validation : "
                                font.bold: true
                            }
                            Text{
                                Layout.preferredWidth: 50
                                text:  (regressionFile?.metricsSummary[criteriaComboBox.currentText][1])?.toFixed(3)
                            }

                        }


                    }

                }



                Rectangle {
                    id: simParameters
                    width: parent.width
                    height: parent.height * 0.8
                    color : "transparent"

                    SimChart{
                        id: regChart
                        width: parent.width
                        height: parent.height

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

}

