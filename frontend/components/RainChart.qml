import QtQuick
import QtQuick.Controls
import QtCharts 2.3
Rectangle {
    id : chartView
    visible: true

    ChartView {
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
            min:fileHandler.pInfos["min"]
            max:1.1*fileHandler.pInfos["max"]
        }

        LineSeries {
            id: seriesQ
            name: "P"
            axisX: axisX
            axisY: axisY
        }
    }

    function updateChart() {
        seriesQ.clear();
        var dates = fileHandler.datesInfos["data"];
        var q_series = fileHandler.pInfos["data"]

        for (var i = 0; i < dates.length; i++) {
            var x = new Date(dates[i]);
            if (q_series && i < q_series.length) {
                seriesQ.append(x.getTime(), q_series[i]);
            }
        }
    }

}
