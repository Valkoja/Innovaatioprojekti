import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import Piirto 1.0

ColumnLayout {
    RowLayout {
        width: 600
        Header {
            title: "Information"
            headerWidth: 600
        }
    }

    Timer {
        id: updateModelTimer
        interval: 5
        running: serverApp.running
        repeat: true
        onTriggered: piirto.setAngles(modelBridge.getBoomAngle(), modelBridge.getDiggingArmAngle(), modelBridge.getBucketAngle())
    }

    Piirto {
        id: piirto
        Layout.preferredWidth: 600
        Layout.preferredHeight: 800
    }
}