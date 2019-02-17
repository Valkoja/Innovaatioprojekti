import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

Rectangle {
    property string title
    property int headerWidth
    color: "black"
    Layout.minimumHeight: 30
    Layout.minimumWidth: headerText.implicitWidth
    Layout.fillWidth: true
    Text {
        id: headerText
        x: 8
        y: 8
        text: title
        color: "white"
        font.weight: Font.Bold
    }
}
