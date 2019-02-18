import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.3


ColumnLayout {
    width: 250
        function round(x) {
            return Number.parseFloat(x).toPrecision(5);
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
}