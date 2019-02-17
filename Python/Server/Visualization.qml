import QtQuick 2.9
import QtQuick.Controls 2.2
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3
import SVGView 1.0

ColumnLayout {
    Header {
        title: "Information"
        width: parent.parent.width
    }

    SVGView {
        id: visualizationCanvas 
        Layout.preferredWidth: 700
        Layout.preferredHeight: 700

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