import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
Dialog{
    modal: true
    id : calendarDialog
    property var calibration_dates
    /*property var user_calibration: {
        "calibration": ["1985-01-01", "2006-12-31"],
        "validation": ["2007-01-01", "2015-12-31"]
    } //Beterou*/

    /*property var user_calibration: {
        "calibration": ["1999-01-01", "2001-12-31"],
        "validation": ["2002-01-01", "2003-12-31"]
    }*/

    /*property var user_calibration: {
        "calibration": ["1985-01-02", "1999-12-31"],
        "validation": ["2002-06-19", "2008-10-10"]
    } // Save*/

    /*property var user_calibration: {
        "calibration": ["1985-01-01", "1996-12-31"],
        "validation": ["2001-01-01", "2006-12-31"]
    } // Atcherigbe*/

    /*property var user_calibration: {
        "calibration": ["1995-01-01", "2006-12-31"],
        "validation": ["2007-01-01", "2010-12-31"]
    } //kaboua*/

    /*property var user_calibration: {
            "calibration": ["1996-01-01", "2005-12-31"],
            "validation": ["2010-01-01", "2015-12-31"]
        } //Zagnanando*/
    /*property var user_calibration: {
            "calibration": ["1987-01-01", "1999-12-31"],
            "validation": ["2000-01-01", "2005-12-31"]
        } //Bonou*/
    /*property var user_calibration: {
            "calibration": ["1994-01-01", "2006-12-31"],
            "validation": ["2007-01-01", "2012-12-31"]
        } //Dome*/
    property var user_calibration: {
            "calibration": ["1988-01-01", "2004-12-31"],
            "validation": ["2009-01-01", "2019-12-31"]
        } //Banankoro
    Row {
        width: parent.width
        height: parent.height
        spacing: 0

        Rectangle {
            width: parent.width
            height: parent.height
            border.width: 1
            border.color: "#ebebeb"
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
                            placeholderText: "Ex : 2000-12-31"
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
                            placeholderText: "Ex : 2000-12-31"
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
        let c_start = new Date(user_dates["calibration"][0]).getTime()
        let c_end   = new Date(user_dates["calibration"][1]).getTime()
        let v_start = new Date(user_dates["validation"][0]).getTime()
        let v_end   = new Date(user_dates["validation"][1]).getTime()

        // Vérification des bornes
        if (isNaN(c_start) || isNaN(c_end) || isNaN(v_start) || isNaN(v_end)) {
            return false; // une date invalide
        }

        if (c_start >= c_end ||
            v_start >= v_end ||
            c_start === v_start ||
            c_end   === v_end ||
            c_start === v_end) {
            return false
        }
        return true
    }

}
