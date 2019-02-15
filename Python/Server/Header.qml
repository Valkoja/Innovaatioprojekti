import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

Item {
    property string title
    property int headerWidth
    Layout.fillWidth: true
    height: 30
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
