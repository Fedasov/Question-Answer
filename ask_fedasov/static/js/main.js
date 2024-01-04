function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const items_like = document.getElementsByClassName('reaction-question')
for (let item of items_like) {
    const [button, counter, disbutton] = item.children;
    button.addEventListener('click', (reaction) => {
        const formData = new FormData();
        formData.append('object_id', button.dataset.id)
        formData.append('like', button.dataset.like)
        console.log(button);
        console.log(disbutton);
        console.log("TRUE");
        formData.append('like', button.dataset.like)
        if (disbutton.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-down-fill") {
            disbutton.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-down-fill");
            disbutton.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-down");
        }
        if (button.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-up") {
            button.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-up");
            button.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-up-fill");
        } else {
            button.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-up-fill");
            button.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-up");
        }

        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.counter;
            });
    })

    disbutton.addEventListener('click', (reaction) => {
        const formData = new FormData();
        formData.append('object_id', button.dataset.id)
        formData.append('like', button.dataset.like)
        console.log(button);
        console.log(disbutton);
        console.log("False");
        formData.append('like', disbutton.dataset.like)
        if (button.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-up-fill") {
            button.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-up-fill");
            button.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-up");
        }
        if (disbutton.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-down") {
            disbutton.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-down");
            disbutton.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-down-fill");
        } else {
            disbutton.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-down-fill");
            disbutton.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-down");
        }

        const request = new Request('/like/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.counter
            });
    })
}

const answer_like = document.getElementsByClassName('reaction-answer')
for (let item of answer_like) {
    const [button, counter, disbutton] = item.children;
    button.addEventListener('click', (answer_reaction) => {
        const formData = new FormData();
        formData.append('object_id', button.dataset.id)
        formData.append('like', button.dataset.like)
        formData.append('like', button.dataset.like)
        if (disbutton.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-down-fill") {
            disbutton.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-down-fill");
            disbutton.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-down");
        }
        if (button.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-up") {
            button.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-up");
            button.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-up-fill");
        } else {
            button.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-up-fill");
            button.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-up");
        }

        const request = new Request('/like/answer/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.counter;
            });
    })

    disbutton.addEventListener('click', (reaction) => {
        const formData = new FormData();
        formData.append('object_id', button.dataset.id)
        formData.append('like', button.dataset.like)
        console.log(button);
        console.log(disbutton);
        console.log("False");
        formData.append('like', disbutton.dataset.like)
        if (button.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-up-fill") {
            button.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-up-fill");
            button.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-up");
        }
        if (disbutton.getElementsByTagName('i')[0].classList[1] == "bi-hand-thumbs-down") {
            disbutton.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-down");
            disbutton.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-down-fill");
        } else {
            disbutton.getElementsByTagName('i')[0].classList.remove("bi-hand-thumbs-down-fill");
            disbutton.getElementsByTagName('i')[0].classList.add("bi-hand-thumbs-down");
        }

        const request = new Request('/like/answer/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request)
            .then((response) => response.json())
            .then((data) => {
                console.log({data});
                counter.innerHTML = data.counter;
            });
    })
}

const checkbox_checked = document.getElementsByClassName('fluency')
for (let item of checkbox_checked) {
    const [checkbox] = item.children;
    checkbox.addEventListener('click', (reaction) => {
        const formData = new FormData();
        console.log(checkbox)
        formData.append('object_id', checkbox.dataset.id);
        const request = new Request('/answer_correct/', {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
            }
        });

        fetch(request).then((response) => response.json())
    })
}

const user_input = $("#user-input")
const search_icon = $('#search-icon')
const artists_div = $('#replaceable-content')
const endpoint = '/'
const delay_by_in_ms = 700
let scheduled_function = false

let ajax_call = function (endpoint, request_parameters) {
    $.getJSON(endpoint, request_parameters)
        .done(response => {
            artists_div.fadeTo('slow', 0).promise().then(() => {
                artists_div.html(response['html_from_view'])
                artists_div.fadeTo('slow', 1)
                search_icon.removeClass('blink')
            })
        })
}

user_input.on('keyup', function () {
    const request_parameters = {
        q: $(this).val()
    }
    search_icon.addClass('blink')
    if (scheduled_function) {
        clearTimeout(scheduled_function)
    }
    scheduled_function = setTimeout(ajax_call, delay_by_in_ms, endpoint, request_parameters)
})
