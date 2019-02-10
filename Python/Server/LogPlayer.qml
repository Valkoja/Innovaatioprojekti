import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.3



ColumnLayout {
        RowLayout {
            Layout.margins: 8
            Text {
                text: "Play a CAN log"
                Layout.fillWidth: true
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
            }
        }

        FileDialog {
            id: fdImport
            title: qsTr("File name")
            folder: shortcuts.home
            onAccepted: {
                let file = fdImport.fileUrl
                fileName.text = file.toString().split('/').pop()
                logPlayerHandler.handleLogFileSelected(file)
            }
        }
}