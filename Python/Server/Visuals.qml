import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import SVGElement 1.0

ColumnLayout {
    anchors.fill: parent
    spacing: 0

    Header {
        title: "Visualization"
        width: parent.parent.width
    }

    SVGElement {
        id: svgViewport 

        Layout.fillWidth: true
        Layout.fillHeight: true

        // boomAngle: Math.round(modelWrapper.mainBoomAngleQuaternion * 10) / 10;
        // armAngle: Math.round(modelWrapper.diggingArmAngleQuaternion * 10) / 10;
        // bucketAngle: Math.round(modelWrapper.bucketAngleQuaternion * 10) / 10;

        boomAngle: modelWrapper.mainBoomAngleQuaternion;
        armAngle: modelWrapper.diggingArmAngleQuaternion;
        bucketAngle: modelWrapper.bucketAngleQuaternion;

        Component.onCompleted: {
            modelWrapper.changed.connect(reDraw)
        }
    }
}