function getJson(url, callback){
    fetch(url)
        .then((response) => {return response.json()})
        .then(data => callback(data))
}

function postJson(url, data, callback){
    fetch(url, {
        method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json; charset=UTF-8',
            'X-CSRFToken': csrftoken
          },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => callback(data));
}