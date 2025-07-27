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

    property string calibrationName : ""
    property string validationName : ""


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
            gridVisible : false
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
            name: calibrationName
            axisX: daxisX
            axisY: vaxisY
            color: "red"
        }
        LineSeries {
            id: seriesQValidation
            name: validationName
            axisX: daxisX
            axisY: vaxisY
            color: "green"
            visible : validationName === "" ? false : true
        }
    }

    function updateChart(dates_cal, q_cal_series, dates_val, q_val_series) {
        seriesQClibration.clear()
        seriesQValidation.clear()
        let i = 0
        qobsChart.maxValue = Math.max(qobsChart.maxValue, Math.max(...[...q_cal_series,...q_val_series]))
        for (i = 0; i < dates_cal.length; i++) {
            if (i < q_cal_series.length)
                seriesQClibration.append(new Date(dates_cal[i]).getTime(), q_cal_series[i])
        }
        for (i = 0; i < dates_val.length; i++) {
            if (i < q_val_series.length)
                seriesQValidation.append(new Date(dates_val[i]).getTime(), q_val_series[i])
        }
    }
    function setChart(dates_obs, q_obs_series) {
        seriesQ.clear()
        seriesQClibration.clear()
        seriesQValidation.clear()
        if (!dates_obs || dates_obs.length === 0)
            return;

        qobsChart.minDate = dates_obs[0]
        qobsChart.maxDate = dates_obs[dates_obs.length - 1]

        qobsChart.minValue = 0
        qobsChart.maxValue = Math.max(...q_obs_series)
        let i = 0
        for (i =0 ; i < dates_obs.length; i++) {
            if (i < q_obs_series.length)
                seriesQ.append(new Date(dates_obs[i]).getTime(), q_obs_series[i])
        }

    }

}
