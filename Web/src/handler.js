import React from 'react';
import Websocket from 'react-websocket';
import Telemetry from './telemetry';
import Visuals from './visuals';
import {CONNECTED, DISCONNECTED, XSITEDATAHELLOMESSAGE} from './constants';

class Handler extends React.Component
{
    constructor(props) {
        super(props);

        this.websocket = null;
        this.state = {
            'limitWarnings': {
                'left': false,
                'right': false,
                'upper': false,
                'lower': false,
                'forward': false,
                'property': false,
                'overload': false},
            'zeroLevel': {
                'height_from_zero': 0.0,
                'distance_to_zero': 0.0,
                'height_to_slope_from_zero': 0.0},
            'anglesEuler': {
                'boom': 0.0,
                'arm': 0.0,
                'bucket': 0.0},
            'anglesQuaternion': {
                'boom': 0.0,
                'arm': 0.0,
                'bucket': 0.0}
        };

        this.handleData = this.handleData.bind(this);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    convertAngle(aQuart) {
        let sinr_cosp = +2.0 * (aQuart.w * aQuart.x + aQuart.y * aQuart.z)
        let cosr_cosp = +1.0 - 2.0 * (aQuart.x * aQuart.x + aQuart.y * aQuart.y)
        let roll = Math.atan2(sinr_cosp, cosr_cosp)

        return Math.round( roll * (180 / Math.PI) * 10 ) / 10;
    }

    handleMessage(aMsg) {
        try {
             let jsonMsg = JSON.parse(aMsg);

            if (jsonMsg.hasOwnProperty('state')) {
                let jsonState = jsonMsg.state;

                if (jsonState.hasOwnProperty('limitWarnings')) {
                    this.setState({'limitWarnings': {
                        'left': jsonState.limitWarnings.hasOwnProperty('left') ? jsonState.limitWarnings.left : this.state.limitWarnings.left,
                        'right': jsonState.limitWarnings.hasOwnProperty('right') ? jsonState.limitWarnings.right : this.state.limitWarnings.right,
                        'upper': jsonState.limitWarnings.hasOwnProperty('upper') ? jsonState.limitWarnings.upper : this.state.limitWarnings.upper,
                        'lower': jsonState.limitWarnings.hasOwnProperty('lower') ? jsonState.limitWarnings.lower : this.state.limitWarnings.lower,
                        'forward': jsonState.limitWarnings.hasOwnProperty('forward') ? jsonState.limitWarnings.forward : this.state.limitWarnings.forward,
                        'property': jsonState.limitWarnings.hasOwnProperty('property') ? jsonState.limitWarnings.property : this.state.limitWarnings.property,
                        'overload': jsonState.limitWarnings.hasOwnProperty('overload') ? jsonState.limitWarnings.overload : this.state.limitWarnings.overload
                    }});
                }

                if (jsonState.hasOwnProperty('zeroLevel')) {
                    this.setState({'zeroLevel': {
                        'height_from_zero': jsonState.zeroLevel.hasOwnProperty('height_from_zero') ? jsonState.zeroLevel.height_from_zero : this.state.zeroLevel.height_from_zero,
                        'distance_to_zero': jsonState.zeroLevel.hasOwnProperty('distance_to_zero') ? jsonState.zeroLevel.distance_to_zero : this.state.zeroLevel.distance_to_zero,
                        'height_to_slope_from_zero': jsonState.zeroLevel.hasOwnProperty('height_to_slope_from_zero') ? jsonState.zeroLevel.height_to_slope_from_zero : this.state.zeroLevel.height_to_slope_from_zero
                    }});
                }

                if (jsonState.hasOwnProperty('angles')) {
                    this.setState({'anglesEuler': {
                        'boom': jsonState.angles.hasOwnProperty('main_boom') ? jsonState.angles.main_boom / 10 : this.state.anglesEuler.boom,
                        'arm': jsonState.angles.hasOwnProperty('digging_arm') ? jsonState.angles.digging_arm / 10 : this.state.anglesEuler.arm,
                        'bucket': jsonState.angles.hasOwnProperty('bucket') ? jsonState.angles.bucket / 10 : this.state.anglesEuler.bucket
                    }});
                }

                if (jsonState.hasOwnProperty('quaternions')) {
                    this.setState({'anglesQuaternion': {
                        'boom': jsonState.quaternions.hasOwnProperty('main_boom_orientation') ? this.convertAngle(jsonState.quaternions.main_boom_orientation) : this.state.anglesQuaternion.boom,
                        'arm': jsonState.quaternions.hasOwnProperty('digging_arm_orientation') ? this.convertAngle(jsonState.quaternions.digging_arm_orientation) : this.state.anglesQuaternion.arm,
                        'bucket': jsonState.quaternions.hasOwnProperty('bucket_orientation') ? this.convertAngle(jsonState.quaternions.bucket_orientation) : this.state.anglesQuaternion.bucket
                    }});
                }
            };
        }
        catch(err) {
            alert(err);
        }

    }

    handleOpen() {
        console.log('Websocket open');
        this.props.setConnection(CONNECTED);
        this.websocket.sendMessage(JSON.stringify(XSITEDATAHELLOMESSAGE));
    }

    handleClose() {
        console.log('Websocket close');
        this.props.setConnection(DISCONNECTED);
    }

    render() {
        return (
            <React.Fragment>
                <Websocket
                    url = {'ws://' + this.props.address + ':9000'}
                    onMessage = {this.handleMessage}
                    onOpen = {this.handleOpen}
                    onClose = {this.handleClose}
                    reconnect = {true}
                    debug = {true}
                    ref = {(aSocket) => { this.websocket = aSocket; }} />
                <Telemetry
                    response = {this.state.response} />
                <Visuals
                    boomA = {this.state.response.anglesQuaternion.boom}
                    armA = {this.state.response.anglesQuaternion.arm}
                    bucketA = {this.state.response.anglesQuaternion.bucket} />
            </React.Fragment>
        );
    }
}

export default Handler;

/*
        {
            "id": 69,
            "state": {
                "limitWarnings": {
                    "left": false, 
                    "right": false, 
                    "upper": false, 
                    "lower": false, 
                    "forward": false, 
                    "property": false, 
                    "overload": false
                }, 
                "zeroLevel": {
                    "height_from_zero": 3.360196113586426, 
                    "distance_to_zero": 3.360196113586426, 
                    "height_to_slope_from_zero": 5.132124900817871
                }, 
                "angles": {
                    "frame_pitch": 0, 
                    "frame_roll": 4, 
                    "main_boom": 564, 
                    "digging_arm": -314, 
                    "bucket": -502, 
                    "heading": 0
                }, 
                "quaternions": {
                    "frame_orientation": {
                        "w": 1.00006103515625, 
                        "x": 0.0001220703125, 
                        "y": 0.00347900390625, 
                        "z": 0.0
                    }, 
                    "main_boom_orientation": {
                        "w": 0.8818359375, 
                        "x": 0.47174072265625, 
                        "y": 0.00225830078125, 
                        "z": -0.001220703125
                    }, 
                    "digging_arm_orientation": {
                        "w": 0.976318359375, 
                        "x": 0.21661376953125, 
                        "y": 0.001953125, 
                        "z": -0.00042724609375
                    }, 
                    "bucket_orientation": {
                        "w": 0.97381591796875, 
                        "x": -0.2271728515625, 
                        "y": -0.01495361328125, 
                        "z": -0.00347900390625
                    }
                }, 
                "slope": 0
            }, 
            "timestamp": "2019-04-20T22:20:37.650616", 
            "latency": 0, 
            "tickRate": 200.0
        }
*/