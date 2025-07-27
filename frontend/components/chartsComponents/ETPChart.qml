import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    id : etpChart
    visible: true
    property date minDate
    property date maxDate
    property real minValue
    property real maxValue
    property real pminValue
    property real pmaxValue

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
            max:maxValue
        }
        ValueAxis {
            id: axisTop
            min:minValue
            max:pmaxValue
            reverse : true
            visible : false
        }
        LineSeries {
            id: seriesQ2
            name: "P"
            axisX : axisX
            axisYRight : axisTop
            visible : false
        }
        LineSeries {
            id: seriesETP
            name: "ETP"
            axisX: axisX
            axisY: axisY
            color : "red"
        }

    }
    function updateCombinedChart(dates, etp_series, p_series) {
        seriesQ2.visible = true
        axisTop.visible = true
        if(etp_series && p_series){
            seriesETP.clear();
            seriesQ2.clear();
            etpChart.minDate = dates[0]
            etpChart.maxDate = dates[dates.length-1]
            etpChart.minValue = Math.min(...etp_series)
            etpChart.maxValue = 2*Math.max(...etp_series)
            etpChart.pminValue = Math.min(...p_series)
            etpChart.pmaxValue = 2*Math.max(...p_series) + etpChart.maxValue

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (etp_series && i < etp_series.length) {
                    seriesETP.append(x.getTime(), etp_series[i]);
                    seriesQ2.append(x.getTime(), p_series[i]);
                }
            }
        }
    }
    function updateChart(dates, etp_series) {
        seriesQ2.visible = false
        axisTop.visible = false
        if(etp_series){
            seriesETP.clear();
            etpChart.minDate = dates[0]
            etpChart.maxDate = dates[dates.length-1]
            etpChart.minValue = Math.min(...etp_series)
            etpChart.maxValue = 1.1*Math.max(...etp_series)

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (i < etp_series.length) {
                    seriesETP.append(x.getTime(), etp_series[i]);
                }
            }
        }
    }
}
