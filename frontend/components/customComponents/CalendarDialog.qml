import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Dialog {
    modal: true
    id : calendarDialog
    property var user_calibration: {
        "calibration": ["1990-01-01", "1992-12-31"],
        "validation": ["1993-01-01", "1994-12-31"]
    }

    Row {
        width: parent.width
        height: parent.height
        spacing: 0

        Rectangle {
            width: parent.width
            height: parent.height
            border.width: 1
            border.color: "#ebebeb"

            Column {
                width: parent.width
                height: parent.height
                padding: 5

                ColumnLayout {
                    spacing: 10
                    id : calibrationRow
                    width: parent.width
                    height: parent.height * 0.5

                    Label {
                        text: "CALIBRATION"
                        font.bold: true
                        Layout.preferredWidth: 70
                    }

                    Row {
                        width: 200
                        spacing: 10

                        Label { text: "Start " }
                        TextField {
                            id: calibrationStart
                            width: 100
                            placeholderText: "Ex : 1999-01-01"
                            background: Rectangle {
                                anchors.fill: parent
                                border.color: "black"
                                border.width: 1
                            }
                            onTextChanged: {
                                calendarDialog.user_calibration["calibration"][0] = text
                                calendarDialog.updateValidationUI()
                            }
                        }

                        Label { text: "End " }
                        TextField {
                            id: calibrationEnd
                            width: 100
                            placeholderText: "Ex : 2000-12-31"
                            background: Rectangle {
                                anchors.fill: parent
                                border.color: "black"
                                border.width: 1
                            }
                            onTextChanged: {
                                calendarDialog.user_calibration["calibration"][1] = text
                                calendarDialog.updateValidationUI()
                            }
                        }
                    }
                }

                ColumnLayout {
                    spacing: 10
                    id : validationRow
                    width: parent.width
                    height: parent.height * 0.5

                    Label {
                        text: "VALIDATION"
                        font.bold: true
                        Layout.preferredWidth: 70
                    }

                    Row {
                        width: 200
                        spacing: 10

                        Label { text: "Start " }
                        TextField {
                            id: validationStart
                            width: 100
                            placeholderText: "Ex : 1999-01-01"
                            background: Rectangle {
                                anchors.fill: parent
                                border.color: "black"
                                border.width: 1
                            }
                            onTextChanged: {
                                calendarDialog.user_calibration["validation"][0] = text
                                calendarDialog.updateValidationUI()
                            }
                        }

                        Label { text: "End " }
                        TextField {
                            id: validationEnd
                            width: 100
                            placeholderText: "Ex : 2000-12-31"
                            background: Rectangle {
                                anchors.fill: parent
                                border.color: "black"
                                border.width: 1
                            }
                            onTextChanged: {
                                calendarDialog.user_calibration["validation"][1] = text
                                calendarDialog.updateValidationUI()
                            }
                        }
                    }
                }
            }
        }
    }

    // Vérification logique
    function checkDates(user_dates) {
        let c_start = new Date(user_dates["calibration"][0]).getTime()
        let c_end   = new Date(user_dates["calibration"][1]).getTime()
        let v_start = new Date(user_dates["validation"][0]).getTime()
        let v_end   = new Date(user_dates["validation"][1]).getTime()

        if (isNaN(c_start) || isNaN(c_end) || isNaN(v_start) || isNaN(v_end)) {
            return false
        }
        if (c_start >= c_end || v_start >= v_end) {
            return false
        }
        if (c_start === v_start || c_end === v_end || c_start === v_end || c_end === v_start) {
            return false
        }
        if (c_start < v_end && v_start < c_end) {
            return false
        }
        return true
    }

    // Mise à jour UI
    function updateValidationUI() {
        let valid = checkDates(calendarDialog.user_calibration)

        calibrationStart.background.border.color = valid ? "black" : "red"
        calibrationEnd.background.border.color   = valid ? "black" : "red"
        validationStart.background.border.color  = valid ? "black" : "red"
        validationEnd.background.border.color    = valid ? "black" : "red"
    }
}
