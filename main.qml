import QtQuick
import QtQuick.Controls
import QtQuick.Controls.Material
import QtQuick.Layouts

import "frontend/components"

ApplicationWindow {
    visible: true
    minimumWidth: 1350
    minimumHeight: 750
    maximumWidth: 1350
    maximumHeight: 750
    title: qsTr("NWIM")
    Material.theme: Material.Light
    Material.accent: Material.Blue

    FileChoose{
        id: fileChooseComponent
    }
    LoadData {
        id: loadDataDialog
    }
    /*GAP{
        id: gapOptim
    }*/

    MenuBarModel{
        height: parent.height * 0.1
        width: parent.width
        id: nwimMenuBar
        onOpenFileTriggered: {
            fileChooseComponent.openDialog()
        }
        onLoadDataTriggred: {
            loadDataDialog.open()
        }
        /*onGapTriggered: {
            console.log("OK")
            gapOptim.open()
        }*/
    }

    HomePage{

    }
}
