import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3


ColumnLayout {
    width: 275

    function round(x) {
        return parseFloat(x).toPrecision(5);
    }

    Header {
        title: "Information"
        Layout.fillWidth: true
    }

    Text {
        id: mainBoomAngleQuaternion
        Layout.topMargin: 8
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Main boom angle (quaternion): " + round(modelWrapper.mainBoomAngleQuaternion)
    }

    Text {
        id: diggingArmAngleQuaternion
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Digging arm angle (quaternion): " + round(modelWrapper.diggingArmAngleQuaternion)
    }

    Text {
        id: bucketAngleQuaternion
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Bucket angle (quaternion): " + round(modelWrapper.bucketAngleQuaternion)
    }

    Text {
        id: mainBoomAngle
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Main boom angle: " + modelWrapper.mainBoomAngle
    }

    Text {
        id: diggingArmAngle
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Digging arm angle: " + modelWrapper.diggingArmAngle
    }

    Text {
        id: bucketAngle
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Bucket angle: " + modelWrapper.bucketAngle
    }

    RowLayout {
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Text {
            id: limitLeft
            Layout.topMargin: 8
            Layout.bottomMargin: 4
            Layout.leftMargin: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningLeft ? "red" : "darkgreen"
            text: "left"
        }

        Text {
            id: limitRight
            Layout.topMargin: 4
            Layout.bottomMargin: 4
            Layout.leftMargin: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningRight ? "red" : "darkgreen"
            text: "right"
        }

        Text {
            id: limitUpper
            Layout.topMargin: 4
            Layout.bottomMargin: 4
            Layout.leftMargin: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningRight ? "red" : "darkgreen"
            text: "upper"
        }

        Text {
            id: limitLower
            Layout.topMargin: 4
            Layout.bottomMargin: 4
            Layout.leftMargin: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningRight ? "red" : "darkgreen"
            text: "lower"
        }
    }

    RowLayout {
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Text {
            id: limitForward
            Layout.margins: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningRight ? "red" : "darkgreen"
            text: "forward"
        }
        Text {
            id: limitProperty
            Layout.margins: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningRight ? "red" : "darkgreen"
            text: "property"
        }

        Text {
            id: limitOverload
            Layout.margins: 4
            Layout.fillWidth: true
            color: modelWrapper.limitWarningRight ? "red" : "darkgreen"
            text: "overload"
        }
    }

    Text {
        id: heightFromZero
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Height from zero: " + round(modelWrapper.heightFromZero)
    }

    Text {
        id: distanceToZero
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Distance to zero: " + round(modelWrapper.distanceToZero)
    }

    Text {
        id: heightToSlopeFromZero
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Height to slope from zero: " + round(modelWrapper.heightToSlopeFromZero)
    }

    Text {
        id: slope
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Layout.fillWidth: true
        text: "Slope: " + round(modelWrapper.slope)
    }

    RowLayout {
        Layout.topMargin: 4
        Layout.bottomMargin: 4
        Layout.leftMargin: 8
        Button {
            id: setZero
            Layout.fillWidth: true
            Layout.leftMargin: 8
            Layout.rightMargin: 8
            text: "Zero"
            onClicked: {
                modelWrapper.setZero()
            }
        }
        Button {
            id: getSlope
            Layout.fillWidth: true
            Layout.leftMargin: 8
            Layout.rightMargin: 8
            text: "Get Slope"
            onClicked: {
                modelWrapper.getSlope()
            }
        }
        Button {
            id: setSlope
            Layout.fillWidth: true
            Layout.leftMargin: 8
            Layout.rightMargin: 8
            text: "Set Slope"
            property double initialSlope
            onClicked: {
                initialSlope: modelWrapper.slope
                slopeDialog.open()
            }
            Dialog {
                id: slopeDialog
                modal: false
                width: 250
                y: -250
                x: -250
                contentItem:
                    Item {
                        ColumnLayout {
                            Text {
                                text: "Slope: " + setSlope.initialSlope
                                elide: Text.ElideRight
                            }
                            TextField {
                                id: slopeInput
                                text: setSlope.initialSlope
                                validator: DoubleValidator {bottom: -45.0; decimals: 2; top: 45.0;}
                            }
                        }
                    }
                footer:
                    DialogButtonBox {
                        Button {
                            text: "Cancel"
                            DialogButtonBox.buttonRole: DialogButtonBox.RejectRole
                        }
                        Button {
                            text: "Set"
                            enabled: slopeInput.acceptableInput
                            DialogButtonBox.buttonRole: DialogButtonBox.AcceptRole
                            onClicked: modelWrapper.setSlope(slopeInput.text)
                        }
                    }
            }
        }
    }
}