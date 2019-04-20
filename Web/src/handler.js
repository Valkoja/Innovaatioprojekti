import React from 'react';
import Websocket from 'react-websocket';
import Telemetry from './telemetry';
import Visuals from './visuals';
import {XSiteDataHelloMessage} from './constants';

class Handler extends React.Component
{
    constructor(props) {
        super(props);

        this.state = {response: null};
        this.socket = null;

        this.handleData = this.handleData.bind(this);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    handleData(aResponse) {
        try {
            let resObj = JSON.parse(aResponse);
            this.setState({'response': resObj.state});
        }
        catch(err) {
            alert(err);
        }
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


        

        // console.log('wat');
        // let result = JSON.parse(data);
        // this.setState({count: this.state.count + result.movement});
        // console.log(data);
        // console.log(aResponse);
    }

    handleOpen() {
        console.log('handleOpen');
        this.socket.sendMessage(JSON.stringify(XSiteDataHelloMessage));
    }

    handleClose() {

    }

    render() {
        return (
            <React.Fragment>
                <Websocket url = {'ws://' + this.props.ip + ':9000'}
                    onMessage = {this.handleData}
                    onOpen = {this.handleOpen}
                    onClose = {this.handleClose}
                    reconnect = {true}
                    debug = {true}
                    ref = {(aSocket) => { this.socket = aSocket; }} />
                <Telemetry />
                <Visuals />
            </React.Fragment>
        );
    }
}

// ref = {(aWebsocket) => { this.refWebSocket = aWebsocket; }} />

export default Handler;