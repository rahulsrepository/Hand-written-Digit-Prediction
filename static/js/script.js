const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
const predictBtn = document.getElementById('predict');
const clearBtn = document.getElementById('clear');
const result = document.getElementById('result');
const fileUpload = document.getElementById('fileUpload');
const modeRadios = document.getElementsByName('mode');

ctx.fillStyle = 'black';
ctx.fillRect(0, 0, canvas.width, canvas.height);

let isDrawing = false;

canvas.addEventListener('mousedown', startDrawing);
canvas.addEventListener('mousemove', draw);
canvas.addEventListener('mouseup', stopDrawing);
canvas.addEventListener('mouseout', stopDrawing);

function startDrawing(e) {
    isDrawing = true;
    draw(e);
}

function draw(e) {
    if (!isDrawing) return;
    ctx.strokeStyle = 'white';
    ctx.lineWidth = 20;
    ctx.lineCap = 'round';
    ctx.lineTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
    ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(e.clientX - canvas.offsetLeft, e.clientY - canvas.offsetTop);
}

function stopDrawing() {
    isDrawing = false;
    ctx.beginPath();
}

clearBtn.addEventListener('click', () => {
    ctx.fillStyle = 'black';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    result.textContent = 'Predicted Digit: ';
});

predictBtn.addEventListener('click', async () => {
    const imageData = canvas.toDataURL('image/png');
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ image: imageData }),
        });
        const data = await response.json();
        result.textContent = `Predicted Digit: ${data.prediction}`;
    } catch (error) {
        console.error('Error:', error);
        result.textContent = 'Error: Could not predict digit';
    }
});

modeRadios.forEach(radio => {
    radio.addEventListener('change', (e) => {
        if (e.target.value === 'draw') {
            canvas.style.display = 'block';
            fileUpload.style.display = 'none';
        } else {
            canvas.style.display = 'none';
            fileUpload.style.display = 'block';
        }
    });
});

fileUpload.addEventListener('change', (e) => {
    const file = e.target.files[0];
    const reader = new FileReader();
    reader.onload = function(event) {
        const img = new Image();
        img.onload = function() {
            ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
        }
        img.src = event.target.result;
    }
    reader.readAsDataURL(file);
    canvas.style.display = 'block';
});