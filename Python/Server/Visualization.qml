import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

import "Visualization.js" as VisualizationFunctions

ColumnLayout {
    Header {
        title: "Information"
        width: parent.parent.width
    }

    Canvas {
        id: visualizationCanvas 
        renderStrategy: Canvas.Threaded
        Layout.preferredWidth: 700
        Layout.preferredHeight: 700
        onPaint: {
            visualizationCanvas.requestAnimationFrame(VisualizationFunctions.updateCanvas)
        }
        onPainted: {
            visualizationCanvas.requestPaint()
        }
    }
}