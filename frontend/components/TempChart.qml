import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {

    visible: true
    property var chartName
    property var cmap: {'Dates': [20090101, 20090102, 20090103, 20090104, 20090105, 20090106, 20090107],
        'ETP': [23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5],
        'P': [0.663632681, 0.139796256, 0.41181907, 0.569830784, 0.581204677, 6.490704477, 6.877533395],
        'Q': [3.941852194, 4.070039112, 3.687567001, 4.173076416, 4.070039112, 3.865270811, 4.04434715],
        'T': [23.5, 23.5, 23.5, 23.5, 23.5, 23.5, 23.5]}
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
            min: 20
            max: 24
        }

        LineSeries {
            id: seriesT
            name: "T"
            axisX: axisX
            axisY: axisY
        }

    }

    function updateChart(columnMapping) {
        seriesT.clear();
        var dates = columnMapping.Dates.map(function(date) {
            return new Date(
                Math.floor(date / 10000), // Année
                Math.floor((date % 10000) / 100) - 1, // Mois (0-11)
                date % 100 // Jour
            );
        });

        for (var i = 0; i < dates.length; i++) {
            var x = dates[i].getTime()
            if (columnMapping.T && i < columnMapping.T.length) {
                seriesT.append(x, columnMapping.T[i]);
            }
        }
    }
}
