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
            format: "yyyy-MM-dd"
            titleText: "Dates"
            min: "2009-01-01"
            max: "2023-12-31"
        }

        ValueAxis {
            id: axisY
            titleText: "Valeurs"
            min: 0
            max: 10
        }

        LineSeries {
            id: seriesQ
            name: "Q"
            axisX: axisX
            axisY: axisY
        }
    }

    function updateChart(columnMapping) {
        seriesQ.clear();
        var dates = columnMapping.Dates.map(function(date) {
            return new Date(
                Math.floor(date / 10000), // Année
                Math.floor((date % 10000) / 100) - 1, // Mois (0-11)
                date % 100 // Jour
            );
        });

        for (var i = 0; i < dates.length; i++) {
            var x = dates[i].getTime()
            if (columnMapping.Q && i < columnMapping.Q.length) {
                seriesQ.append(x, columnMapping.Q[i]);
            }
        }
    }
}
