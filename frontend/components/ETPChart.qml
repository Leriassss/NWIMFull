import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    width: 600
    height: 400
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
            max: "2009-01-07"
        }

        ValueAxis {
            id: axisY
            titleText: "Valeurs"
            min: 2
            max: 6
        }

        LineSeries {
            id: seriesETP
            name: "ETP"
            axisX: axisX
            axisY: axisY
        }


        Component.onCompleted: updateChart(cmap)
    }

    function updateChart(columnMapping) {
        seriesETP.clear();
        var dates = columnMapping.Dates.map(function(date) {
            return new Date(
                Math.floor(date / 10000),
                Math.floor((date % 10000) / 100) - 1,
                date % 100
            );
        });

        for (var i = 0; i < dates.length; i++) {
            var x = dates[i].getTime()
            if (columnMapping.ETP && i < columnMapping.ETP.length) {
                seriesETP.append(x, columnMapping.ETP[i]);
            }
        }
    }
}
