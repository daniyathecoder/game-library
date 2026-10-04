/*im so tiredddddddddddd*/
const gameCards = document.querySelectorAll(".game-card");
const searchButton = document.querySelector(".search-button");
const seeAllButton = document.querySelector(".section-heading a");
const adventureCategory = document.querySelector("#adventure");
const twoPlayerCategory = document.querySelector("#players2");

/*search*/
searchButton.addEventListener("click", function() {
    const search = prompt("search a game");


if (search == null) {
    return;
}

const searchText = search.toLowerCase();

gameCards.forEach(function (card) 
{
    const gameName = card
    .querySelector("h3")
    .textContent
    .toLowerCase();

    if (gameName.includes(searchText)) {
        card.computedStyleMap.display = "block";
    } else {
        card.style.display = "none";
    }
    
});


document 
.querySelector("#games")
.scrollIntoView({
    behavior: "smooth"
});

});

seeAllButton.addEventListener("click", function(event) {
    event.preventDefault();

    gameCards.forEach(function (card) {
        card.style.display = "block";
    });


    document
    .querySelector("#games")
    .scrollIntoView({
        behavior: "smooth"
    });

});

adventureCategory.addEventListener("click", function () {
    gameCards.forEach( function (card) {
        card.style.display="none";
    });

    const eraBreaker = adventureCategory.querySelector(".game-card");

    if (eraBreaker) {
        eraBreaker.style.display = "block";

    }

    document 
    .querySelector("#games")
    .scrollIntoView({
        behavior: "smooth"
    });
});

twoPlayerCategory.addEventListener("click", function() {
    gameCards.forEach(function (card) {
        card.style.display = "none";
    });

    const fireboy = twoPlayerCategory.querySelector(".game-card");

    if (fireboy) {
        fireboy.style.display = "block";
    }

    document
    .querySelector("#games")
    .scrollIntoView({
        behavior: "smooth"
    });
});
