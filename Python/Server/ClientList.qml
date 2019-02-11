import QtQuick 2.11
import QtQuick.Layouts 1.3


Rectangle {
    width: 250
    Layout.fillHeight: true
    border.width: 1
    border.color: "black"
    GridLayout {
        Text {
            Layout.margins: 8
            text: "Clients"
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
}

