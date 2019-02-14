import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import Piirto 1.0

Rectangle {
    width: 600
    height: 600
    border.width: 1
    border.color: "black"

    ColumnLayout {
        RowLayout {
            Text {
                Layout.margins: 8
                text: "Information"
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
}