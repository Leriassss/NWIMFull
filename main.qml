import QtQuick
import QtQuick.Controls
//import QtQuick.Controls.Material
import QtQuick.Layouts
import Qt5Compat.GraphicalEffects

import "frontend/components"
//import "./frontend/components/parameters"
//import io.qt.test 1.0 as TestModule
//import "io/qt/rangeqarameterqml"
//import io.qt.rangeqarameterqml

ApplicationWindow {
    visible: true
    minimumWidth: 1350
    minimumHeight: 750
    maximumWidth: 1350
    maximumHeight: 750
    title: qsTr("NWIM")
    //Material.theme: Material.Light
    //Material.accent: Material.Blue

    menuBar:MenuBarModel{
        width: parent.width
        id: nwimMenuBar
        onOpenFileTriggered: {
            loadFileDialog.open()
        }
        onSaveTriggered: {
            //saveFileDialog.open()
            saveOptions.open()
        }

        onLoadDataTriggred: {
            //loadDataDialog.show()
            loadDataDialog.open()
        }
        onGapTriggered: {
            gapOptim.open()
        }
        onGridTriggered: {
            gridOptim.open()
        }
        onRegressionTriggered: {
            regression.open()
        }
        onPetTriggered: {
            etpComputing.open()
        }
        onBaseFlowTriggered: {
            baseflow.open()
        }
    }
    header: ToolBar {
            id: toolBar
            background: Rectangle{
                height: 1
                border.color: "#ebebeb"
                border.width: 1
            }

       }

    HomePage{
        id : homepage
        anchors.top: toolBar.bottom
        width: parent.width
        height: parent.height
    }

    footer : Rectangle{
        height: 35
        width: parent.width
        color: "#d8ffdb"
        //gradient: #d8ffdb
    }

    FileChoose{
        id: fileChooseComponent
    }

    FileChoose {
         id: loadFileDialog
         title: "Please choose a folder"
         nameFilters: ["JSON (*.json)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(loadFileDialog.file.toString());
             manualCalibration.loadParameters(fileName, homepage.parameter_bundle2)

         }
         onRejected: {
            console.log("Canceled")
         }
     }
    Dialog {
        id: saveOptions
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
        width: 300
        height: 200
        title: "Save options"
        Rectangle{
            anchors.fill: parent
            /*border.color: "grey"
            border.width: 1*/
            Column{
                anchors.fill: parent

                CustomRadioButton{
                    height: 50
                    width: parent.width
                    text: "Save Parameters"
                    onClicked: {
                        saveFileDialog.open()
                        saveOptions.close()
                    }

                }
                Rectangle{
                    width: parent.width
                    height: 1
                    color: "#ebebeb"
                }

                CustomRadioButton{
                    height: 50
                    width: parent.width
                    text: "Save Plot"

                }
                Rectangle{
                    width: parent.width
                    height: 1
                    color: "#ebebeb"
                }
                CustomRadioButton{
                    height: 50
                    width: parent.width
                    text: "Save Data"
                    onClicked: {
                        saveQSimDialog.open()
                        saveOptions.close()
                    }

                }

            }

        }


    }

    FileChoose {
         id: saveFileDialog
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["JSON (*.json)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(saveFileDialog.file.toString());
             manualCalibration.saveParameters(homepage.parameter_bundle2, fileName)

         }
         onRejected: {
            console.log("Canceled")
         }
     }

    FileChoose {
         id: saveQSimDialog
         title: "Please choose a folder"
         fileMode: FileChoose.SaveFile
         nameFilters: ["txt (*.txt)"]
         property string fileName: ""
         onAccepted: {
            fileName = cleanFilePath(saveQSimDialog.file.toString());
             manualCalibration.saveQSim(fileName)
         }
         onRejected: {
            console.log("Canceled")
         }
     }


    LoadData {
        id: loadDataDialog
        x: Math.round((parent.width - width) / 2)
        y: Math.round((parent.height - height) / 2)
    }
    Optimization{
        id: gapOptim
    }
    GridParametersDialog{
        id:  gridOptim
    }

    ETPComputing{
        id : etpComputing
    }

    Regression{
        id: regression
    }
    BaseFlow{
        id: baseflow
    }

    function cleanFilePath(filePath) {
        if (filePath.startsWith("file:///")) {
            return filePath.substring(8);
        }
        return filePath;
    }


}
