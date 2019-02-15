import QtQuick 2.11
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.3


ColumnLayout {
        RowLayout {
            width: 250
            Header {
                title: "Play a CAN log"
                headerWidth: 250
            }
        }

        Text {
            id: fileName
            Layout.margins: 8
            Layout.fillWidth: true
            color: logPlayerHandler.state ? "green" : "red"
        }


        Text {
            id: processed
            Layout.margins: 8
            Layout.fillWidth: true
            text: "Messages processed " + logPlayerHandler.processed
        }

        RowLayout {
            Layout.fillWidth: true
            Layout.margins: 8
            Button {
                id: openDialog
                Layout.fillWidth: true
                text: "Open log"
                onClicked: fdImport.open();
            }
            Button {
                id: playLog
                Layout.fillWidth: true
                text: "Play log"
                onClicked: {
                    logPlayerHandler.handlePlayLogClicked()
                    serverApp.running = true
                }
                enabled: logPlayerHandler.hasFile ? true : false
            }
        }

        FileDialog {
            id: fdImport
            title: qsTr("File name")
            nameFilters: [ "Busmaster log files (*.log)" ]
            onAccepted: {
                let file = fdImport.fileUrl
                fileName.text = file.toString().split('/').pop()
                logPlayerHandler.handleLogFileSelected(file)
            }
        }
}