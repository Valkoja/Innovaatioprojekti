import React from 'react';
import Websocket from 'react-websocket';

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

    }

    handleClose() {

    }

    render() {
        return (
            <div>
                {/* Handler
                <Websocket url='ws://10.0.0.184:9000' onMessage={this.handleData.bind(this)} /> */}

                <Websocket url='ws://10.0.0.184:8888'
                    onMessage={this.handleData}
                    onOpen={this.handleOpen}
                    onClose={this.handleClose}
                    reconnect={true}
                    debug={true}
                    ref={(aWebsocket) => { this.refWebSocket = aWebsocket; }}/>
            </div>
        );
    }
}

export default Handler;