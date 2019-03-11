import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.2
import QtQuick.Layouts 1.3


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

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin
        RowLayout {

            spacing: 8

            ColumnLayout {
                Rectangle {
                    width: 180
                    Layout.fillHeight: true
                    border.width: 1
                    border.color: "black"
                    LogPlayer {
                        id: log
                    }
                }

                Rectangle {
                    width: 180
                    Layout.fillHeight: true
                    border.width: 1
                    border.color: "black"
                    CanBus {
                        id: bus
                    }
                }
            }

            Rectangle {
                Layout.minimumHeight: 700
                Layout.minimumWidth: 700
                Layout.fillHeight: true
                Layout.fillWidth: true
                border.width: 1
                border.color: "black"

                Visuals {
                    id: svgContainer
                }
            }

            ColumnLayout {
                Rectangle {
                    Layout.fillHeight: true
                    Layout.minimumWidth: 275
                    border.width: 1
                    border.color: "black"

                    ClientList {
                        id: clients
                    }
                }

                Rectangle {
                    //Layout.fillHeight: true
                    height: 400
                    Layout.minimumWidth: 275
                    border.width: 1
                    border.color: "black"

                    Information {
                        id: info
                    }
                }
            }
        }
        Rectangle {
            height: 150
            Layout.fillWidth: true
            border.width: 1
            border.color: "black"
            AppLog {

            }
        }
    }
}
