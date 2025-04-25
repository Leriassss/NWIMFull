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

    signal runningStart

    property string chartName



    ChartView {
        id: chartView
        anchors.fill: parent
        antialiasing: true
        legend.visible: true


        DateTimeAxis {
            id: daxisX
            format: fileHandler.userFormat
            titleText: "Dates"
            min: minDate
            max: maxDate
        }

        ValueAxis {
            id: vaxisY
            min: minValue
            max: 1.1 * maxValue
            titleText: "Streamflow"
        }

        LineSeries {
            id: seriesQ
            name: "Observed"
            axisX: daxisX
            axisY: vaxisY
            color: "blue"
        }

        LineSeries {
            id: seriesQModel
            name: "Predicted"
            axisX: daxisX
            axisY: vaxisY
            color: "red"
        }
    }

    function updateChart(dates, q_obs_series, q_sim_series) {
        seriesQ.clear()
        seriesQModel.clear()

        if (!dates || dates.length === 0)
            return;

        qobsChart.minDate = dates[0]
        qobsChart.maxDate = dates[dates.length - 1]

        // Fusionner les deux séries pour obtenir le min/max global
        var allValues = q_obs_series.concat(q_sim_series)
        qobsChart.minValue = Math.min(...allValues)
        qobsChart.maxValue = Math.max(...allValues)

        for (var i = 0; i < dates.length; i++) {
            var x = new Date(dates[i])
            var timestamp = x.getTime()

            if (i < q_obs_series.length)
                seriesQ.append(timestamp, q_obs_series[i])

            if (i < q_sim_series.length)
                seriesQModel.append(timestamp, q_sim_series[i])
        }
    }
}
