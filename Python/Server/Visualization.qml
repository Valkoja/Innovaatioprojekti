import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

import "Visualization.js" as VisualizationFunctions

ColumnLayout {
    RowLayout {
        width: 600
        Header {
            title: "Information"
            headerWidth: 600
        }
    }

    Canvas {
        id: visualizationCanvas 
        renderStrategy: Canvas.Threaded
        width: 600
        height: 800
        onPaint: {
            visualizationCanvas.requestAnimationFrame(VisualizationFunctions.updateCanvas)
        }
        onPainted: {
            visualizationCanvas.requestPaint()
        }
    }
}