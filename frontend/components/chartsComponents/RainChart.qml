import QtQuick
import QtQuick.Controls
import QtCharts 2.3
Rectangle {
    id : chartContainer
    visible: true
    property string minDate
    property string maxDate
    property real minValue
    property real maxValue
    property var barValues
    property var axisXValues

    property string chartName
    ChartView {
        id : chartView
        anchors.fill: parent
        antialiasing: true

        BarSeries {
                id: mySeries
                axisX: BarCategoryAxis {
                    categories: axisXValues
                }
                axisY: ValueAxis {
                    id: axisY
                    min:minValue
                    max:1.1*maxValue
                }
                BarSet { label: "Pluies"; values: barValues}
            }
    }

    function updateChart(dates, p_series) {
        chartContainer.minDate = dates[0]
        chartContainer.maxDate = dates[dates.length-1]
        chartContainer.minValue = Math.min(...p_series)
        chartContainer.maxValue = Math.max(...p_series)
        chartContainer.barValues = p_series
        chartContainer.axisXValues = dates
    }

}
