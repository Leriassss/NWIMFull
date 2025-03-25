import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    id: qobsChart
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
            id: vaxisY
            titleText: "Valeurs"
            min:minValue
            max:1.1*maxValue
        }

        LineSeries {
            id: seriesQ
            name: chartName
            axisX: daxisX
            axisY: vaxisY
        }
    }

    function updateChart(dates, q_series) {
        seriesQ.clear();
        qobsChart.minDate = dates[0]
        qobsChart.maxDate = dates[dates.length-1]
        qobsChart.minValue = Math.min(...q_series)
        qobsChart.maxValue = Math.max(...q_series)

        for (var i = 0; i < dates.length; i++) {
            var x = new Date(dates[i]);
            if (q_series && i < q_series.length) {
                seriesQ.append(x.getTime(), q_series[i]);
            }
        }
    }
}
