import React from 'react';
import Websocket from 'react-websocket';
import {XSiteDataHelloMessage} from './constants';

class Handler extends React.Component
{
    constructor(props) {
        super(props);

        this.handleData = this.handleData.bind(this);
        this.handleOpen = this.handleOpen.bind(this);
        this.handleClose = this.handleClose.bind(this);
    }

    handleData(data) {
        console.log('wat');
        // let result = JSON.parse(data);
        // this.setState({count: this.state.count + result.movement});
        console.log(data);
    }

    handleOpen() {
        console.log('handleOpen');
        this.refWebSocket.sendMessage(JSON.stringify(XSiteDataHelloMessage));
    }

    handleClose() {

    }

    render() {
        return (
            <React.Fragment>
                <Websocket url = 'ws://10.0.0.184:9000'
                    onMessage = {this.handleData}
                    onOpen = {this.handleOpen}
                    onClose = {this.handleClose}
                    reconnect = {true}
                    debug = {true}
                    ref = {(aWebsocket) => { this.refWebSocket = aWebsocket; }} />
            </React.Fragment>
        );
    }
}

export default Handler;