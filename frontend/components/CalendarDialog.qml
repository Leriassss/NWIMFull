import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Dialog{
    modal: true
    property var calibration_dates
    property var user_calibration: {
        "calibration": calibrationYear.currentText + "-" + calibrationMonth.currentText + "-" + calibrationDay.currentText,
        "validation": validationYear.currentText + "-" + validationMonth.currentText + "-" + validationDay.currentText
    }


    Row {
        width: parent.width
        height: parent.height
        spacing: 0

        Rectangle {
            width: parent.width
            height: parent.height
            border.width: 1
            Column{
                width: parent.width
                height: parent.height
                padding: 5
                RowLayout{
                    spacing: 10
                    id : calibrationRow
                    width: parent.width
                    height: parent.height *0.5

                    Label{
                        text: "CALIBRATION"
                        font.bold: true
                        Layout.preferredWidth:  70
                    }

                    ComboBox {
                        id: calibrationYear
                        model : Object.keys(calibration_dates)
                        currentIndex: 0
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 30
                        onCurrentTextChanged: {
                            calibrationMonth.model = Object.keys(calibration_dates[calibrationYear.currentText])
                        }
                    }
                    Label{
                        text: "-"
                        font.bold: true
                    }

                    ComboBox {
                        id: calibrationMonth
                        currentIndex: 0
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 30
                        onCurrentTextChanged: {
                            calibrationDay.model =calibration_dates[calibrationYear.currentText][calibrationMonth.currentText]

                        }
                    }
                    Label{
                        text: "-"
                        font.bold: true
                    }
                    ComboBox {
                        id: calibrationDay
                        currentIndex: 0
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 30
                    }
                }

                RowLayout{
                    spacing: 10
                    id : validationRow
                    width: parent.width
                    height: parent.height *0.5

                    Label{
                        text: "VALIDATION"
                        font.bold: true
                        Layout.preferredWidth:  70
                    }

                    ComboBox {
                        id: validationYear
                        model : Object.keys(calibration_dates)
                        currentIndex: 0
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 30
                        onCurrentTextChanged: {
                            validationMonth.model = Object.keys(calibration_dates[validationYear.currentText])
                        }
                    }
                    Label{
                        text: "-"
                        font.bold: true
                    }

                    ComboBox {
                        id: validationMonth
                        currentIndex: 0
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 30
                        onCurrentTextChanged: {
                            validationDay.model =calibration_dates[validationYear.currentText][validationMonth.currentText]

                        }
                    }
                    Label{
                        text: "-"
                        font.bold: true
                    }
                    ComboBox {
                        id: validationDay
                        currentIndex: 0
                        Layout.preferredWidth: 100
                        Layout.preferredHeight: 30
                    }
                }

            }
        }

    }

}
