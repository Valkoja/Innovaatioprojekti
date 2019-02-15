import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Layouts 1.3
import QtGraphicalEffects 1.12

ApplicationWindow {
    id: serverApp
    title: "Server"
    visible: true
    property int margin: 8
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin

    color: "#607D8B"

    Material.theme: Material.Light
    //Material.accent: Material.Blue

    property bool running: false

    RowLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        spacing: 8

        ColumnLayout {
            Rectangle {
                width: 250
                Layout.fillHeight: true
                border.width: 1
                border.color: "black"
                LogPlayer {
                    id: log
                }
            }

            Rectangle {
                width: 250
                Layout.fillHeight: true
                border.width: 1
                border.color: "black"
                CanBus {
                    id: bus
                }
            }
        }

        Rectangle {
            width: 600
            Layout.minimumHeight: 600
            Layout.fillHeight: true
            border.width: 1
            border.color: "black"

            Visualization {
                id: visuals
            }
        }

        Rectangle {
            width: 250
            Layout.fillHeight: true
            border.width: 1
            border.color: "black"

            ClientList {
                id: clients
            }
        }
    }
}
