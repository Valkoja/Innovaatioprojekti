import QtQuick 2.11
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.12
import QtQuick.Layouts 1.3

Item {
    property string title
    property int headerWidth
    Layout.fillWidth: true
    Rectangle {
        color: "black"
        width: headerWidth
        height: 30
        Text {
            x: 8
            y: 8
            text: title
            color: "white"
            font.weight: Font.Bold
        }
    }
}
