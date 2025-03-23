import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    width: 600
    height: 400
    visible: true
    property var chartName

    ChartView {
        id: chartView
        title: chartName
        anchors.fill: parent
        antialiasing: true

        DateTimeAxis {
            id: axisX
            format:fileHandler.userFormat
            titleText: "Dates"
            min:fileHandler.datesInfos["min"]
            max: fileHandler.datesInfos["max"]
        }

        ValueAxis {
            id: axisY
            titleText: "Valeurs"
            min:fileHandler.etpInfos["min"]
            max:1.1*fileHandler.etpInfos["max"]
        }

        LineSeries {
            id: seriesETP
            name: "ETP"
            axisX: axisX
            axisY: axisY
        }

    }



    function updateChart() {
        seriesETP.clear();
        var dates = fileHandler.datesInfos["data"];
        var etp_series = fileHandler.etpInfos["data"]

        for (var i = 0; i < dates.length; i++) {
            var x = new Date(dates[i]);
            if (etp_series && i < etp_series.length) {
                seriesETP.append(x.getTime(), etp_series[i]);
            }
        }
    }
}
