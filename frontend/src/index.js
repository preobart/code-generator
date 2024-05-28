const URL = 'http://127.0.0.1:5000';

const $button = document.querySelector('#button');
const $textarea = document.getElementById('inputText');
const $typeOption = document.getElementById('barcodeType');
const $errorCorrectionLevelOption = document.getElementById('errorCorrectionLevel');
const $sizeOption = document.getElementById('barcodeSize');
const $colorOption = document.getElementById('barcodeColor');

$button.onclick = async () => {
    if (typeof $textarea.value === 'undefined' || $textarea.value.length === 0) {
        return;
    }

    if ($typeOption.value === 'qr-code') {
        const body = {
            text: $textarea.value,
            level: $errorCorrectionLevelOption.value
        };

        try {
            const response = await fetch(`${URL}/qrcode`, {
                method: 'POST',
                body: JSON.stringify(body)
            });
    
            const data = await response.json();

            drawQRCode(data, $colorOption.value);
        } catch (error) {
            toastr.error("Что-то пошло не так! Проверьте данные!");
        }

        
    } else {
        const body = {
            text: $textarea.value,
            type: $typeOption.value
        };

        try {
            const response = await fetch(`${URL}/barcode`, {
                method: 'POST',
                body: JSON.stringify(body)
            });
    
            const data = await response.text();
    
            drawBarcode(data, $colorOption.value);
        } catch (error) {
            toastr.error("Что-то пошло не так! Проверьте данные!");
        }
    }
};

$sizeOption.onchange = handleSize;

function handleSize() {
    const barcodeType = document.getElementById('barcodeType').value;
    const barcodeSize = document.getElementById('barcodeSize').value;
    const canvas = document.getElementById('barcodeCanvas');

    if (barcodeType === 'qr-code') {
        if (barcodeSize === 'small') {
            canvas.width = 400;
            canvas.height = 400;
        } else if (barcodeSize === 'medium') {
            canvas.width = 500;
            canvas.height = 500;
        } else {
            canvas.width = 600;
            canvas.height = 600;
        }
    } else {
        if (barcodeSize === 'small') {
            canvas.width = 400;
            canvas.height = 200;
        } else if (barcodeSize === 'medium') {
            canvas.width = 500;
            canvas.height = 250;
        } else {
            canvas.width = 600;
            canvas.height = 300;
        }
    }
}

$typeOption.onchange = () => {
    handleSize();

    const barcodeType = document.getElementById('barcodeType').value;
    const errorCorrectionLevel = document.getElementById('errorCorrectionLevel');

    if (barcodeType === 'qr-code') {
        errorCorrectionLevel.style.display = 'block';
    } else {
        errorCorrectionLevel.style.display = 'none';
    }
};

// Функция для рисования QR-кода
function drawQRCode(matrix, color) {
    const canvas = document.getElementById('barcodeCanvas');
    const ctx = canvas.getContext('2d');

    const canvasSize = Math.min(canvas.width, canvas.height); // Выбираем размер канваса
    const cellSize = Math.floor(canvasSize / matrix.length); // Рассчитываем размер одной ячейки

    // Устанавливаем подходящий размер канваса
    canvas.width = canvasSize;
    canvas.height = canvasSize;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    const offsetX = Math.floor((canvas.width - cellSize * matrix.length) / 2);
    const offsetY = Math.floor((canvas.height - cellSize * matrix.length) / 2);

    for (let row = 0; row < matrix.length; row++) {
        for (let col = 0; col < matrix[row].length; col++) {
            ctx.fillStyle = matrix[row][col] ? color : '#ffffff';
            ctx.fillRect(offsetX + col * cellSize, offsetY + row * cellSize, cellSize, cellSize);
        }
    }
}

// Функция для рисования штрих-кода
function drawBarcode(codeString, color) {
    const canvas = document.getElementById('barcodeCanvas');
    const ctx = canvas.getContext('2d');

    const canvasWidth = canvas.width;
    const canvasHeight = canvas.height;
    const barWidth = canvasWidth / codeString.length;

    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < codeString.length; i++) {
        ctx.fillStyle = codeString[i] === '1' ? color : '#ffffff';
        ctx.fillRect(barWidth * i, 0, Math.ceil(barWidth), canvasHeight);
    }
}
