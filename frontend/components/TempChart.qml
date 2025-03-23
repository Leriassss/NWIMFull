import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {

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
            min:fileHandler.tempInfos["min"]
            max:1.1*fileHandler.tempInfos["max"]
        }

        LineSeries {
            id: seriesT
            name: "T"
            axisX: axisX
            axisY: axisY
        }

    }

    function updateChart() {
        seriesT.clear();
        var dates = fileHandler.datesInfos["data"];
        var temp_series = fileHandler.tempInfos["data"]

        for (var i = 0; i < dates.length; i++) {
            var x = new Date(dates[i]);
            if (temp_series && i < temp_series.length) {
                seriesT.append(x.getTime(), temp_series[i]);
            }
        }
    }
}
