import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import SVGElement 1.0

ColumnLayout {
    // Miksi tämä korjaa tilanteen?
    anchors.fill: parent
    spacing: 0

    Header {
        title: "Visualization"
        width: parent.parent.width
    }

    SVGElement {
        id: svgViewport 

        /*
        Layout.preferredWidth: 600
        Layout.preferredHeight: 600
        */

        Layout.fillWidth: true
        Layout.fillHeight: true

        /*
        boomAngle: modelWrapper.mainBoomAngle
        armAngle: modelWrapper.diggingArmAngle
        bucketAngle: modelWrapper.bucketAngle
        */

        boomAngle: modelWrapper.mainBoomAngleQuaternion
        armAngle: modelWrapper.diggingArmAngleQuaternion
        bucketAngle: modelWrapper.bucketAngleQuaternion

        Component.onCompleted: {
            modelWrapper.changed.connect(reDraw)
        }
/*
        renderStrategy: Canvas.Threaded

        onPaint: {
            visualizationCanvas.requestAnimationFrame(VisualizationFunctions.updateCanvas)
        }
        onPainted: {
            visualizationCanvas.requestPaint()
        }
*/
    }
}