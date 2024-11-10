document.addEventListener('DOMContentLoaded', () => {
    const mediaItems = document.querySelectorAll('.media-item');
    const modal = document.getElementById('media-modal');
    const modalImage = document.getElementById('modal-image');
    const modalVideo = document.getElementById('modal-video');
    const closeBtn = document.querySelector('.close');

    mediaItems.forEach(item => {
        item.addEventListener('click', () => {
            const image = item.querySelector('img');
            const video = item.querySelector('video');
            
            if (image) {
                modalImage.src = image.src;
                modalVideo.style.display = 'none';
                modalImage.style.display = 'block';
            }
            
            if (video) {
                modalVideo.src = video.src;
                modalImage.style.display = 'none';
                modalVideo.style.display = 'block';
            }
            
            modal.style.display = 'block';
        });
    });

    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });
});
