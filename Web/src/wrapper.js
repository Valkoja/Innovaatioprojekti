import React from 'react';
import Handler from './handler';

class Wrapper extends React.Component
{
    // constructor(props) {
    //     super(props);
    // }

    render() {
        return (
            <Handler ip={'10.0.0.184'} />
        );
    }
}

export default Wrapper;