import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2


ColumnLayout {
    width: 180
    spacing: 0
    Layout.minimumHeight: 250
    Header {
        title: "Play a CAN log"
    }

    Text {
        id: fileName
        Layout.margins: 8
        Layout.fillWidth: true
        color: logPlayerHandler.state == "ready" ? "green" : "red"
        text: "No file"
    }

    Text {
        id: processed
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Messages processed " + logPlayerHandler.processed
    }

    ColumnLayout {
        Layout.fillWidth: true
        Layout.margins: 8
        spacing: 0
        Button {
            id: openDialog
            Layout.fillWidth: true
            text: "Open log"
            enabled: logPlayerHandler.state == "nofile" || logPlayerHandler.state == "ready"  ? true : false
            onClicked: fdImport.open();
        }
        CheckBox {
            id: loopLog
            text: "Loop"
            checked: false
            enabled: logPlayerHandler.state == "ready" ? true : false
            onClicked: {
                logPlayerHandler.handleLoopLogClicked(checked)
            }
        }
        Button {
            id: playLog
            Layout.fillWidth: true
            text: "Play log"
            onClicked: {
                logPlayerHandler.handlePlayLogClicked()
                serverApp.running = true
            }
            enabled: logPlayerHandler.state == "ready" ? true : false
        }
        Button {
            id: stopLog
            Layout.fillWidth: true
            text: "Stop log"
            onClicked: {
                logPlayerHandler.handleStopLogClicked()
            }
            enabled: logPlayerHandler.state == "playing" ? true : false
        }
    }

    FileDialog {
        id: fdImport
        title: qsTr("File name")
        nameFilters: [ "Busmaster log files (*.log)" ]
        onAccepted: {
            var file = fdImport.fileUrl
            fileName.text = file.toString().split('/').pop()
            logPlayerHandler.handleLogFileSelected(file)
        }
    }
}