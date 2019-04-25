import React from 'react';
import {CONNECTING} from './constants';

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
        return (
            <div>
                <input type="text" value={this.state.address} onChange={this.handleInput} />
                <button onClick={this.handleSubmit}>Yhdistä</button>
            </div>
        );
    }
}

export default Dialog;