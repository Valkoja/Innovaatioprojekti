import QtQuick 2.11
import QtQuick.Controls 2.4
import QtQuick.Controls.Material 2.4
import QtQuick.Layouts 1.3

ApplicationWindow {
    visible: true
    property int margin: 11
    width: mainLayout.implicitWidth + 2 * margin
    height: mainLayout.implicitHeight + 2 * margin
    minimumWidth: mainLayout.Layout.minimumWidth + 2 * margin
    minimumHeight: mainLayout.Layout.minimumHeight + 2 * margin

    Material.theme: Material.Light
    Material.accent: Material.Blue

    ColumnLayout {
        id: mainLayout
        anchors.fill: parent
        anchors.margins: margin

        Text {
            text: {
                networking.getIP()
            }
            Layout.alignment: Qt.AlignHCenter
        }

        Button {
            text: qsTr("Start server")
            onClicked: {
                handler.handleButtonClicked()
            }
            Layout.alignment: Qt.AlignHCenter
            visible: false
        }

        ThingList {
            id: "ips"
        }

        CubeManager {
            id: "manager"
        }
    }
}