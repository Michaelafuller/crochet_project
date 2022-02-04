var commentForm = document.querySelector('#comment')

console.log(commentForm)

commentForm.addEventListener('submit', function(e){
    e.preventDefault()

    let form = new FormData(commentForm)

    fetch('/comments/create', {
        method: 'post',
        body: form
    }) 
    .then(resp => resp.json())
    .then(data => {
        console.log(data);
        if (data.message === 'success'){
            var newComment = document.querySelector('#newComment')
            var content = data.content 

            newComment.innerHTML += `
                <div class="container-fluid bg-dark text-light m-4 p-3 rounded-3">
                    <h4>Comment: </h4>
                    <p class="m-3"> ${content.content}</p>
                </div>
                `
        }
        else{
            console.log('Failure')
        }
    })
    .catch(e => console.log(e))
})