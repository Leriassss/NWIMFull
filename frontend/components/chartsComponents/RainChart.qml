import QtQuick
import QtQuick.Controls
import QtCharts 2.3
Rectangle {
    id : chartContainer
    visible: true
    property date minDate
    property date maxDate
    property real minValue
    property real maxValue

    property string chartName
    ChartView {
        id: chartView
        title: chartName
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
            min:minValue
            max:1.1*maxValue
        }
        LineSeries {
            id: seriesP
            name: "Q"
            axisX: daxisX
            axisY: vaxisY
        }
    }
    function updateChart(dates, p_series) {
        if(p_series){
            seriesP.clear();
            chartContainer.minDate = dates[0]
            chartContainer.maxDate = dates[dates.length-1]
            chartContainer.minValue = Math.min(...p_series)
            chartContainer.maxValue = Math.max(...p_series)

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (i < p_series.length) {
                    seriesP.append(x.getTime(), p_series[i]);
                }
            }
        }

    }
}
