import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    id: qobsChart
    visible: true
    property date minDate
    property date maxDate
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
            id: seriesQClibration
            name: "Calibration"
            axisX: daxisX
            axisY: vaxisY
            color: "red"
        }
        LineSeries {
            id: seriesQValidation
            name: "Validation"
            axisX: daxisX
            axisY: vaxisY
            color: "green"
        }
    }

    function updateChart(dates_obs, q_obs_series, dates_cal, q_cal_series, dates_val, q_val_series) {
        seriesQ.clear()
        seriesQClibration.clear()
        seriesQValidation.clear()

        if (!dates_obs || dates_obs.length === 0)
            return;

        qobsChart.minDate = dates_obs[0]
        qobsChart.maxDate = dates_obs[dates_obs.length - 1]

        // Fusionner les deux séries pour obtenir le min/max global
        var allValues = q_obs_series.concat([...q_cal_series,...q_val_series])
        qobsChart.minValue = Math.min(...allValues)
        qobsChart.maxValue = Math.max(...allValues)
        let i = 0
        for (i =0 ; i < dates_obs.length; i++) {
            if (i < q_obs_series.length)
                seriesQ.append(new Date(dates_obs[i]).getTime(), q_obs_series[i])
        }
        for (i = 0; i < dates_cal.length; i++) {
            if (i < q_cal_series.length)
                seriesQClibration.append(new Date(dates_cal[i]).getTime(), q_cal_series[i])
        }
        for (i = 0; i < dates_val.length; i++) {
            if (i < q_val_series.length)
                seriesQValidation.append(new Date(dates_val[i]).getTime(), q_val_series[i])
        }
    }
}
