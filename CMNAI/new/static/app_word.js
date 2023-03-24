const canvas = document.getElementById("jsCanvas");
const ctx = canvas.getContext("2d");

const canvas_top = document.getElementById("canvas_top");
const ctx_top = canvas_top.getContext("2d");

const colors = document.getElementsByClassName("jsColor");
const range = document.getElementById("jsRange");
const mode = document.getElementById("jsMode");
const mode1 = document.getElementById("jsMode1");
const saveBtn = document.getElementById("jsSave")
const reloadX = document.getElementById("jsReloadX")

const INITIAL_COLOR = "black";
const CANVAS_SIZE = 970;



canvas.width = CANVAS_SIZE;
canvas.height = 330;

canvas_top.width = CANVAS_SIZE;
canvas_top.height = 330;


ctx.fillStyle = 'white';

//ctx.drawImage(img, 100, 100);
//ctx.fillRect(0,0,CANVAS_SIZE,CANVAS_SIZE)

ctx.strokeStyle = 'black';
ctx.lineWidth = 8;
ctx.fillStyle = 'white';

ctx_top.fillStyle = 'white';
//ctx.fillRect(0,0,CANVAS_SIZE,CANVAS_SIZE)

ctx_top.strokeStyle = 'black';
ctx_top.lineWidth = 8;
ctx_top.fillStyle = 'white';




// (x, y, w, h) == (좌상단 x좌표, 좌상단 y좌표, 가로 길이, 세로 길이)
ctx.rect(10,10,310,310);
//ctx.fillRect(10,10,110,110)
ctx.rect(330,10,310,310); ctx.rect(650,10,310,310);




ctx.stroke();
ctx.fill();

//ctx.strokeStyle = "#2c2c2c";
ctx.strokeStyle = INITIAL_COLOR;
ctx.fillstyle = "white";
ctx.lineWidth = 10; /* 라인 굵기 */


ctx_top.rect(10,10,310,310);
//ctx.fillRect(10,10,110,110)
ctx_top.rect(330,10,310,310); ctx_top.rect(650,10,310,310);


ctx_top.stroke();
ctx_top.fill();
//ctx.Rect(0, 0, 150, 150)

//ctx.strokeStyle = "#2c2c2c";
ctx_top.strokeStyle = INITIAL_COLOR;
ctx_top.fillstyle = "white";
ctx_top.lineWidth = 10; /* 라인 굵기 */




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
    mode.innerText = "Fill";
    mode1.innerText = "Fill";
    mode.style.display = "none";
    mode1.style.display = "block";
 }else{
 filling = true;
 mode.innerText = "Paint";
 mode1.innerText = "Paint";
 mode1.style.display = "none";
 mode.style.display = "block";
 }
}

function handleCanvasClick(event){
        fillRect(event);
        const x = event.offsetX;
        const y = event.offsetY;
        if (filling){
        if (x < 320 && y < 320){ctx.fillRect(10,10,310,310); ctx_top.fillRect(10,10,310,310);}
        else if (x < 640 && y < 640){ctx.fillRect(330,10,310,310); ctx_top.fillRect(330,10,310,310);}
        else if (x < 970 && y < 970){ctx.fillRect(650,10,310,310); ctx_top.fillRect(650,10,310,310);}
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

if(reloadX){
    reloadX.addEventListener("click", setBackground)
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
    ctx.drawImage(image, 0, 0, CANVAS_SIZE, CANVAS_SIZE);
    }
    image.src = "../static/image_0.png";
    alert('hi');
}