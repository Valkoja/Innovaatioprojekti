import QtQuick 2.9
import QtQuick.Layouts 1.3


ColumnLayout {
    width: 250
    Header {
        title: "Clients"
    }

    ListView {
        id: pythonList
        

        clip: true

        model: pythonListModel

        delegate: Component {
            Rectangle {
                width: pythonList.width
                height: 40
                color: ((index % 2 == 0)?"#222":"#111")
                Text {
                    id: title
                    elide: Text.ElideRight
                    text: model.thing.peer
                    color: "white"
                    font.bold: true
                    anchors.leftMargin: 10
                    anchors.fill: parent
                    verticalAlignment: Text.AlignVCenter
                }
                MouseArea {
                    anchors.fill: parent
                    onClicked: { controller.thingSelected(model.thing) }
                }
            }
        }
    }
}

