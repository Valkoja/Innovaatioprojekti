import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.2


ColumnLayout {
    spacing: 0
    Layout.fillWidth: true
    Header {
        title: "Logger"
    }
    ListView {
        Layout.minimumHeight: 120
        Layout.minimumWidth: parent.parent.width
        pixelAligned: true
        id: clientList
        clip: true
        model: appLogHandler.history
        delegate: ItemDelegate {
            Text {
                leftPadding: 8
                topPadding: 4
                text: modelData
            }
            height: 25
        }
        width: parent.width
        ScrollIndicator.vertical: ScrollIndicator { }
    }
}