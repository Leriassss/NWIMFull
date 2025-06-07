import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    id : etpChart
    width: 600
    height: 400
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
            id: axisX
            format:fileHandler.userFormat
            titleText: "Dates"
            min:minDate
            max: maxDate
        }

        ValueAxis {
            id: axisY
            //titleText: "Valeurs"
            min:minValue
            max:1.1*maxValue
        }

        LineSeries {
            id: seriesETP
            name: "ETP"
            axisX: axisX
            axisY: axisY
        }

    }
    function updateChart(dates, etp_series) {
        if(etp_series){
            console.log("---- qseries")
            console.log(etp_series)
            seriesETP.clear();
            etpChart.minDate = dates[0]
            etpChart.maxDate = dates[dates.length-1]
            etpChart.minValue = Math.min(...etp_series)
            etpChart.maxValue = Math.max(...etp_series)

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (etp_series && i < etp_series.length) {
                    seriesETP.append(x.getTime(), etp_series[i]);
                }
            }
        }
    }
}
