// JavaScript for the bird exhibition site

document.addEventListener('DOMContentLoaded', function() {
    // Image preview for upload form
    const imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.onchange = function() {
            const [file] = imageInput.files;
            if (file) {
                let previewDiv = document.getElementById('image-preview');
                if (!previewDiv) {
                    previewDiv = document.createElement('div');
                    previewDiv.id = 'image-preview';
                    previewDiv.className = 'mt-3';
                    imageInput.parentNode.appendChild(previewDiv);
                }
                
                previewDiv.innerHTML = `
                    <h6>Предпросмотр:</h6>
                    <img src="${URL.createObjectURL(file)}" 
                         class="img-thumbnail" 
                         style="max-width: 300px; max-height: 300px;">
                `;
            }
        };
    }
    
    // Star rating for judge evaluation
    const scoreInput = document.getElementById('id_score');
    if (scoreInput && scoreInput.type === 'number') {
        scoreInput.classList.add('form-range');
        scoreInput.setAttribute('min', '1');
        scoreInput.setAttribute('max', '10');
        scoreInput.setAttribute('step', '1');
        
        const scoreValue = document.createElement('div');
        scoreValue.className = 'form-text text-center mb-2';
        scoreValue.innerHTML = `Оценка: <strong>${scoreInput.value || 5}</strong> из 10`;
        
        scoreInput.parentNode.insertBefore(scoreValue, scoreInput);
        
        scoreInput.addEventListener('input', function() {
            scoreValue.innerHTML = `Оценка: <strong>${this.value}</strong> из 10`;
        });
    }
});
