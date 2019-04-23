import React from 'react';

class Visuals extends React.Component
{
    constructor(props) {
        super(props);

        let boomSin = Math.sin(40 * ( Math.PI / 180));
        let boomCos = Math.cos(40 * ( Math.PI / 180));

        let armSin = Math.sin(-60 * ( Math.PI / 180));
        let armCos = Math.cos(-60 * ( Math.PI / 180));

        let bucketSin = Math.sin(-150 * ( Math.PI / 180));
        let bucketCos = Math.cos(-150 * ( Math.PI / 180));

        this.state = {
            'boomSin': [boomSin, boomSin, boomSin, boomSin, boomSin, boomSin, boomSin, boomSin, boomSin, boomSin],
            'boomCos': [boomCos, boomCos, boomCos, boomCos, boomCos, boomCos, boomCos, boomCos, boomCos, boomCos],
            'armSin': [armSin, armSin, armSin, armSin, armSin, armSin, armSin, armSin, armSin, armSin],
            'armCos': [armCos, armCos, armCos, armCos, armCos, armCos, armCos, armCos, armCos, armCos],
            'bucketSin': [bucketSin, bucketSin, bucketSin, bucketSin, bucketSin, bucketSin, bucketSin, bucketSin, bucketSin, bucketSin],
            'bucketCos': [bucketCos, bucketCos, bucketCos, bucketCos, bucketCos, bucketCos, bucketCos, bucketCos, bucketCos, bucketCos]
        };
    }

    calculateX(aAngle, aLength) {
        let x = Math.floor(Math.fabs(Math.cos(Math.radians(aAngle)) * aLength))

        if (-90 <= aAngle && aAngle <= 90) {
            x = x * -1;
        }

        return x;
    }

    calculateY(aAngle, aLength) {
        let y = Math.floor(Math.fabs(Math.sin(Math.radians(aAngle)) * aLength))
    
        if (0 <= aAngle && aAngle <= 180) {
            y = y * -1;
        }

        return y;
    }

    calculateA(aSinList, aCosList) {
        const reducer = (accumulator, currentValue) => { return accumulator + currentValue; };

        let s = aSinList.reduce(reducer);
        let c = aCosList.reduce(reducer);
        let a = Math.atan2(s, c)
    
        return Math.round((a * 180 / Math.PI) * 10) / 10;
    }

    componentDidUpdate() {
        let boomSin = [...this.state.boomSin];
            boomSin.shift();
            boomSin.push(Math.sin(this.props.boomA * ( Math.PI / 180)));

        let boomCos = [...this.state.boomCos];
            boomCos.shift();
            boomCos.push(Math.cos(this.props.boomA * ( Math.PI / 180)));

        let armSin = [...this.state.armSin];
            armSin.shift();
            armSin.push(Math.sin(this.props.armA * ( Math.PI / 180)));

        let armCos = [...this.state.armCos];
            armCos.shift();
            armCos.push(Math.cos(this.props.armA * ( Math.PI / 180)));

        let bucketSin = [...this.state.bucketSin];
            bucketSin.shift();
            bucketSin.push(Math.sin(this.props.bucketA * ( Math.PI / 180)));

        let bucketCos = [...this.state.bucketCos];
            bucketCos.shift();
            bucketCos.push(Math.cos(this.props.bucketA * ( Math.PI / 180)));

        this.setState({
            'boomSin': boomSin,
            'boomCos': boomCos,
            'armSin': armSin,
            'armCos': armCos,
            'bucketSin': bucketSin,
            'bucketCos': bucketCos
        });
    }

    render() {
        let boomA = this.calculateA(this.state.boomSin, this.state.boomCos);
        let boomX = 900;
        let boomY = 900;
    
        let armA = this.calculateA(this.state.armSin, this.state.armCos);
        let armX = boomX + this.calculateX(boomA, 385);
        let armY = boomY + this.calculateY(boomA, 385);
    
        let bucketA = this.calculateA(this.state.bucketSin, this.state.bucketCos);
        let bucketX = armX + this.calculateX(armA, 176);
        let bucketY = armY + this.calculateY(armA, 176);

        let levelX = bucketX + this.calculateX(bucketA, 136) + this.props.distanceFromZero;
        let levelY = bucketY + this.calculateY(bucketA, 136) + this.props.heightFromZero;

        return (
            <svg
                width = '100%'
                height = '100%'
                xmlns = 'http://www.w3.org/2000/svg'
                xmlnsXlink = 'http://www.w3.org/1999/xlink'>

                <path
                    id = 'SVGBoom'
                    transform = {'rotate(' + boomA + ' 500 500) translate(' + (boomX - 500) + ' ' + (boomY - 500) + ')'}
                    d = 'M 112.06,494.03
                         C 103.19,500.92 112.00,509.11 117.94,505.97
                           124.83,502.34 121.78,491.03 112.06,494.03 Z
                         M 497.06,494.03
                         C 488.19,500.92 497.00,509.11 502.94,505.97
                           509.83,502.34 506.78,491.03 497.06,494.03 Z
                         M 489.09,540.64
                         C 464.07,530.87 359.66,490.66 334.33,480.33
                           318.73,474.36 310.36,474.18 297.33,477.67
                           277.33,483.39 144.78,520.45 119.91,526.82
                           104.64,529.00 92.18,519.36 88.91,507.00
                           86.18,494.91 90.55,481.45 104.27,475.27
                           119.54,469.05 252.88,412.90 300.64,392.45
                           319.18,384.27 336.82,385.36 352.52,392.57
                           402.57,415.75 497.60,453.01 518.64,462.27
                           536.18,470.09 548.09,494.36 539.00,516.67
                           530.82,535.55 509.00,546.91 489.09,540.64 Z' />

                <path
                    id = 'SVGArm'
                    transform = {'rotate(' + armA + ' 500 500) translate(' + (armX - 500) + ' ' + (armY - 500) + ')'}
                    d = 'M 321.45,518.18
                         C 333.98,519.14 486.24,526.30 498.17,527.00
                           511.56,527.44 517.50,521.62 521.43,516.74
                           528.87,507.22 561.57,463.31 568.55,454.00
                           574.75,444.81 567.50,431.50 552.00,435.09
                           528.91,439.98 346.42,476.83 324.00,481.27
                           312.39,483.96 306.00,488.43 305.75,500.00
                           305.83,509.30 311.35,516.70 321.45,518.18 Z
                         M 321.06,494.03
                         C 312.19,500.92 321.00,509.11 326.94,505.97
                           333.83,502.34 330.78,491.03 321.06,494.03 Z
                         M 497.06,494.03
                         C 488.19,500.92 497.00,509.11 502.94,505.97
                           509.83,502.34 506.78,491.03 497.06,494.03 Z' />

                <path
                    id = 'SVGBucket'
                    transform = {'rotate(' + bucketA + ' 500 500) translate(' + (bucketX - 500) + ' ' + (bucketY - 500) + ')'}
                    d = 'M 515.25,485.38
                         C 523.50,457.25 512.88,426.75 485.00,412.38
                           443.25,393.25 412.38,413.88 398.75,437.88
                           392.44,448.49 369.89,488.81 367.00,494.00
                           362.69,501.59 367.41,500.66 371.75,497.50
                           379.26,491.89 387.17,486.42 395.88,480.62
                           415.79,487.00 464.94,502.43 480.17,507.48
                           482.09,515.22 491.09,521.30 500.00,521.57
                           512.78,521.39 518.87,512.39 520.91,505.04
                           522.70,497.43 520.09,489.09 515.25,485.38 Z
                         M 497.06,494.03
                         C 488.19,500.92 497.00,509.11 502.94,505.97
                           509.83,502.34 506.78,491.03 497.06,494.03 Z' />

                <path
                    id = 'SVGLevel'
                    transform = {'rotate(' + this.props.levelA + ' 500 500) translate(' + (levelX - 500) + ' ' + (levelY - 500) + ')'}
                    d = 'M 0,1000 L 2000,1000 M 1000,980 L 1000,1020 Z' />

            </svg>
        );
    }
}

export default Visuals;