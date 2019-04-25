import React from 'react';
import ReactDOM from 'react-dom';
import Dialog from './dialog';
import Handler from './handler';
import {INITIAL, CONNECTING, CONNECTED, NOTFOUND, DISCONNECTED} from './constants';
import './index.css';

class Root extends React.Component
{
    constructor(props) {
        super(props);

        this.state = {
            'connection': INITIAL,
            'address': '10.0.0.184'
        };

        this.setConnection = this.setConnection.bind(this);
    }

    setConnection(aConnection, aAddress) {
        switch (aConnection) {
            case DISCONNECTED:
                if (this.state.connection === CONNECTING) {
                    this.setState({'connection': NOTFOUND});
                }
                else {
                    this.setState({'connection': DISCONNECTED});
                }
                break;

            case CONNECTING:
                this.setState({'connection': CONNECTING, 'address': aAddress});
                break;

            default:
                this.setState({'connection': aConnection});
                break;
        }
    }

    render() {
        if (this.state.connection === CONNECTING || this.state.connection === CONNECTED) {
            return <Handler setConnection={this.setConnection} connection={this.state.connection} address={this.state.address} />
        }
        else {
            return <Dialog setConnection={this.setConnection} connection={this.state.connection} address={this.state.address} />
        }
    }
}

ReactDOM.render(<Root />, document.getElementById('root'));