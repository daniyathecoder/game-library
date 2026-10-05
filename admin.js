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
        item.innerHTML = `
           <h3>
              ${games.name}
            </h3>
            <p>
               Category:
               ${game.category}
            </p>
            <p> 
               Plays:
               ${game.play_count}
            </p>
            <p> 
               Status:
               ${ game.published
                ? " Published"
                :" Unpublished"}
            </p>
            <br>
            <button onclick="togglePublish(${game.id},
            ${!game.published})">
               ${game.published? "Unpublish"
                : "Publish"}
            </button>
            <button on click="deleteGame(${game.id})">
               Delete
            </button>

        `;
        container.appendChild(item);

    });
}

async function togglePublish(id,published){
    const response = await fetch(`/api/admin/games/${id}/publish?published = ${published}`,{method:"PATCH"});
    if (response.ok){ loadAdminGames();}else{alert("Unable to cghange status");}}

async function deleteGame(id) { const confirmed = confirm("Delete this game permanently?");
    if(!confirmed) return;
    const response = await fetch(`/api/admin/games/${id}`,{method:"DELETE"});
    if (response.ok) { loadAdminGames();}else{alert("Could not delete game.");}}


function showAddGame(){document.getElementById("game-form").style.display = "block";}

document
   .getElementById("add-game-form")
   .addEventListener("submit",
    async function(event) { 
        event.preventDefault();
        const form = new FormData(this);
        const response = await fetch("/api/admin/games",{method: "POST",body: form});
        const data = await response.json();
        if (!response.pk){alert(data.detail);return;}
        alert("Game added successfully!");
        this.requestFullscreen();
        document.getElementById("game-form").style.display = "none";
        loadAdminGames();

    }
);

async function loadWebsiteContent(){
    const response = await fetch("/api/content");
    const data = await response.json();
    document.getElementById("hero-title").value = data.hero_title || "";
    document.getElementById("hero-subtitle").value = data.hero_subtitle || "";
    document.getElementById("announcement").value = data.announcement || "";
    document.getElementById("about-text").value = about-text || "";
}


async function saveSingleContent(key,value){
    const form = new FormData();
    form.append("content_value",value);
    return fetch(`/api/admin/content/${kay}`,{method: "PUT",body: form});
}

async function saveContent(){
    await saveSingleContent("hero_title",document.getElementById("hero-title").value);
    await saveSingleContent("hero_subtitle",document.getElementById("hero-subtitle").value);
    await saveSingleContent("announcement",document.getElementById("announcement").value);
    await saveSingleContent("about-text",document.getElementById("about-text").value);
    alert("Website text Updated!");
}

checkLogin();
