import React from 'react';
import {CONNECTING, NOTFOUND, DISCONNECTED} from './constants';

class Dialog extends React.Component
{
    constructor(props) {
        super(props);
        this.state = {'address': this.props.address};
        this.handleInput = this.handleInput.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
    }

    handleInput(aEvent) {
        this.setState({'address': aEvent.target.value});
    }

    handleSubmit() {
        this.props.setConnection(CONNECTING, this.state.address);
    }

    render() {
        let title = '';

        switch(this.props.connection) {
            case NOTFOUND:
                title = 'Yhteyttä ei saatu avattua, tarkista osoite';
                break;
            case DISCONNECTED:
                title = 'Yhteys katkesi';
                break;
            default:
                title = 'Syötä palvelimen osoite';
                break;
        }

        return (
            <div>
                <h1>{title}</h1>
                <input type="text" value={this.state.address} onChange={this.handleInput} />
                <button onClick={this.handleSubmit}>Yhdistä</button>
            </div>
        );
    }
}

export default Dialog;