import QtQuick 2.11
import QtQuick.Controls 2.0
import QtQuick.Controls.Material 2.0
import QtQuick.Layouts 1.3

ColumnLayout {
    property int valueWidth: 30
    Text {
        text: "Cube"
        Layout.alignment: Qt.AlignHCenter
    }

    RowLayout {
        Text {
            text: "X"
        }
        Slider { 
            id: "x"
            value: 0.50
            stepSize: 0.01
            onMoved: {
                sliderHandler.handleSliderMoved("x", x.value)
            }
        }
        Text {
            text: {
                Math.round(x.value * 100) / 100;
            }
            Layout.minimumWidth: valueWidth
        }
    }
    RowLayout {
        Text {
            text: "Y"
        }
        Slider { 
            id: "y"
            value: 0.5
            stepSize: 0.01
            onMoved: {
                sliderHandler.handleSliderMoved("y", y.value)
            }
        }
        Text {
            text: {
                Math.round(y.value * 100) / 100;
            }
            Layout.minimumWidth: valueWidth
        }
    }
    RowLayout {
        Text {
            text: "Z"
        }
        Slider { 
            id: "z"
            value: 0.5
            stepSize: 0.01
            onMoved: {
                sliderHandler.handleSliderMoved("z", z.value)
            }
        }
        Text {
            text: {
                Math.round(z.value * 100) / 100;
            }
            Layout.minimumWidth: valueWidth
        }
    }
}