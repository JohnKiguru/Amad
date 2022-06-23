var updateBtns = document.getElementsByClassName('update-cart')

for (var i = 0; i < updateBtns.length; i ++){
    updateBtns[i].addEventListener('click', function(){
        var productId = this.dataset.item
        console.log(productId)
        var action = this.dataset.action
        console.log(action)


        console.log('User: ', user)
        if(user === 'AnonymousUser'){
            console.log('Not Authenticated...')
        }
        else{
            updateUserOrder(productId, action)
        }
    })
}
function updateUserOrder(productId, action, e){

    var url = 'http://127.0.0.1:8000/products/update/'

    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({'productId':productId, 'action':action})
    })
    .then((response) => {
        return response.json()
    })
    .then((data) => {
        console.log('data: ', data)
        location.reload()
    })
}