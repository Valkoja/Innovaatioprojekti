import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import QtQuick.Dialogs 1.2



ColumnLayout {
    width: 180
    spacing: 0

    Header {
        title: "CAN Bus"
        Layout.fillWidth: true
    }

    ComboBox {
        id: busSelectComboBox
        Layout.minimumWidth: 164
        Layout.leftMargin: 8
        model: canBusHandler.available
        textRole: "toString"
        enabled: canBusHandler.state == "open" ? false : true
        delegate: ItemDelegate {
            text: modelData.interface + "/" + modelData.channel
            width: 164
        }
        onCurrentIndexChanged: {
            canBusHandler.handleBusSelected(currentIndex)
        }
    }

    Button {
        id: scanBus
        Layout.fillWidth: true
        Layout.leftMargin: 8
        Layout.rightMargin: 8
        text: "Scan"
        enabled: canBusHandler.state == "open" ? false : true
        onClicked: canBusHandler.handleScanClicked();
    }

    Text {
        id: processed
        Layout.margins: 8
        Layout.fillWidth: true
        text: "Messages processed " + canBusHandler.processed
    }

    Button {
        id: openBus
        Layout.fillWidth: true
        Layout.leftMargin: 8
        Layout.rightMargin: 8
        text: "Open bus"
        enabled: canBusHandler.state == "ready" ? true : false
        onClicked: {
            canBusHandler.handleOpenBusClicked()
            modelWrapper.getZero()
        }
    }
    Button {
        id: stopBus
        Layout.fillWidth: true
        Layout.leftMargin: 8
        Layout.rightMargin: 8
        text: "Close bus"
        enabled: canBusHandler.state == "open" ? true : false
        onClicked: {
            canBusHandler.handleCloseBusClicked()
        }
    }

    Dialog {
        id: busErrored
        standardButtons: Dialog.Ok
        visible: canBusHandler.errorMessage != "" ? true : false
        Text {
            text: canBusHandler.errorMessage
            height: 40
        }
        onAccepted: {
            canBusHandler.handleErrorAcknowledgedClicked()
        }
    }
}