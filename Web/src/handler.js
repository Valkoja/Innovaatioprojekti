import React from 'react';
import Websocket from 'react-websocket';

class Handler extends React.Component
{
    // constructor(props) {
    //     super(props);
    // }

    handleData(data) {
        let result = JSON.parse(data);
        // this.setState({count: this.state.count + result.movement});
        console.log(data);
    }

    render() {
        return (
            <div>
                Handler
                <Websocket url='ws://localhost:8888/live/product/12345/' onMessage={this.handleData.bind(this)} />
            </div>
        );
    }
}

export default Handler;