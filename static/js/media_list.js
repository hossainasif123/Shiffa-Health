document.addEventListener('DOMContentLoaded', () => {
    const mediaItems = document.querySelectorAll('.media-item');
    const modal = document.getElementById('media-modal');
    const modalImage = document.getElementById('modal-image');
    const modalVideo = document.getElementById('modal-video');
    const closeBtn = document.querySelector('.close');
    const deleteModal = document.getElementById('modal-d');
    const confirmDeleteBtn = document.getElementById('confirm-delete');
    const cancelDeleteBtn = document.getElementById('cancel-delete');

    let mediaIdToDelete = null;
    let deleteUrl = null;

    // Open media in modal
    mediaItems.forEach(item => {
        item.addEventListener('click', (event) => {
            // Prevent clicking on delete button from opening the media
            if (event.target.classList.contains('delete-option')) return;

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

        // Handle options menu click
        const optionsMenu = item.querySelector('.options-menu');
        if (optionsMenu) {
            optionsMenu.addEventListener('click', (event) => {
                event.stopPropagation(); // Prevent parent click event

                const dropdown = item.querySelector('.options-dropdown');
                if (dropdown) {
                    dropdown.style.display = dropdown.style.display === 'block' ? 'none' : 'block';
                }
            });
        }

        // Handle delete option click
        const deleteOption = item.querySelector('.delete-option');
        if (deleteOption) {
            deleteOption.addEventListener('click', (event) => {
                event.stopPropagation(); // Prevent parent click event

                mediaIdToDelete = item.dataset.mediaId;
                deleteUrl = deleteOption.getAttribute('data-delete-url');

                deleteModal.style.display = 'block';
            });
        }
    });

    // Close the media modal
    closeBtn.addEventListener('click', () => {
        modal.style.display = 'none';
    });

    window.addEventListener('click', (event) => {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
        if (event.target === deleteModal) {
            deleteModal.style.display = 'none';
        }

        // Hide all dropdowns when clicking outside
        if (!event.target.closest('.media-item')) {
            document.querySelectorAll('.options-dropdown').forEach(dropdown => {
                dropdown.style.display = 'none';
            });
        }
    });

    // Handle the delete confirmation
    confirmDeleteBtn.addEventListener('click', () => {
        if (mediaIdToDelete && deleteUrl) {
            deleteMedia(deleteUrl, mediaIdToDelete);
        }
    });

    // Handle the delete cancellation
    cancelDeleteBtn.addEventListener('click', () => {
        deleteModal.style.display = 'none';
    });

    // Function to handle the AJAX delete
    function deleteMedia(deleteUrl, mediaId) {
        fetch(deleteUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ media_id: mediaId })
        })
        .then(response => {
            if (response.ok) {
                const mediaItem = document.querySelector(`.media-item[data-media-id="${mediaId}"]`);
                if (mediaItem) {
                    mediaItem.remove();
                }

                deleteModal.style.display = 'none';
                alert('Media deleted successfully');
            } else {
                return response.json().then(errorData => {
                    alert("Error: " + errorData.message || "Could not delete media.");
                });
            }
        })
        .catch(error => {
            console.error("Error:", error);
            alert("Error: Could not delete media.");
        });
    }
});

// Function to submit the upload form
function submitForm() {
    document.getElementById('upload-form').submit();
}
