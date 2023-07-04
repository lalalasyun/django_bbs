$('#trim_div').on('mousedown', function(e) {
    const clientWidth = $('.trim_image img')[0].clientWidth;
    const clientHeight = $('.trim_image img')[0].clientHeight
    const initX = e.pageX;
    const initY = e.pageY;
    const transformValue = getTransFormValue();
    $('html').mousemove(function (e){
        const nowTransformValue = getTransFormValue();
        const moveX =  - (initX - e.pageX);
        const moveY =  - (initY - e.pageY);
        let setX = transformValue.x;
        let setY = transformValue.y;
        
        if (-(clientWidth - 400) < setX + moveX && setX + moveX < 1) {
            setX += moveX;
        } else {
            setX = nowTransformValue.x;
        }
        if (-(clientHeight - 400) < setY + moveY && setY + moveY < 1) {
            setY += moveY;
        } else {
            setY = nowTransformValue.y;
        }
        setTransFormValue(setX, setY);
    })
    $('html').on('mouseup', function() {
        $('html').off('mousemove');
    });
});

function getTransFormValue() {
    const split = $('.trim_image img').css('transform').split(/[(,)]/);
    return {
        x: Number(split[5]),
        y: Number(split[6])
    }
}

function setTransFormValue(x, y) {
    $('.trim_image img').css('transform','translate3d(' + x + 'px, ' + y + 'px, 0px)');
    $("#trim_form #id_position_x").val(x);
    $("#trim_form #id_position_y").val(y);
}

function changeTransFormValue( x, y ) {
    const startX = - ($('.trim_image img')[0].clientWidth - 400)
    const startY = - ($('.trim_image img')[0].clientHeight - 400);
    return {
        x: startX > x ? startX : x > 0 ? 0 : x,
        y: startY > y ? startY : y > 0 ? 0 : y
    }
}

function setZoomValue( value ) {
    const zoom = (value / 100) + 1;
    $('.trim_image img').css('height',400 * zoom + "px");
    $("#trim_form #id_zoom").val(value);

    let transformValue = getTransFormValue();
    transformValue = changeTransFormValue(transformValue.x, transformValue.y)
    setTransFormValue(transformValue.x, transformValue.y);
}

$('#range').on('input', function() {
    setZoomValue($('#range').val());
});

function getZoom() {
    const zoom = ($('#range').val() / 100) + 1;
    return zoom;
}

setTransFormValue(0, 0);