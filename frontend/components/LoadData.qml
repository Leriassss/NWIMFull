import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import Qt.labs.qmlmodels
import "."

Dialog {
    id: loadDataDialog
    title: "IMPORTATION"
    modal: true
    width: 1300
    height: 700
    standardButtons: Dialog.Ok | Dialog.Cancel
    padding: 5
    FileChoose{
        id:fileChooseComponent
    }

    Row{
        anchors.fill: parent
        spacing: 5
        padding: -5
        ColumnLayout {
            width: parent.width *0.3
            height: parent.height
            spacing: 5

            Row{
                width: parent.width
                height: parent.height*0.2
                spacing: 0
                Label{
                    text: "Location : "
                    anchors.verticalCenter: fileLocation.verticalCenter
                    padding: 5
                    anchors.rightMargin: 5
                }

                TextField{
                    id : fileLocation
                    width: parent.width*0.6
                    height: 30
                    text : fileChooseComponent.fileName
                }
                Button{
                    width: parent.width*0.2
                    text: "Browse"
                    height: 30

                    onClicked: {
                        fileChooseComponent.openDialog()
                    }
                }
            }

            // Contenu du tableau avec ScrollView
            ScrollView {
                width: parent.width
                height: parent.height*0.8 - 5
                leftPadding: 10
                id : dataTable
                TableView {
                    id: tableView
                    clip: true
                    interactive: true
                    rowSpacing: 0
                    columnSpacing: 0

                    model: TableModel {
                        id: tableModel
                        TableModelColumn { display: "Dates" }
                        TableModelColumn { display: "P" }
                        TableModelColumn { display: "T" }
                        TableModelColumn { display: "Q" }
                        TableModelColumn { display: "ETP" }

                        rows: [
                            { Dates: "Dates", P: "P", T: "T", Q: "Q", ETP: "ETP" },
                            { Dates: "2023-12-22", P: 3.1, T: 35.2, Q: 0.2, ETP: 4.50 },
                            { Dates: "2024-12-22", P: 2.3, T: 33.5, Q: 0.1, ETP: 3.50 },
                            { Dates: "2025-02-22", P: 8.9, T: 35.2, Q: 0.4, ETP: 1.50 },
                            { Dates: "2023-12-22", P: 3.1, T: 35.2, Q: 0.2, ETP: 4.50 },
                            { Dates: "2024-12-22", P: 2.3, T: 33.5, Q: 0.1, ETP: 3.50 },
                            { Dates: "2025-02-22", P: 8.9, T: 35.2, Q: 0.4, ETP: 1.50 },
                            { Dates: "2023-12-22", P: 3.1, T: 35.2, Q: 0.2, ETP: 4.50 },
                            { Dates: "2024-12-22", P: 2.3, T: 33.5, Q: 0.1, ETP: 3.50 },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" },
                            { Dates: "", P: "", T: "", Q: "", ETP: "" }
                        ]

                        function copyToClipboard(indexes) {
                            let text = ""
                            for (let i = 0; i < indexes.length; i++) {
                                let row = indexes[i].row
                                let col = indexes[i].column
                                text += this.rows[row][this.columns[col].name] + "\t"
                                if (col === this.columns.length - 1) {
                                    text += "\n"
                                }
                            }
                            Qt.application.clipboard.text = text
                        }

                        function pasteFromClipboard(targetIndex) {
                            let clipboardText = Qt.application.clipboard.text
                            let rows = clipboardText.split("\n")
                            console.log("**********************************")
                            console.log(rows)
                            for (let i = 0; i < rows.length; i++) {
                                let columns = rows[i].split("\t")
                                for (let j = 0; j < columns.length; j++) {
                                    let row = targetIndex.row + i
                                    let col = targetIndex.column + j
                                    if (row < this.rows.length && col < this.columns.length) {
                                        this.rows[row][this.columns[col].name] = columns[j]
                                    }
                                }
                            }
                            this.layoutChanged()
                        }
                    }

                    selectionModel: ItemSelectionModel {}

                    delegate: Rectangle {
                        implicitWidth: 75
                        implicitHeight: 25
                        required property bool selected
                        required property bool current
                        border.width: current ? 2 : 1
                        color: selected ? "lightblue" : "transparent"
                        Text {
                            text: model.display
                            anchors.centerIn: parent
                        }
                    }

                    Shortcut {
                        sequence: StandardKey.Copy
                        onActivated: {
                            let indexes = tableView.selectionModel.selectedIndexes
                            tableModel.copyToClipboard(indexes)
                        }
                    }

                    Shortcut {
                        sequence: StandardKey.Paste
                        onActivated: {
                            let targetIndex = tableView.selectionModel.currentIndex
                            tableModel.pasteFromClipboard(targetIndex)
                        }
                    }
                }
            }

            Rectangle{
                width: 100
                height: 40
                color: "transparent"
                anchors.horizontalCenter: parent.horizontalCenter
                Button{
                    text: "Edit"
                    anchors.fill: parent
                    anchors.top: dataTable.bottom

                }
            }


        }

        Column{
            width: parent.width *0.7
            height: parent.height
            spacing: 5

            Rectangle {
                id: simulationPane
                width: parent.width
                height: parent.height
                border.width: 2
                Column{
                    width: parent.width
                    height: parent.height

                    Rectangle{
                        id:plotOptions
                        width: parent.width
                        height: parent.height*0.15
                        border.width: 2

                        Row{
                            width: parent.width
                            height: parent.height
                            spacing: 6
                            Rectangle{
                                width: parent.width*0.5
                                height: parent.height
                                border.width: 2
                                Text{
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "CALIBRATION"
                                }


                            }
                            Rectangle{
                                border.width: 2
                                anchors.margins: 20
                                width: parent.width*0.5 - 6
                                height: parent.height
                                Text {
                                    anchors.margins: 5
                                    anchors.horizontalCenter: parent.horizontalCenter
                                    text: "PLOT"
                                }
                                Row{
                                    spacing: 6
                                    width: parent.width
                                    height: parent.height
                                    Rectangle{
                                        width: parent.width*0.5
                                        height:  parent.height*0.7
                                        anchors.bottom: parent.bottom
                                        border.width: 2
                                        Text {
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            text: "PARAMETERS"
                                        }
                                        Row {
                                            anchors.centerIn: parent
                                            width: parent.width
                                            spacing : 5
                                            leftPadding: 10
                                            CheckBox {
                                                checked: true
                                                text: "ETP"
                                            }
                                            CheckBox {
                                                text: "P"
                                            }
                                            CheckBox {
                                                text: "T"
                                            }
                                            CheckBox {
                                                text: "Q"
                                            }
                                        }
                                    }
                                    Rectangle{
                                        width: parent.width*0.5 - 6
                                        height: parent.height*0.7
                                        border.width: 2
                                        anchors.bottom: parent.bottom
                                        Text {
                                            anchors.horizontalCenter: parent.horizontalCenter
                                            text: "PERIOD"
                                        }
                                        Row {
                                            leftPadding: 10
                                            anchors.centerIn: parent
                                            width: parent.width
                                            CheckBox {
                                                checked: true
                                                text: "CALIBRATION"
                                                rightPadding: 5

                                            }
                                            CheckBox {

                                                text: "VALIDATION"
                                            }
                                        }
                                    }

                                }

                            }
                        }

                    }
                    Rectangle{
                        id : plot
                        width: parent.width
                        height: parent.height*0.85
                        border.width: 2
                        Rectangle{
                            width: parent.width
                            height: 25
                            border.width: 1
                            anchors.top: parent.top
                            Row{
                                spacing: 20
                                anchors.fill: parent
                                padding: 5
                                Label{
                                    leftPadding: 10
                                    rightPadding: 10
                                    text: "STATISTICS"

                                    //anchors.verticalCenter: parent.verticalCenter
                                }
                                Row{
                                    width: parent.width * 0.8
                                    height: parent.height
                                    spacing: 25

                                    Label{
                                        text: "Min :     "
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    Label{
                                        text : "Max :    "
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    Label{
                                        text: "Sum:     "
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    Label{
                                        text : "Mean :    "
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                    Label{
                                        text : "SD :    "
                                        verticalAlignment: Text.AlignVCenter
                                    }
                                }
                            }
                        }
                    }
                }
            }

        }
    }

    SelectionRectangle {
        target: tableView
    }
}
