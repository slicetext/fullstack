let login_button = document.getElementById("login_button")

window.addEventListener('login', (e) => {
    document.getElementById('login_button').innerText = e.detail;
});

const logout_button = document.getElementById("logout_button");
logout_button.addEventListener('click', async () => {
    let response = await fetch("http://192.168.111.8:5000/api/logout", {method: 'POST'})
    localStorage.setItem("name", "Not Logged In")
    update_loggedin()
});

async function get_my_addresses() {
	let response = await fetch("http://192.168.111.8:5000/api/user_addresses")
	let json = await response.json()
	console.log(json)
}

const searchBox = document.getElementById("search");
searchBox.addEventListener('keydown', function(event) {
    if(event.key === 'Enter') {
        update_assigned(searchBox.value)
    }
});

const assigned_addresses = document.getElementById("assigned_addresses_rows");

class AssignedIP {
    constructor(address, owner, description) {
        this.address = address;
        this.owner = owner
        this.description = description;
    }
}

function create_entry(assigned_ip) {
    const row = assigned_addresses.insertRow(-1);
    const address = row.insertCell(0);
    address.textContent = assigned_ip.address;
    const owner = row.insertCell(1);
    owner.textContent = assigned_ip.owner;
    const description = row.insertCell(2);
    description.textContent = assigned_ip.description;
}

async function get_assigned(search) {
    // return [
    //     new AssignedIP("10.0.30.1", "me", "testing"),
    //     new AssignedIP("10.0.30.2", "you", "testing")
    // ]
    let response = await fetch("http://192.168.111.8:5000/api/search?q="+search)
    let json = await response.json()
    console.log(json)
    let results = []
    json.forEach((i) => {
        results.push(new AssignedIP(i[0], i[1], i[2]));
    });
    return results
}

async function update_assigned(search) {
    // Reset table
    assigned_addresses.innerHTML = '';
    const assigned = await get_assigned(search);
    assigned.forEach((i) => {
        create_entry(i);
    });
}

function update_loggedin() {
	let name = localStorage.getItem("name")
	login_button.innerHTML = name;
}

async function my_addresses() {
	let response = await fetch("http://192.168.111.8:5000/api/user_addresses")
	let json = await response.json()
	console.log(json)
	my_addresses = document.getElementById("my_addresses")
	json.forEach((entry) => {
		const row = my_addresses.insertRow(-1);
		const address = row.insertCell(0);
		address.textContent = entry[0]
		const description = row.insertCell(1);
		description.textContent = entry[2]

		const remove = row.insertCell(2);

		const button = document.createElement('button');
		button.textContent = "Remove";
		button.classList.add("remove-btn")
		button.dataset.address = entry[0]

		button.addEventListener("click", async () => {
			let delete_response = await fetch("http://192.168.111.8:5000/api/remove_address", {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify( { 'address': event.target.dataset.address} )
			})
			if (!response.ok) {
				throw new Error(`HTTP error! Status: ${response.status}`);
			}
			window.location.reload()

		});

		remove.appendChild(button)
	});
}

document.addEventListener("DOMContentLoaded", () => {
	//update_assigned();
	update_loggedin();
	my_addresses();
});

