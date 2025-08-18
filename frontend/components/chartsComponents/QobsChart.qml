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
    property real pminValue
    property real pmaxValue

    property string chartName



    ChartView {
        id: chartView
        anchors.fill: parent
        antialiasing: true
        title: chartName

        DateTimeAxis {
            id: daxisX
            format:fileHandler.userFormat
            titleText: "Dates"
            min:minDate
            max: maxDate
        }

        ValueAxis {
            id: vaxisY
            min:minValue
            max:maxValue
        }
        ValueAxis {
            id: axisY
            min:minValue
            max:pmaxValue
            reverse : true
            visible : false
        }
        LineSeries {
            id: seriesQ2
            name: "P"
            axisX : daxisX
            axisYRight : axisY
            visible : false
        }
        LineSeries {
            id: seriesQ
            name: "Q"
            axisX: daxisX
            axisY: vaxisY
        }
        MouseArea {
                   id: mouseArea
                   anchors.fill: parent
                   hoverEnabled: true

                   onPositionChanged: (mouse) => {
                       // conversion pixel -> valeur (x,y) du graphique
                       let value = chartView.mapToValue(Qt.point(mouse.x, mouse.y), seriesQ)
                       let dateX = new Date(value.x)
                       tooltip.x = mouse.x + 15
                       tooltip.y = mouse.y - 10
                       tooltip.text = "x: " + Qt.formatDateTime(dateX, "yyyy-MM-dd") + ", y: " + value.y.toFixed(2)
                       tooltip.visible = true
                   }

                   onExited: tooltip.visible = false
               }

               // Petit texte flottant qui suit la souris
               Label {
                   id: tooltip
                   visible: false
                   color: "black"
                   font.pixelSize: 12
                   text: ""
               }
    }

    function updateCombinedChart(dates, q_series, p_series) {
        seriesQ2.visible = true
        axisY.visible = true
        if(q_series && p_series){
            seriesQ.clear();
            seriesQ2.clear();
            let finite_q_series = q_series.filter(Number.isFinite)
            let finite_p_series = p_series.filter(Number.isFinite)

            qobsChart.minDate = dates[0]
            qobsChart.maxDate = dates[dates.length-1]
            qobsChart.minValue = Math.min(...finite_q_series)
            qobsChart.maxValue = 2*Math.max(...finite_q_series)
            qobsChart.pminValue = Math.min(...finite_p_series)
            qobsChart.pmaxValue = 2*Math.max(...finite_p_series) + qobsChart.maxValue

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (q_series && i < q_series.length) {
                    seriesQ.append(x.getTime(), q_series[i]);
                    seriesQ2.append(x.getTime(), p_series[i]);
                }
            }
        }

    }
    function updateChart(dates, q_series) {
        seriesQ2.visible = false
        axisY.visible = false
        if(q_series){
            seriesQ.clear();
            seriesQ2.clear();
            let finite_q_series = q_series.filter(Number.isFinite)
            qobsChart.minDate = dates[0]
            qobsChart.maxDate = dates[dates.length-1]
            qobsChart.minValue = Math.min(...finite_q_series)
            qobsChart.maxValue = 1.1*Math.max(...finite_q_series)

            for (var i = 0; i < dates.length; i++) {
                var x = new Date(dates[i]);
                if (q_series && i < q_series.length) {
                    seriesQ.append(x.getTime(), q_series[i]);
                }
            }
        }

    }
}
