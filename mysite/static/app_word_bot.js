const canvas_bot = document.getElementById("canvas_bot");
const ctx_bot = canvas_bot.getContext("2d");

const colors_bot = document.getElementsByClassName("jsColor");
const range_bot = document.getElementById("jsRange");
const mode_bot = document.getElementById("jsMode");
const mode1_bot = document.getElementById("jsMode1");
const saveBtn_bot = document.getElementById("jsSave")
const reloadX_bot = document.getElementById("jsReloadX")

const INITIAL_COLOR_bot = "black";
const CANVAS_SIZE_bot = 1010;



//canvas.width = CANVAS_SIZE;
//canvas.height = 330;

canvas_bot.width = CANVAS_SIZE_bot;
canvas_bot.height = 260;


//ctx.fillStyle = 'white';

//ctx.drawImage(img, 100, 100);
//ctx.fillRect(0,0,CANVAS_SIZE,CANVAS_SIZE)

//ctx.strokeStyle = 'black';
//ctx.lineWidth = 8;
//ctx.fillStyle = 'white';

ctx_bot.fillStyle = 'white';
//ctx.fillRect(0,0,CANVAS_SIZE,CANVAS_SIZE)

ctx_bot.strokeStyle = 'black';
ctx_bot.lineWidth = 8;
ctx_bot.fillStyle = 'white';




//// (x, y, w, h) == (좌상단 x좌표, 좌상단 y좌표, 가로 길이, 세로 길이)
//ctx.rect(10,10,310,310);
////ctx.fillRect(10,10,110,110)
//ctx.rect(330,10,310,310); ctx.rect(650,10,310,310);
//
//
//
//
//ctx.stroke();
//ctx.fill();
//
////ctx.strokeStyle = "#2c2c2c";
//ctx.strokeStyle = INITIAL_COLOR;
//ctx.fillstyle = "white";
//ctx.lineWidth = 10; /* 라인 굵기 */


ctx_bot.rect(10,10,240,240);
//ctx.fillRect(10,10,110,110)
ctx_bot.rect(260,10,240,240);
ctx_bot.rect(510,10,240,240);
ctx_bot.rect(760,10,240,240);


ctx_bot.stroke();
ctx_bot.fill();
//ctx.Rect(0, 0, 150, 150)

//ctx.strokeStyle = "#2c2c2c";
ctx_bot.strokeStyle = INITIAL_COLOR_bot;
ctx_bot.fillstyle = "white";
ctx_bot.lineWidth = 10; /* 라인 굵기 */




let painting_bot = false;
let filling_bot = false;

function stopPainting() {
    painting_bot = false;
}

function startPainting() {
    painting_bot = true;
}

function onMouseMove(event) {
    const x = event.offsetX;
    const y = event.offsetY;
    if (!painting_bot) {
//        ctx.beginPath();
//        ctx.moveTo(x, y);
        ctx_bot.beginPath();
        ctx_bot.moveTo(x, y);
    } else{
//        ctx.lineTo(x, y);
//        ctx.stroke();
        ctx_bot.lineTo(x, y);
        ctx_bot.stroke();
    }
}

function handleColorClick(event) {
    const color = event.target.style.backgroundColor;
//    ctx.strokeStyle = color;
//    ctx.fillStyle = color;
    ctx_bot.strokeStyle = color;
    ctx_bot.fillStyle = color;
}

function handleRangeChange(event){
    const size = event.target.value;
//    ctx.lineWidth = size;
    ctx_bot.lineWidth = size;
}

function handleModeClick(){
 if (filling_bot == true){
    filling_bot = false;
    mode_bot.style.display = "none";
    mode1_bot.style.display = "block";
 }else{
 filling_bot = true;
 mode1_bot.style.display = "none";
 mode_bot.style.display = "block";
 }
}

function handleCanvasClick(event){
        fillRect(event);
        const x = event.offsetX;
        const y = event.offsetY;
        if (filling_bot){
        if (x < 255 && y < 255){ctx_bot.fillRect(10,10,240,240);}
        else if (x < 505 && y < 505){ctx_bot.fillRect(260,10,240,240);}
        else if (x < 755 && y < 755){ctx_bot.fillRect(510,10,240,240);}
        else if (x < 1010 && y < 1010){ctx_bot.fillRect(760,10,240,240);}
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
    const image_top = canvas_bot.toDataURL("image/jfif",1.0);
    const link = document.createElement("a");
    link.href = image_top;
    link.download = "5";
    link.click();
}

function fillRect(event){
    const x = event.offsetX;
    const y = event.offsetY;
}

if (canvas_bot) {
    canvas_bot.addEventListener("mousemove", onMouseMove);
    canvas_bot.addEventListener("mousedown", startPainting);
    canvas_bot.addEventListener("mouseup", stopPainting);
    canvas_bot.addEventListener("mouseleave", stopPainting);
    canvas_bot.addEventListener("click", handleCanvasClick);
}

Array.from(colors_bot).forEach(color =>
    color.addEventListener("click", handleColorClick));

if(range_bot){
    range_bot.addEventListener("input", handleRangeChange)
}
if(mode_bot){
    mode_bot.addEventListener("click", handleModeClick);
}
if(mode1_bot){
    mode1_bot.addEventListener("click", handleColorClick);
    mode1_bot.addEventListener("click", handleModeClick);
}
if(saveBtn_bot){
    saveBtn_bot.addEventListener("click", handleSaveClick)
    saveBtn_bot.addEventListener("click", handleSaveClick_top)
}

if(reloadX_bot){
    reloadX_bot.addEventListener("click", setBackground)
//    reloadX.addEventListener("click", handleAnalysisClick2)
}

//function handleAnalysisClick(event){
//    alert('hi');
//}

//function handleAnalysisClick2(){
//    const image = canvas.toDataURL("image/jfif",1.0);
//    const link = document.createElement("a");
//    link.href = image;
//    link.download = "0";
//    link.click();
//}

//const form = document.getElementById('reloadX');
//
//form.addEventListener('submit', function (e) {
//    e.preventDefault();
//    console.log('submit');
//});

//const img = new Image();
//img.src = 'C:/projects/second_3/project/static/back.png';
//img.onload=function(){
//	//canvas에 그리기 .drawImage(이미지, x, y, width, height)
//	ctx.drawImage(img, 200,200,100,100);
//};


function setBackground(){
    var image = new Image();
    image.onload = function() {
    ctx.drawImage(image, 0, 0, CANVAS_SIZE_bot, CANVAS_SIZE_bot);
    }
    image.src = "../static/image_0.png";
    alert('hi');
}