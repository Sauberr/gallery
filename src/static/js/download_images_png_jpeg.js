document.addEventListener('DOMContentLoaded', function () {
    const downloadButtons = document.querySelectorAll('.download-btn');

    downloadButtons.forEach(button => {
        button.addEventListener('click', function (event) {
            event.preventDefault();
            const imageUrl = this.getAttribute('data-url');
            const format = this.getAttribute('data-format');
            downloadImage(imageUrl, format);
        });
    });

    function downloadImage(url, format) {
        const img = new Image();
        img.crossOrigin = 'Anonymous';
        img.src = url;
        img.onload = function () {
            const canvas = document.createElement('canvas');
            canvas.width = img.width;
            canvas.height = img.height;
            const ctx = canvas.getContext('2d');
            ctx.drawImage(img, 0, 0);
            const dataUrl = canvas.toDataURL(`image/${format}`);
            const link = document.createElement('a');
            link.href = dataUrl;
            link.download = `image.${format}`;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        };
    }
});