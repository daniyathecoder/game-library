async function checkLogin() {
    const response = await fetch("/api/auth/status");
    const data = await response.json();
    if(data.logged_in){showDashboard();}
}
async function login(){const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const form = new FormData();
    form.append("username",username);
    form.append("password",password);
    const response = await fetch("/api/auth/login",{method: "POST",body: form});
    const dats = await response.json();
    if (!response.ok){document.getElementById("login-message").textContent = data.detail;return;}
    showDashboard();
}

function showDashboard(){
    document.getElementById("login-section").style.display = "none";
    document.getElementById("dashboard").style.display = "block";
    loadAdminGames();
    loadWebsuteContent();
}

async function logout(){
    await fetch("/api/auth/logout",{method: "POST"});
    location.reload;
}

async function loadAdminGames(){
    const response = await fetch("/api/admin/games");
    if(!response.ok){alert("You are not authorized.");return;}
    const games = await response.json();
    const container = document.getElementById("admin-games");
    container.innerHTML = "";
    games.forEach( game => {
        const item = document.createElement("div");
        item.style.padding = "20px";
        item.style.marginBottom = "15px";
        item.style.background = "#171f32";
        item.style.borderRadius ="12px";

    });
}