import QtQuick
import QtQuick.Controls
import QtQuick.Layouts
import QtQuick.Controls.Material

Rectangle {
    width: 400
    height: 250

    Column {
        anchors.centerIn: parent
        spacing: 10

        RowLayout {
            spacing: 0  // Évite un espace entre la zone de texte et le bouton
            width: 200  // Taille ajustée

            TextField {
                id: dateInput
                readOnly: true
                text: Qt.formatDate(new Date(), "dd/MM/yyyy")
                Layout.fillWidth: true
            }

            Button {
                text: "📅"
                flat: true
                onClicked: datePopup.open()
            }
        }

        Popup {
            id: datePopup
            modal: true
            focus: true
            width: 320
            height: 380
            closePolicy: Popup.CloseOnEscape | Popup.CloseOnPressOutside
            padding: 10

            Column {
                spacing: 10
                anchors.fill: parent

                // Sélection de l'année et du mois
                RowLayout {
                    spacing: 10
                    Layout.alignment: Qt.AlignHCenter

                    ComboBox {
                        id: yearCombo
                        model: ListModel {
                            Component.onCompleted: {
                                let currentYear = new Date().getFullYear()
                                for (let i = currentYear - 50; i <= currentYear + 50; i++) {
                                    append({ year: i })
                                }
                                currentIndex = 50  // Positionne sur l'année actuelle
                            }
                        }
                        textRole: "year"
                        width: 80
                        onCurrentIndexChanged: updateDaysGrid()
                    }

                    ComboBox {
                        id: monthCombo
                        model: ["Janvier", "Février", "Mars", "Avril", "Mai", "Juin",
                                "Juillet", "Août", "Septembre", "Octobre", "Novembre", "Décembre"]
                        width: 100
                        currentIndex: new Date().getMonth()
                        onCurrentIndexChanged: updateDaysGrid()
                    }
                }

                // Affichage des jours du mois
                GridView {
                    id: daysGrid
                    width: parent.width
                    height: 200
                    cellWidth: 40
                    cellHeight: 40
                    model: ListModel { id: daysModel }

                    delegate: Button {
                        text: model.day
                        width: 40
                        height: 40
                        onClicked: {
                            let selectedDate = new Date(yearCombo.currentText, monthCombo.currentIndex, model.day)
                            dateInput.text = Qt.formatDate(selectedDate, "dd/MM/yyyy")
                            datePopup.close()
                        }
                    }
                }
            }
        }
    }

    // Fonction pour mettre à jour les jours du mois
    function updateDaysGrid() {
        daysModel.clear()
        let year = parseInt(yearCombo.currentText)
        let month = monthCombo.currentIndex
        let daysInMonth = new Date(year, month + 1, 0).getDate()

        for (let i = 1; i <= daysInMonth; i++) {
            daysModel.append({ day: i })
        }
    }
}
