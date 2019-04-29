import React from 'react';

class Telemetry extends React.Component
{
    constructor(props) {
        super(props);
        this.updateTick = this.updateTick.bind(this);
    }

    shouldComponentUpdate() {
        // Prevent re-renders, updateTick will force updates
        return false;
    }

    componentDidMount() {
        let intervalID = setInterval(this.updateTick, 50);
        this.setState({'intervalID': intervalID});
    }

    componentWillUnmount() {
        clearInterval(this.state.intervalID);
    }

    updateTick() {
        this.forceUpdate();
    }

    render() {
        return (
            <div id='telemetry'>
                <table>
                    <tbody>
                        <tr><th colSpan='2'>Limit warnings:</th></tr>
                        <tr><td>Left:</td><td>{this.props.limitWarnings.left ? 'true' : 'false'}</td></tr>
                        <tr><td>Right</td><td>{this.props.limitWarnings.right ? 'true' : 'false'}</td></tr>
                        <tr><td>Upper:</td><td>{this.props.limitWarnings.upper ? 'true' : 'false'}</td></tr>
                        <tr><td>Lower:</td><td>{this.props.limitWarnings.lower ? 'true' : 'false'}</td></tr>
                        <tr><td>Forward:</td><td>{this.props.limitWarnings.forward ? 'true' : 'false'}</td></tr>
                        <tr><td>Property:</td><td>{this.props.limitWarnings.property ? 'true' : 'false'}</td></tr>
                        <tr><td>Overload:</td><td>{this.props.limitWarnings.overload ? 'true' : 'false'}</td></tr>
                    </tbody>
                </table>

                <table>
                    <tbody>

                        <tr><th colSpan='2'>Zero level:</th></tr>
                        <tr><td>Height from zero:</td><td>{Math.round(this.props.zeroLevel.height_from_zero * 100) / 100}</td></tr>
                        <tr><td>Distance to zero:</td><td>{Math.round(this.props.zeroLevel.distance_to_zero * 100) / 100}</td></tr>
                        <tr><td>Height to slope from zero:</td><td>{Math.round(this.props.zeroLevel.height_to_slope_from_zero * 100) / 100}</td></tr>
                    </tbody>
                </table>

                <table>
                    <tbody>

                        <tr><th colSpan='2'>Euler angles:</th></tr>
                        <tr><td>Main boom:</td><td>{this.props.anglesEuler.boom}</td></tr>
                        <tr><td>Digging arm:</td><td>{this.props.anglesEuler.arm}</td></tr>
                        <tr><td>Bucket:</td><td>{this.props.anglesEuler.bucket}</td></tr>
                        </tbody>
                </table>

                <table>
                    <tbody>
                        <tr><th colSpan='2'>Quaternion angles:</th></tr>
                        <tr><td>Main boom:</td><td>{this.props.anglesQuaternion.boom}</td></tr>
                        <tr><td>Digging arm:</td><td>{this.props.anglesQuaternion.arm}</td></tr>
                        <tr><td>Bucket:</td><td>{this.props.anglesQuaternion.bucket}</td></tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Telemetry;