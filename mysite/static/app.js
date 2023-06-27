const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");

const canvas_top = document.getElementById("canvas_top");
const ctx_top = canvas_top.getContext("2d");

const colors = document.getElementsByClassName("jsColor");
const range = document.getElementById("jsRange");
const mode = document.getElementById("jsMode");
const mode1 = document.getElementById("jsMode1");
const saveBtn = document.getElementById("jsSave")

const INITIAL_COLOR = "black";
const CANVAS_SIZE = 1210;

canvas.width = CANVAS_SIZE;
canvas.height = CANVAS_SIZE;

canvas_top.width = CANVAS_SIZE;
canvas_top.height = CANVAS_SIZE;


ctx.fillStyle = 'white';
//ctx.fillRect(0,0,CANVAS_SIZE,CANVAS_SIZE)

ctx.strokeStyle = 'black';
ctx.lineWidth = 2.5;
ctx.fillStyle = 'white';

ctx_top.fillStyle = 'white';
//ctx.fillRect(0,0,CANVAS_SIZE,CANVAS_SIZE)

ctx_top.strokeStyle = 'black';
ctx_top.lineWidth = 2.5;
ctx_top.fillStyle = 'white';




// (x, y, w, h) == (좌상단 x좌표, 좌상단 y좌표, 가로 길이, 세로 길이)
ctx.rect(10,10,110,110);
//ctx.fillRect(10,10,110,110)
ctx.rect(130,10,110,110); ctx.rect(250,10,110,110); ctx.rect(370,10,110,110); ctx.rect(490,10,110,110);
ctx.rect(610,10,110,110); ctx.rect(730,10,110,110); ctx.rect(850,10,110,110); ctx.rect(970,10,110,110); ctx.rect(1090,10,110,110);

ctx.rect(10,130,110,110); ctx.rect(130,130,110,110); ctx.rect(250,130,110,110); ctx.rect(370,130,110,110); ctx.rect(490,130,110,110);
ctx.rect(610,130,110,110); ctx.rect(730,130,110,110); ctx.rect(850,130,110,110); ctx.rect(970,130,110,110); ctx.rect(1090,130,110,110);

ctx.rect(10,250,110,110); ctx.rect(130,250,110,110); ctx.rect(250,250,110,110); ctx.rect(370,250,110,110); ctx.rect(490,250,110,110);
ctx.rect(610,250,110,110); ctx.rect(730,250,110,110); ctx.rect(850,250,110,110); ctx.rect(970,250,110,110); ctx.rect(1090,250,110,110);

ctx.rect(10,370,110,110); ctx.rect(130,370,110,110); ctx.rect(250,370,110,110); ctx.rect(370,370,110,110); ctx.rect(490,370,110,110);
ctx.rect(610,370,110,110); ctx.rect(730,370,110,110); ctx.rect(850,370,110,110); ctx.rect(970,370,110,110); ctx.rect(1090,370,110,110);

ctx.rect(10,490,110,110); ctx.rect(130,490,110,110); ctx.rect(250,490,110,110); ctx.rect(370,490,110,110); ctx.rect(490,490,110,110);
ctx.rect(610,490,110,110); ctx.rect(730,490,110,110); ctx.rect(850,490,110,110); ctx.rect(970,490,110,110); ctx.rect(1090,490,110,110);

ctx.rect(10,610,110,110); ctx.rect(130,610,110,110); ctx.rect(250,610,110,110); ctx.rect(370,610,110,110); ctx.rect(490,610,110,110);
ctx.rect(610,610,110,110); ctx.rect(730,610,110,110); ctx.rect(850,610,110,110); ctx.rect(970,610,110,110); ctx.rect(1090,610,110,110);

ctx.rect(10,730,110,110); ctx.rect(130,730,110,110); ctx.rect(250,730,110,110); ctx.rect(370,730,110,110); ctx.rect(490,730,110,110);
ctx.rect(610,730,110,110); ctx.rect(730,730,110,110); ctx.rect(850,730,110,110); ctx.rect(970,730,110,110); ctx.rect(1090,730,110,110);

ctx.rect(10,850,110,110); ctx.rect(130,850,110,110); ctx.rect(250,850,110,110); ctx.rect(370,850,110,110); ctx.rect(490,850,110,110);
ctx.rect(610,850,110,110); ctx.rect(730,850,110,110); ctx.rect(850,850,110,110); ctx.rect(970,850,110,110); ctx.rect(1090,850,110,110);

ctx.rect(10,970,110,110); ctx.rect(130,970,110,110); ctx.rect(250,970,110,110); ctx.rect(370,970,110,110); ctx.rect(490,970,110,110);
ctx.rect(610,970,110,110); ctx.rect(730,970,110,110); ctx.rect(850,970,110,110); ctx.rect(970,970,110,110); ctx.rect(1090,970,110,110);

ctx.rect(10,1090,110,110); ctx.rect(130,1090,110,110); ctx.rect(250,1090,110,110); ctx.rect(370,1090,110,110); ctx.rect(490,1090,110,110);
ctx.rect(610,1090,110,110); ctx.rect(730,1090,110,110); ctx.rect(850,1090,110,110); ctx.rect(970,1090,110,110); ctx.rect(1090,1090,110,110);



//ctx.rect(15,10,310,110);
ctx.stroke();
ctx.fill();
//ctx.Rect(0, 0, 150, 150)

//ctx.strokeStyle = "#2c2c2c";
ctx.strokeStyle = INITIAL_COLOR;
ctx.fillstyle = "white";
ctx.lineWidth = 2.5; /* 라인 굵기 */


ctx_top.rect(10,10,110,110);
//ctx_top.fillRect(10,10,110,110)
ctx_top.rect(130,10,110,110); ctx_top.rect(250,10,110,110); ctx_top.rect(370,10,110,110); ctx_top.rect(490,10,110,110);
ctx_top.rect(610,10,110,110); ctx_top.rect(730,10,110,110); ctx_top.rect(850,10,110,110); ctx_top.rect(970,10,110,110); ctx_top.rect(1090,10,110,110);

ctx_top.rect(10,130,110,110); ctx_top.rect(130,130,110,110); ctx_top.rect(250,130,110,110); ctx_top.rect(370,130,110,110); ctx_top.rect(490,130,110,110);
ctx_top.rect(610,130,110,110); ctx_top.rect(730,130,110,110); ctx_top.rect(850,130,110,110); ctx_top.rect(970,130,110,110); ctx_top.rect(1090,130,110,110);

ctx_top.rect(10,250,110,110); ctx_top.rect(130,250,110,110); ctx_top.rect(250,250,110,110); ctx_top.rect(370,250,110,110); ctx_top.rect(490,250,110,110);
ctx_top.rect(610,250,110,110); ctx_top.rect(730,250,110,110); ctx_top.rect(850,250,110,110); ctx_top.rect(970,250,110,110); ctx_top.rect(1090,250,110,110);

ctx_top.rect(10,370,110,110); ctx_top.rect(130,370,110,110); ctx_top.rect(250,370,110,110); ctx_top.rect(370,370,110,110); ctx_top.rect(490,370,110,110);
ctx_top.rect(610,370,110,110); ctx_top.rect(730,370,110,110); ctx_top.rect(850,370,110,110); ctx_top.rect(970,370,110,110); ctx_top.rect(1090,370,110,110);

ctx_top.rect(10,490,110,110); ctx_top.rect(130,490,110,110); ctx_top.rect(250,490,110,110); ctx_top.rect(370,490,110,110); ctx_top.rect(490,490,110,110);
ctx_top.rect(610,490,110,110); ctx_top.rect(730,490,110,110); ctx_top.rect(850,490,110,110); ctx_top.rect(970,490,110,110); ctx_top.rect(1090,490,110,110);

ctx_top.rect(10,610,110,110); ctx_top.rect(130,610,110,110); ctx_top.rect(250,610,110,110); ctx_top.rect(370,610,110,110); ctx_top.rect(490,610,110,110);
ctx_top.rect(610,610,110,110); ctx_top.rect(730,610,110,110); ctx_top.rect(850,610,110,110); ctx_top.rect(970,610,110,110); ctx_top.rect(1090,610,110,110);

ctx_top.rect(10,730,110,110); ctx_top.rect(130,730,110,110); ctx_top.rect(250,730,110,110); ctx_top.rect(370,730,110,110); ctx_top.rect(490,730,110,110);
ctx_top.rect(610,730,110,110); ctx_top.rect(730,730,110,110); ctx_top.rect(850,730,110,110); ctx_top.rect(970,730,110,110); ctx_top.rect(1090,730,110,110);

ctx_top.rect(10,850,110,110); ctx_top.rect(130,850,110,110); ctx_top.rect(250,850,110,110); ctx_top.rect(370,850,110,110); ctx_top.rect(490,850,110,110);
ctx_top.rect(610,850,110,110); ctx_top.rect(730,850,110,110); ctx_top.rect(850,850,110,110); ctx_top.rect(970,850,110,110); ctx_top.rect(1090,850,110,110);

ctx_top.rect(10,970,110,110); ctx_top.rect(130,970,110,110); ctx_top.rect(250,970,110,110); ctx_top.rect(370,970,110,110); ctx_top.rect(490,970,110,110);
ctx_top.rect(610,970,110,110); ctx_top.rect(730,970,110,110); ctx_top.rect(850,970,110,110); ctx_top.rect(970,970,110,110); ctx_top.rect(1090,970,110,110);

ctx_top.rect(10,1090,110,110); ctx_top.rect(130,1090,110,110); ctx_top.rect(250,1090,110,110); ctx_top.rect(370,1090,110,110); ctx_top.rect(490,1090,110,110);
ctx_top.rect(610,1090,110,110); ctx_top.rect(730,1090,110,110); ctx_top.rect(850,1090,110,110); ctx_top.rect(970,1090,110,110); ctx_top.rect(1090,1090,110,110);



ctx_top.stroke();
ctx_top.fill();
//ctx.Rect(0, 0, 150, 150)

//ctx.strokeStyle = "#2c2c2c";
ctx_top.strokeStyle = INITIAL_COLOR;
ctx_top.fillstyle = "white";
ctx_top.lineWidth = 2.5; /* 라인 굵기 */




let painting = false;
let filling = false;

function stopPainting() {
    painting = false;
}

function startPainting() {
    painting = true;
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if (!painting) {
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx_top.beginPath();
        ctx_top.moveTo(x, y);
    } else{
        ctx.lineTo(x, y);
        ctx.stroke();
        ctx_top.lineTo(x, y);
        ctx_top.stroke();
    }
}

function handleColorClick(event) {
    const color = event.target.style.backgroundColor;
    ctx.strokeStyle = color;
    ctx.fillStyle = color;
    ctx_top.strokeStyle = color;
    ctx_top.fillStyle = color;
}

function handleRangeChange(event){
    const size = event.target.value;
    ctx.lineWidth = size;
    ctx_top.lineWidth = size;
}

function handleModeClick(){
 if (filling == true){
    filling = false;
    mode.style.display = "none";
    mode1.style.display = "block";
 }else{
 filling = true;
 mode1.style.display = "none";
 mode.style.display = "block";
 }
}

function handleCanvasClick(event){
        fillRect(event);
        const x = event.offsetX;
        const y = event.offsetY;
        if (filling){
        if (x < 120 && y < 120){ctx.fillRect(10,10,110,110); ctx_top.fillRect(10,10,110,110);}
        else if (x < 240 && y < 120){ctx.fillRect(130,10,110,110); ctx_top.fillRect(130,10,110,110);}
        else if (x < 360 && y < 120){ctx.fillRect(250,10,110,110); ctx_top.fillRect(250,10,110,110);}
        else if (x < 480 && y < 120){ctx.fillRect(370,10,110,110); ctx_top.fillRect(370,10,110,110);}
        else if (x < 600 && y < 120){ctx.fillRect(490,10,110,110); ctx_top.fillRect(490,10,110,110);}
        else if (x < 720 && y < 120){ctx.fillRect(610,10,110,110); ctx_top.fillRect(610,10,110,110);}
        else if (x < 840 && y < 120){ctx.fillRect(730,10,110,110); ctx_top.fillRect(730,10,110,110);}
        else if (x < 960 && y < 120){ctx.fillRect(850,10,110,110); ctx_top.fillRect(850,10,110,110);}
        else if (x < 1080 && y < 120){ctx.fillRect(970,10,110,110); ctx_top.fillRect(970,10,110,110);}
        else if (x < 1200 && y < 120){ctx.fillRect(1090,10,110,110); ctx_top.fillRect(1090,10,110,110);}

        if (y > 120){
        if (x < 120 && y < 240){ctx.fillRect(10,130,110,110); ctx_top.fillRect(10,130,110,110);}
        else if (x < 240 && y < 240){ctx.fillRect(130,130,110,110); ctx_top.fillRect(130,130,110,110);}
        else if (x < 360 && y < 240){ctx.fillRect(250,130,110,110); ctx_top.fillRect(250,130,110,110);}
        else if (x < 480 && y < 240){ctx.fillRect(370,130,110,110); ctx_top.fillRect(370,130,110,110);}
        else if (x < 600 && y < 240){ctx.fillRect(490,130,110,110); ctx_top.fillRect(490,130,110,110);}
        else if (x < 720 && y < 240){ctx.fillRect(610,130,110,110); ctx_top.fillRect(610,130,110,110);}
        else if (x < 840 && y < 240){ctx.fillRect(730,130,110,110); ctx_top.fillRect(730,130,110,110);}
        else if (x < 960 && y < 240){ctx.fillRect(850,130,110,110); ctx_top.fillRect(850,130,110,110);}
        else if (x < 1080 && y < 240){ctx.fillRect(970,130,110,110); ctx_top.fillRect(970,130,110,110);}
        else if (x < 1200 && y < 240){ctx.fillRect(1090,130,110,110); ctx_top.fillRect(1090,130,110,110);}
        }
        if (y > 240){
        if (x < 120 && y < 360){ctx.fillRect(10,250,110,110); ctx_top.fillRect(10,250,110,110);}
        else if (x < 240 && y < 360){ctx.fillRect(130,250,110,110); ctx_top.fillRect(130,250,110,110);}
        else if (x < 360 && y < 360){ctx.fillRect(250,250,110,110); ctx_top.fillRect(250,250,110,110);}
        else if (x < 480 && y < 360){ctx.fillRect(370,250,110,110); ctx_top.fillRect(370,250,110,110);}
        else if (x < 600 && y < 360){ctx.fillRect(490,250,110,110); ctx_top.fillRect(490,250,110,110);}
        else if (x < 720 && y < 360){ctx.fillRect(610,250,110,110); ctx_top.fillRect(610,250,110,110);}
        else if (x < 840 && y < 360){ctx.fillRect(730,250,110,110); ctx_top.fillRect(730,250,110,110);}
        else if (x < 960 && y < 360){ctx.fillRect(850,250,110,110); ctx_top.fillRect(850,250,110,110);}
        else if (x < 1080 && y < 360){ctx.fillRect(970,250,110,110); ctx_top.fillRect(970,250,110,110);}
        else if (x < 1200 && y < 360){ctx.fillRect(1090,250,110,110); ctx_top.fillRect(1090,250,110,110);}
        }
        if (y > 360){
        if (x < 120 && y < 480){ctx.fillRect(10,370,110,110); ctx_top.fillRect(10,370,110,110);}
        else if (x < 240 && y < 480){ctx.fillRect(130,370,110,110); ctx_top.fillRect(130,370,110,110);}
        else if (x < 360 && y < 480){ctx.fillRect(250,370,110,110); ctx_top.fillRect(250,370,110,110);}
        else if (x < 480 && y < 480){ctx.fillRect(370,370,110,110); ctx_top.fillRect(370,370,110,110);}
        else if (x < 600 && y < 480){ctx.fillRect(490,370,110,110); ctx_top.fillRect(490,370,110,110);}
        else if (x < 720 && y < 480){ctx.fillRect(610,370,110,110); ctx_top.fillRect(610,370,110,110);}
        else if (x < 840 && y < 480){ctx.fillRect(730,370,110,110); ctx_top.fillRect(730,370,110,110);}
        else if (x < 960 && y < 480){ctx.fillRect(850,370,110,110); ctx_top.fillRect(850,370,110,110);}
        else if (x < 1080 && y < 480){ctx.fillRect(970,370,110,110); ctx_top.fillRect(970,370,110,110);}
        else if (x < 1200 && y < 480){ctx.fillRect(1090,370,110,110); ctx_top.fillRect(1090,370,110,110);}
        }
        if (y > 480){
        if (x < 120 && y < 600){ctx.fillRect(10,490,110,110); ctx_top.fillRect(10,490,110,110);}
        else if (x < 240 && y < 600){ctx.fillRect(130,490,110,110); ctx_top.fillRect(130,490,110,110);}
        else if (x < 360 && y < 600){ctx.fillRect(250,490,110,110); ctx_top.fillRect(250,490,110,110);}
        else if (x < 480 && y < 600){ctx.fillRect(370,490,110,110); ctx_top.fillRect(370,490,110,110);}
        else if (x < 600 && y < 600){ctx.fillRect(490,490,110,110); ctx_top.fillRect(490,490,110,110);}
        else if (x < 720 && y < 600){ctx.fillRect(610,490,110,110); ctx_top.fillRect(610,490,110,110);}
        else if (x < 840 && y < 600){ctx.fillRect(730,490,110,110); ctx_top.fillRect(730,490,110,110);}
        else if (x < 960 && y < 600){ctx.fillRect(850,490,110,110); ctx_top.fillRect(850,490,110,110);}
        else if (x < 1080 && y < 600){ctx.fillRect(970,490,110,110); ctx_top.fillRect(970,490,110,110);}
        else if (x < 1200 && y < 600){ctx.fillRect(1090,490,110,110); ctx_top.fillRect(1090,490,110,110);}
        }
        if (y > 600){
        if (x < 120 && y < 720){ctx.fillRect(10,610,110,110); ctx_top.fillRect(10,610,110,110);}
        else if (x < 240 && y < 720){ctx.fillRect(130,610,110,110); ctx_top.fillRect(130,610,110,110);}
        else if (x < 360 && y < 720){ctx.fillRect(250,610,110,110); ctx_top.fillRect(250,610,110,110);}
        else if (x < 480 && y < 720){ctx.fillRect(370,610,110,110); ctx_top.fillRect(370,610,110,110);}
        else if (x < 600 && y < 720){ctx.fillRect(490,610,110,110); ctx_top.fillRect(490,610,110,110);}
        else if (x < 720 && y < 720){ctx.fillRect(610,610,110,110); ctx_top.fillRect(610,610,110,110);}
        else if (x < 840 && y < 720){ctx.fillRect(730,610,110,110); ctx_top.fillRect(730,610,110,110);}
        else if (x < 960 && y < 720){ctx.fillRect(850,610,110,110); ctx_top.fillRect(850,610,110,110);}
        else if (x < 1080 && y < 720){ctx.fillRect(970,610,110,110); ctx_top.fillRect(970,610,110,110);}
        else if (x < 1200 && y < 720){ctx.fillRect(1090,610,110,110); ctx_top.fillRect(1090,610,110,110);}
        }
        if (y > 720){
        if (x < 120 && y < 840){ctx.fillRect(10,730,110,110); ctx_top.fillRect(10,730,110,110);}
        else if (x < 240 && y < 840){ctx.fillRect(130,730,110,110); ctx_top.fillRect(130,730,110,110);}
        else if (x < 360 && y < 840){ctx.fillRect(250,730,110,110); ctx_top.fillRect(250,730,110,110);}
        else if (x < 480 && y < 840){ctx.fillRect(370,730,110,110); ctx_top.fillRect(370,730,110,110);}
        else if (x < 600 && y < 840){ctx.fillRect(490,730,110,110); ctx_top.fillRect(490,730,110,110);}
        else if (x < 720 && y < 840){ctx.fillRect(610,730,110,110); ctx_top.fillRect(610,730,110,110);}
        else if (x < 840 && y < 840){ctx.fillRect(730,730,110,110); ctx_top.fillRect(730,730,110,110);}
        else if (x < 960 && y < 840){ctx.fillRect(850,730,110,110); ctx_top.fillRect(850,730,110,110);}
        else if (x < 1080 && y < 840){ctx.fillRect(970,730,110,110); ctx_top.fillRect(970,730,110,110);}
        else if (x < 1200 && y < 840){ctx.fillRect(1090,730,110,110); ctx_top.fillRect(1090,730,110,110);}
        }
        if (y > 840){
        if (x < 120 && y < 960){ctx.fillRect(10,850,110,110); ctx_top.fillRect(10,850,110,110);}
        else if (x < 240 && y < 960){ctx.fillRect(130,850,110,110); ctx_top.fillRect(130,850,110,110);}
        else if (x < 360 && y < 960){ctx.fillRect(250,850,110,110); ctx_top.fillRect(250,850,110,110);}
        else if (x < 480 && y < 960){ctx.fillRect(370,850,110,110); ctx_top.fillRect(370,850,110,110);}
        else if (x < 600 && y < 960){ctx.fillRect(490,850,110,110); ctx_top.fillRect(490,850,110,110);}
        else if (x < 720 && y < 960){ctx.fillRect(610,850,110,110); ctx_top.fillRect(610,850,110,110);}
        else if (x < 840 && y < 960){ctx.fillRect(730,850,110,110); ctx_top.fillRect(730,850,110,110);}
        else if (x < 960 && y < 960){ctx.fillRect(850,850,110,110); ctx_top.fillRect(850,850,110,110);}
        else if (x < 1080 && y < 960){ctx.fillRect(970,850,110,110); ctx_top.fillRect(970,850,110,110);}
        else if (x < 1200 && y < 960){ctx.fillRect(1090,850,110,110); ctx_top.fillRect(1090,850,110,110);}
        }
        if (y > 960){
        if (x < 120 && y < 1080){ctx.fillRect(10,970,110,110); ctx_top.fillRect(10,970,110,110);}
        else if (x < 240 && y < 1080){ctx.fillRect(130,970,110,110); ctx_top.fillRect(130,970,110,110);}
        else if (x < 360 && y < 1080){ctx.fillRect(250,970,110,110); ctx_top.fillRect(250,970,110,110);}
        else if (x < 480 && y < 1080){ctx.fillRect(370,970,110,110); ctx_top.fillRect(370,970,110,110);}
        else if (x < 600 && y < 1080){ctx.fillRect(490,970,110,110); ctx_top.fillRect(490,970,110,110);}
        else if (x < 720 && y < 1080){ctx.fillRect(610,970,110,110); ctx_top.fillRect(610,970,110,110);}
        else if (x < 840 && y < 1080){ctx.fillRect(730,970,110,110); ctx_top.fillRect(730,970,110,110);}
        else if (x < 960 && y < 1080){ctx.fillRect(850,970,110,110); ctx_top.fillRect(850,970,110,110);}
        else if (x < 1080 && y < 1080){ctx.fillRect(970,970,110,110); ctx_top.fillRect(970,970,110,110);}
        else if (x < 1200 && y < 1080){ctx.fillRect(1090,970,110,110); ctx_top.fillRect(1090,970,110,110);}
        }
        if (y > 1080){
        if (x < 120 && y < 1200){ctx.fillRect(10,1090,110,110); ctx_top.fillRect(10,1090,110,110);}
        else if (x < 240 && y < 1200){ctx.fillRect(130,1090,110,110); ctx_top.fillRect(130,1090,110,110);}
        else if (x < 360 && y < 1200){ctx.fillRect(250,1090,110,110); ctx_top.fillRect(250,1090,110,110);}
        else if (x < 480 && y < 1200){ctx.fillRect(370,1090,110,110); ctx_top.fillRect(370,1090,110,110);}
        else if (x < 600 && y < 1200){ctx.fillRect(490,1090,110,110); ctx_top.fillRect(490,1090,110,110);}
        else if (x < 720 && y < 1200){ctx.fillRect(610,1090,110,110); ctx_top.fillRect(610,1090,110,110);}
        else if (x < 840 && y < 1200){ctx.fillRect(730,1090,110,110); ctx_top.fillRect(730,1090,110,110);}
        else if (x < 960 && y < 1200){ctx.fillRect(850,1090,110,110); ctx_top.fillRect(850,1090,110,110);}
        else if (x < 1080 && y < 1200){ctx.fillRect(970,1090,110,110); ctx_top.fillRect(970,1090,110,110);}
        else if (x < 1200 && y < 1200){ctx.fillRect(1090,1090,110,110); ctx_top.fillRect(1090,1090,110,110);}
        }
        }
}


//손글씨 원본 캔버스 / 아래장
function handleSaveClick(){
    const image = canvas.toDataURL("image/jfif",1.0);
    const link = document.createElement("a");
    link.href = image;
    link.download = "0";
    link.click();
}

// 텍스트 전환 / 윗장
function handleSaveClick_top(){
    const image_top = canvas_top.toDataURL("image/jfif",1.0);
    const link = document.createElement("a");
    link.href = image_top;
    link.download = "5";
    link.click();
}

function fillRect(event){
    const x = event.offsetX;
    const y = event.offsetY;
}

if (canvas_top) {
    canvas_top.addEventListener("mousemove", onMouseMove);
    canvas_top.addEventListener("mousedown", startPainting);
    canvas_top.addEventListener("mouseup", stopPainting);
    canvas_top.addEventListener("mouseleave", stopPainting);
    canvas_top.addEventListener("click", handleCanvasClick);
}

Array.from(colors).forEach(color =>
    color.addEventListener("click", handleColorClick));

if(range){
    range.addEventListener("input", handleRangeChange)
}
if(mode){
    mode.addEventListener("click", handleModeClick);
}
if(mode1){
    mode1.addEventListener("click", handleColorClick);
    mode1.addEventListener("click", handleModeClick);
}
if(saveBtn){
    saveBtn.addEventListener("click", handleSaveClick)
    saveBtn.addEventListener("click", handleSaveClick_top)
}