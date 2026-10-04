const params = new URLSearchParams(window.location.search);
const gameId = params.get("id");
async function loadGame(){
    if (!gameId){ document.getElementById("game-dtails").textContent = "Game ID Missing.";
        return;
    }
    const response = await fetch(`/api/games/${gameId}`);
    if (!response.ok){ document.getElementById("game-deatails").textContent = "Game not Found";return;}
    const game = await response.json();
    document.getElementById("game-details").innerHTML = ` 
       <div class="game-card">
          <img 
             src="${game.thumbnail_url|| "https://placehold.co/800x500?text=Game"}"alt="${game.name}">
          <div class="game-card-content">
             <h1>
                ${game.name}
              </h1>
              <p class = "category">
                 ${game.category}
               </p>
               <br>
               <p> 
                  Creator: ${game.creator}
               </p>
               <p> 
                  ${game.play_count} plays
               </p>
               <br>
               < button class = "primary-button"
               oneclick="playGame()">
                  --> PLAY NOW!!
               </button>
               ${game.github_url?`
                   <p style="margin-top:20px">
                      <a href = "${game.github_url}"
                      target="_blank">
                         View GitHub
                      </a>
                   </p>
                   `: ""}
           </div
       </div>
    `;
       
}
async function playGame(){
    await fetch(`/api/games/${gameId}/play`,{method: "POST"});
    const response = await fetch(`/api/games/${gameId}`);
    const game = await response.json();
    window.location.href = game.playable_url;}

loadGame();