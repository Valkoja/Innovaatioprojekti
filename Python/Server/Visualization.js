function calculateX(angle, length) {
    var x = Math.floor(Math.abs(Math.cos(angle * Math.PI / 180) * length))

    if (angle >= -90 && angle <= 90) {
        return x * -1;
    }
    
    return x;
}

function calculateY(angle, length) {
    var y = Math.floor(Math.abs(Math.sin(angle * Math.PI / 180) * length));
    
    if (angle >= 0 && angle <= 180) {
        return y * -1;
    }
    
    return y;
}

function updateCanvas() {
    var angleA = modelWrapper.mainBoomAngle;
    var angleB = modelWrapper.diggingArmAngle;
    var angleC = modelWrapper.bucketAngle;

    // Kontekstiolio, viivanleveys, nollataan tilanne
    var context = visualizationCanvas.getContext('2d');
        context.lineWidth = 2;
        context.reset();

    // Alkupiste oikealle alas
    var p1 = {'x': 550, 'y': 475};

    context.beginPath();
    context.moveTo(p1.x, p1.y);

    // Puomi
    var p2 = {'x': p1.x + calculateX(angleA, 385), 'y': p1.y + calculateY(angleA, 385)};

    context.strokeStyle = '#ff0000';
    context.lineTo(p2.x, p2.y);

    // Toinen puomi
    var p3 = {'x': p2.x + calculateX(angleA + angleB, 176), 'y': p2.y + calculateY(angleA + angleB, 176)};

    context.strokeStyle = '#00ff00';
    context.lineTo(p3.x, p3.y);

    // Kauha
    var p4 = {'x': p3.x + calculateX(angleA + angleB + angleC, 133), 'y': p3.y + calculateY(angleA + angleB + angleC, 133)};

    context.strokeStyle = '#0000ff';
    context.lineTo(p4.x, p4.y);
    context.stroke();
}