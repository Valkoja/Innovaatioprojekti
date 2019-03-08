import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.2


ColumnLayout {
    spacing: 0
    Header {
        title: "Clients"
    }
    ListView {
        Layout.minimumHeight: 250
        Layout.minimumWidth: 275
        pixelAligned: true
        id: clientList
        clip: true
        model: clientListModel
        delegate: ItemDelegate {
            contentItem: 
                Item {
                    Text {
                        text: model.client.peer
                    }
                }
            width: parent.width
            onClicked: { controller.clientKicked(model.client) }
        }
        ScrollIndicator.vertical: ScrollIndicator { }
    }
}
