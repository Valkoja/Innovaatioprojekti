import QtQuick 2.9
import QtQuick.Layouts 1.3
import QtQuick.Controls 2.2


ColumnLayout {
    spacing: 0
    Header {
        title: "Clients"
        extra: networking.getIP()
    }
    ListView {
        Layout.minimumHeight: 250
        Layout.minimumWidth: 275
        pixelAligned: true
        id: clientList
        clip: true
        model: clientListModel
        delegate: ItemDelegate {
            height: delegateLayout.Layout.minimumHeight + 16 * 2
            contentItem:
                Item {
                    id: clientItem
                    property string library: model.client.library
                    property string peer: model.client.peer
                    property string platform: model.client.platform
                    ColumnLayout {
                        id: delegateLayout
                        Text {
                            text: clientItem.library + "@" + clientItem.peer + " on " + clientItem.platform
                            Layout.preferredWidth: 250
                            elide: Text.ElideRight
                        }
                        Text {
                            text: "latency: " + model.client.latency + " ms, tickrate: " + model.client.tickRate + " Hz"
                            Layout.preferredWidth: 250
                            elide: Text.ElideRight
                        }
                    }
                    Dialog {
                        id: clientDialog
                        x: -600
                        y: 50
                        modal: false
                        contentItem:
                            Item {
                                ColumnLayout {
                                    Text {
                                        text: "Peer: " + clientItem.peer
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        text: "Library: " + clientItem.library
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        text: "Platform: " + clientItem.platform
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        text: "Latency: " + model.client.latency + " ms"
                                        elide: Text.ElideRight
                                    }
                                    Text {
                                        text: "Tickrate: " + model.client.tickRate + " Hz"
                                        elide: Text.ElideRight
                                    }
                                    SpinBox {
                                        property int number: 0
                                        id: tickrateSpinBox
                                        from: 1
                                        to: 200
                                        stepSize: 1
                                        editable: true
                                        validator: IntValidator {
                                            bottom: Math.min(tickrateSpinBox.from, tickrateSpinBox.to)
                                            top: Math.max(tickrateSpinBox.from, tickrateSpinBox.to)
                                        }
                                        value: 200
                                        onValueModified: {
                                            model.client.setTickRate(value)
                                        }
                                    }
                                }
                            }
                        footer:
                            DialogButtonBox {
                                Button {
                                    text: "Close"
                                    DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
                                }
                                Button {
                                    text: "Kick"
                                    DialogButtonBox.buttonRole: DialogButtonBox.DestructiveRole
                                    onClicked: controller.clientKicked(model.client)
                                }
                            }
                    }
                }
            width: parent.width
            onClicked: { clientDialog.open() }
        }
        ScrollIndicator.vertical: ScrollIndicator { }
    }

}
