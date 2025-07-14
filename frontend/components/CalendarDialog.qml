import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Dialog{
    modal: true
    id : calendarDialog
    property var calibration_dates
    property var user_calibration: {
        "calibration": ["", ""],
        "validation": ["", ""]
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
                ColumnLayout{
                    spacing: 10
                    id : calibrationRow
                    width: parent.width
                    height: parent.height *0.5

                    Label{
                        text: "CALIBRATION"
                        font.bold: true
                        Layout.preferredWidth:  70
                    }

                    Row{
                        width: 200
                        spacing: 10
                        Label{
                            text: "Start "
                        }
                        TextField{
                            id : calibrationStart
                            width: 100
                            placeholderText: "Ex : 1999-01-01"
                            onTextChanged: {
                                calendarDialog.user_calibration["calibration"][0] = text
                                if(!checkDates(calendarDialog.user_calibration)){
                                    calibrationStart.color = "red"
                                }
                                else{
                                    calibrationStart.color = "black"
                                }
                            }
                        }
                        Label{
                            text: "End "
                        }
                        TextField{
                            id : calibrationEnd
                            width: 100
                            placeholderText: "Ex : 1999-01-01"
                            onTextChanged: {
                                calendarDialog.user_calibration["calibration"][1] = text
                                if(!checkDates(calendarDialog.user_calibration)){
                                    calibrationEnd.color = "red"
                                }
                                else{
                                    calibrationEnd.color = "black"
                                }
                            }
                        }
                    }
                }
                ColumnLayout{
                    spacing: 10
                    id : validationRow
                    width: parent.width
                    height: parent.height *0.5

                    Label{
                        text: "VALIDATION"
                        font.bold: true
                        Layout.preferredWidth:  70
                    }

                    Row{
                        width: 200
                        spacing: 10
                        Label{
                            text: "Start "
                        }
                        TextField{
                            id : validationStart
                            width: 100
                            placeholderText: "Ex : 1999-01-01"
                            onTextChanged: {
                                calendarDialog.user_calibration["validation"][0] = text
                                if(!checkDates(calendarDialog.user_calibration)){
                                    validationStart.color = "red"
                                }
                                else{
                                    validationStart.color = "black"
                                }
                            }
                        }
                        Label{
                            text: "End "
                        }
                        TextField{
                            id : validationEnd
                            width: 100
                            placeholderText: "Ex : 1999-01-01"
                            onTextChanged: {
                                calendarDialog.user_calibration["validation"][1] = text
                                if(!checkDates(calendarDialog.user_calibration)){
                                    validationEnd.color = "red"
                                }
                                else{
                                    validationEnd.color = "black"
                                }
                            }
                        }
                    }
                }

            }
        }

    }
    function checkDates(user_dates){
        let c_start = new Date(user_dates["calibration"][0])
        let c_end = new Date(user_dates["calibration"][1])
        let v_start = new Date(user_dates["validation"][0])
        let v_end = new Date(user_dates["validation"][1])
        if (c_start >= c_end || v_start >= v_end || c_start == v_start || c_end == v_end || c_start == v_end){
            return false
        }
        else{
            return true
        }
    }
}
