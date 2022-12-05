async function JoinLobby(){
    let response = await fetch('http://127.0.0.1:3000/JoinNewLobby')
    let data = await response.json()
    return data
}

JoinLobby().then(data => console.log(data))