let username = ""

export function updateLoggedIn(uname) {
    username = uname
    window.dispatchEvent(new CustomEvent('login', {detail: username, bubbles: true}));
}
