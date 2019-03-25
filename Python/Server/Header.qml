import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

Rectangle {
    property string title
    property string extra: ""
    property int headerWidth
    color: "black"
    Layout.minimumHeight: 30
    Layout.minimumWidth: headerText.implicitWidth
    Layout.fillWidth: true
    Text {
        id: headerText
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.leftMargin: 8
        anchors.topMargin: 8
        text: title
        color: "white"
        font.weight: Font.Bold
    }
    Text {
        id: headerText2
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.rightMargin: 8
        anchors.topMargin: 8
        text: extra
        color: "white"
        font.weight: Font.Bold
    }
}
