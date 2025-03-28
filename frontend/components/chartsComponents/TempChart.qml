import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {

    id: tempChart
    visible: true
    property string minDate
    property string maxDate
    property real minValue
    property real maxValue

    property string chartName

    ChartView {
        id: chartView
        anchors.fill: parent
        antialiasing: true

        DateTimeAxis {
            id: daxisX
            format:fileHandler.userFormat
            titleText: "Dates"
            min:minDate
            max: maxDate
        }

        ValueAxis {
            id: axisY
            titleText: "Valeurs"
            min:minValue
            max:1.1*maxValue
        }

        LineSeries {
            id: seriesT
            name: "T"
            axisX: daxisX
            axisY: axisY
        }

    }

    function updateChart(dates, t_series) {
        if(t_series){
            console.log("---- temp series")
            console.log(t_series)
            seriesT.clear();
            tempChart.minDate = dates[0]
            tempChart.maxDate = dates[dates.length-1]
            tempChart.minValue = Math.min(...t_series)
            tempChart.maxValue = Math.max(...t_series)

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (t_series && i < t_series.length) {
                    seriesT.append(x.getTime(), t_series[i]);
                }
            }
        }

    }
}
