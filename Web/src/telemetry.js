import React from 'react';

class Telemetry extends React.Component
{
    // constructor(props) {
    //     super(props);
    // }

    render() {
        return (
            <div>
                <h1>Telemetry</h1>
                <table>
                    <tbody>
                        <tr><th colSpan='2'>Limit warnings:</th></tr>
                        <tr><td>Left:</td><td>{this.props.response.limitWarnings.left}</td></tr>
                        <tr><td>Right</td><td>{this.props.response.limitWarnings.right}</td></tr>
                        <tr><td>Upper:</td><td>{this.props.response.limitWarnings.upper}</td></tr>
                        <tr><td>Lower:</td><td>{this.props.response.limitWarnings.lower}</td></tr>
                        <tr><td>Forward:</td><td>{this.props.response.limitWarnings.forward}</td></tr>
                        <tr><td>Property:</td><td>{this.props.response.limitWarnings.property}</td></tr>
                        <tr><td>Overload:</td><td>{this.props.response.limitWarnings.overload}</td></tr>

                        <tr><th colSpan='2'>Zero level:</th></tr>
                        <tr><td>Height from zero:</td><td>{this.props.response.height_from_zero}</td></tr>
                        <tr><td>Distance to zero:</td><td>{this.props.response.distance_to_zero}</td></tr>
                        <tr><td>Height to slope from zero:</td><td>{this.props.response.height_to_slope_from_zero}</td></tr>

                        <tr><th colSpan='2'>Euler angles:</th></tr>
                        <tr><td>Main boom:</td><td>{this.props.response.anglesEuler.boom}</td></tr>
                        <tr><td>Digging arm:</td><td>{this.props.response.anglesEuler.arm}</td></tr>
                        <tr><td>Bucket:</td><td>{this.props.response.anglesEuler.bucket}</td></tr>

                        <tr><th colSpan='2'>Quaternion angles:</th></tr>
                        <tr><td>Main boom:</td><td>{this.props.response.anglesQuaternion.boom}</td></tr>
                        <tr><td>Digging arm:</td><td>{this.props.response.anglesQuaternion.arm}</td></tr>
                        <tr><td>Bucket:</td><td>{this.props.response.anglesQuaternion.bucket}</td></tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

export default Telemetry;