document.addEventListener('DOMContentLoaded', function () {
    // Buttons fow modal windows
    var editButtons = document.querySelectorAll('#edit-button');

    // Modal window
    var modal = document.getElementById('ModalWindos');

    // Modal window textarea
    var textarea = document.getElementById('floatingTextarea');

    // Referencia al botón "Edit" dentro del modal
    var editBtn = document.getElementById('edit-btn');

    // ID courrent post
    var postId = null;

    // Close Modal window in X
    var span = document.getElementsByClassName('close')[0];


    if(span){
        span.addEventListener('click', function () {
        modal.style.display = 'none';
        });

        editBtn.addEventListener('click', function (ev) {
            ev.preventDefault()
            var newPostContent = textarea.value;
            
    
            //  Logic to modify the post using the new content (newPostContent) and the post ID (postId)
            function getCookie(csrftoken) {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${csrftoken}=`);
                if (parts.length == 2) return parts.pop().split(';').shift();
    
            }
    
            // Make the AJAX request to the server to save the edited post
            fetch('/edit/' + postId, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken') // Pass the CSRF token in the header
                    },
                    body: JSON.stringify({
                        postContentEdit: newPostContent
                    }),
                })
                .then(response => response.json())
                .then(data => {
                    // Manage server response after saving the publication
                    console.log(data.message);
    
                    // close the modal
                    modal.style.display = "none";
    
                    // Update the user interface
                    var nuevoContenidoEditado = data.postContentEdit;
    
                    // Update the content 
                    document.getElementById(`postContent_${postId}`).innerHTML= nuevoContenidoEditado              
                })
                .catch(error => {
                    console.error('Error al guardar la publicación:', error);
                });
    
       
            modal.style.display = 'none';
    
    
        });

    }
    
    
    

    // Event to close the modal by clicking outside it
    window.addEventListener('click', function (event) {
        if (event.target === modal) {
            modal.style.display = 'none';
        }
    });

    

    // Event to open the modal and get the post ID by clicking the "Edit" button
    editButtons.forEach(function (editButton) {
        editButton.addEventListener('click', function (event) {


            postId = event.target.dataset.post;
            postContentOld = event.target.parent
            

            textarea.value =  document.getElementById(`postContent_${postId}`).innerText
            modal.style.display = 'none';

            setTimeout(() => {
                modal.style.display = 'block';
            }, 100)

           //Random bg for modal

    var images = [
      'bgModal0.jpg',
      'bgModal1.jpg',
      'bgModal2.jpg',
      'bgModal3.jpg',
      'bgModal4.jpg',
      'bgModal5.jpg',
      'bgModal6.jpg',
      'bgModal7.jpg',

      
    ];
    
    var randomIndex = Math.floor(Math.random() * images.length);
    console.log(randomIndex)
    var randomImage = images[randomIndex];
    
    var element = document.querySelector('.modal-content');
    element.style.backgroundImage = 'url(' + "/static/network/images/" + randomImage + ')';
    element.style.backgroundSize = '100% 100%';
        });
    });

    // Event to modify the post by clicking the "Edit" button within the modal
    

    
    var liked = !liked 

 
    
});

// Difine an array with the state of each post
var likeStatus = {};


function likeUnlike(postId, whoYouLiked) {
  const btnLike = document.getElementById(`like_${postId}`);

 
    
   
    
  // See if Lie status is exist in the actual postId
  if (!(postId in likeStatus)) {
    likeStatus[postId] = whoYouLiked.indexOf(postId) >= 0;
  }

  var liked = likeStatus[postId];

  if (liked) {
    fetch(`/removeLike/${postId}`)
      .then(response => response.json())
      .then(data => {
        console.log(data.message)
        btnLike.classList.remove('fa-thumbs-down');
        btnLike.classList.add('fa-thumbs-up');
        likeStatus[postId] = false;
        document.getElementById(`totalLikes_${postId}`).textContent = "Likes : " + data.total_likes;
      })
      .catch(error => {
        console.error('Error when making the request Fetch:', error);
      });
      
      
  } else {
    fetch(`/addLike/${postId}`)
      .then(response => response.json())
      .then(data => {
        console.log(data.message)
        btnLike.classList.remove('fa-thumbs-up');
        btnLike.classList.add('fa-thumbs-down');
        likeStatus[postId] = true;
        document.getElementById(`totalLikes_${postId}`).textContent = "Likes : " + data.total_likes;
      })
      .catch(error => {
        console.error('Error when making the request Fetch:', error);
      });
      
  }
}



