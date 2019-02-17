import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import SVGElement 1.0

ColumnLayout {
    // Miksi tämä korjaa tilanteen?
    anchors.fill: parent

    Header {
        title: "Information"
        width: parent.parent.width
    }

    SVGElement {
        id: svgViewport 
        // Layout.preferredWidth: 600
        // Layout.preferredHeight: 600
        Layout.fillWidth: true
        Layout.fillHeight: true
        boomAngle: modelWrapper.mainBoomAngle
        armAngle: modelWrapper.diggingArmAngle
        bucketAngle: modelWrapper.bucketAngle

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