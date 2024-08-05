document.getElementById('id_image').addEventListener('change', function (event) {
    const [file] = event.target.files;
    if (file) {
        const preview = document.getElementById('image-preview');
        preview.src = URL.createObjectURL(file);
        preview.style.display = 'block';
    }
});