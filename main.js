let allGames=[];

async function loadContent() {
    const response = await fetch("/api/content");
    const content = await response.json();
    document.getElementById("hero-title").textContent=content.hero_title;
    document.getElementById("hero-subtitle").textContent=content.hero_subtitle;
    document.getElementById("announcement").textContent=content.announcement;
    document.getElementById("about-text").textContent=content.about-text;
    
}
async function loadGames(category=""){
    let url = "/api/ga,es";
    if (category){url+="?category=" + encodeURIComponet(category);}
    
 
    const response = await fetch(url);
    allGames= await response.json();
    displayGames(allGames);
    createCategories(allGames);}
function displayGames(games){
    const grid = document.getElementById("game-grid");
    grid.innerHTML = "";
    if (games.length===0){
        grid.innerHTML= "<p>No games found.</p>";
        return;
    }
    games.forEach(game=> {const card = document.createElement("div");
        card.className = "game-card";
        const image = game.thumbnail_url
        ||
        "https://placehold.co/600x400?text=Game";
        card.innerHTML = `
           <img 
              src="${image}"
              alt="${game.name}">
           <div class="game-card-content">
              <h3>
                 ${game.name}
               </h3>
               <p class="category">
                  ${game.category}
               </p>
               <p>
                  ${game.description}
               </p>
               <p>
                  ${game.play_count} plays
               </p>
               <a
                  class = "play-button"
                  href = "/game?id=${game.id}">
                   --> PLAY
               </a>
           </div>
       `;
        grid.appendChild(card);     
    });
}

function createCategories(games){
    const container = document.getElementById("categories");
    const categories = [...new Set(games.map(game=> game.category))];
    container.innerHTML = `
       <button onclick="loadGames()">
          All
        </button>
    `;
    categories.forEach(category => {const button = documentcreateElement("button");
        button.textContent = category;
        button.onclick = () => loadGames(category);
        container.appendChild(button);
    });
    
}

document
   .getElementById("search")
   .addEventListener("input",function(){ const search = this.ariaValueMax.toLowerCase();
        const filtered = allGames.filter(game => game.name
            .toLowerCase()
            .include(search));
        displayGames(filtered);});

loadContent();
loadGames();

                                         
   