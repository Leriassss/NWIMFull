import QtQuick
import QtQuick.Controls
import QtCharts 2.3

Rectangle {
    id : chartView
    visible: true
    property var cmap : ({})

    ValueAxis {
        id: axisY
        titleText: "Valeurs"
        min: 0
        max: 10
    }

    ChartView {
        anchors.fill: parent
        antialiasing: true
        BarSeries {
            id: mySeries
            axisX: BarCategoryAxis { categories: chartView.cmap.Dates}
            BarSet { id : pbarset ; label: "Pluie"; values: chartView.cmap.P }
        }

    }
    function updateChart(columnMapping) {
        chartView.cmap = columnMapping
    }
}
