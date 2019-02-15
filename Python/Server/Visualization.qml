import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

import "Visualization.js" as VisualizationFunctions

Rectangle {
    width: 600
    height: 600
    border.width: 1
    border.color: "black"

    ColumnLayout {
        RowLayout {
            Text {
                Layout.margins: 8
                text: "Information"
            }
        }

        Timer {
            id: updateModelTimer
            interval: 5
            running: serverApp.running
            repeat: true
            onTriggered: visualizationCanvas.requestPaint()
        }

		Canvas {
			id: visualizationCanvas
			width: 600
			height: 800
			onPaint: VisualizationFunctions.updateCanvas()
		}
    }
}