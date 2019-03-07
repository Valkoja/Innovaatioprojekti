import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2



ColumnLayout {
    width: 180
    //property string bus: "vcan0"
        Header {
            title: "CAN Bus"
            Layout.fillWidth: true
        }

        Text {
            id: busState
            text: canBusHandler.bus + " off"
            Layout.margins: 8
            Layout.fillWidth: true
            color: canBusHandler.state ? "green" : "red"
        }


        Text {
            id: processed
            Layout.margins: 8
            Layout.fillWidth: true
            text: "Messages processed " + canBusHandler.processed
        }

        ColumnLayout {
            Layout.fillWidth: true
            Layout.margins: 8
            Button {
                id: openDialog
                Layout.fillWidth: true
                text: "Select bus"
                onClicked: selectBusDialog.open();
            }
            Button {
                id: playLog
                Layout.fillWidth: true
                text: "Open bus"
                onClicked: {
                    canBusHandler.handleOpenBusClicked()
                }
            }
        }

        Dialog {
            id: selectBusDialog
            //modal: true
            standardButtons: Dialog.Ok
            Column {
                anchors.fill: parent
                Text {
                    text: "Bus"
                    height: 40
                }
                TextField {
                    id: canBusInput
                    width: parent.width * 0.75
                    focus: true
                    text: canBusHandler.bus
                }
            }
            onAccepted: {
                bus = canBusInput.text
            }
        }
}