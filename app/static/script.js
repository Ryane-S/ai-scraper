// Méthode qui fetch la liste des articles
async function loadArticles(){
    const response = await fetch("/news/articles", {
        method: 'GET',
        headers: {
            "Accept": "application/json",
        }
    })
    if (response.ok == true){
        const articles = await response.json();
        return articles;
    }
    throw new Error("Impossible de contacter le serveur")
}

// Méthode qui lance le scraper pour rafraichissement
async function scrapArticles(){
    const response = await fetch("/news/scrape", {
        method: 'POST',
        headers: {
            "Accept": "application/json",
        }
    })
    if (response.ok == true){
        return true
    }
    throw new Error("Impossible de contacter le serveur")
}

// Méthode qui vérifie le statut du scraping
async function checkScrapStatus() {
    const response = await fetch("/news/scrape/status");
    const data = await response.json();
    return data.status; // "idle", "running", ou "error"
}

function pollStatus() {
    return new Promise((resolve, reject) => {
        const interval = setInterval(async () => {
            const status = await checkScrapStatus();
            if (status === "idle") {
                clearInterval(interval);
                resolve();
            } else if (status === "error") {
                clearInterval(interval);
                reject(new Error("Le scraping a échoué"));
            }
            // Si "running", on continue
        }, 1000);
    });
}

// Fonction qui affiche les articles dans le DOM
function displayArticles(articles) {
    // Construire le HTML à injecter dans le DOM
    let html = ''

    // Récupérer les infos des articles et remplir le HTML progressivement
    articles.forEach(article => {
        // Gérer le cas où l'url de l'image n'est pas disponible
        const image_url = article.image_url || "https://placehold.co/400x200";
        // Formater la date avec gestion des erreurs
        let formattedDate = "Date inconnue";
        if (article.date) {
            const dateObj = new Date(article.date);
            if (!isNaN(dateObj.getTime())) {
                formattedDate = dateObj.toLocaleString('fr-FR', {
                    day: 'numeric',
                    month: 'long',
                    year: 'numeric',
                    hour: '2-digit',
                    minute: '2-digit'
                });
            }
        }
        // Construire la chaine contenant les infos d'un article
        const articleData = `
        <article class="article">
            <img src="${image_url}" alt="image" class="article-img">
            <div class="article-date">${formattedDate}</div>
            <h2 class="article-title">${article.title}</h2>
            <p>
                ${article.description || "Pas de description disponible."}
            </p>
        </article>
        `
        html += articleData
    });

    // Injecter le HTML dans le DOM
    const conteneur = document.querySelector(".main") // Récupérer la classe du conteneur d'article
    conteneur.innerHTML = html;
}

// Fetch la liste des articles
const articles = loadArticles()
    .then(articles => {
        displayArticles(articles);
    })
    .catch(error => {
        console.error(error);
    });

// Rafraichit la liste des articles
const button = document.getElementById("refreshBtn");
button.addEventListener('click', async () => {
    // Désactiver le bouton
    button.disabled = true
    button.textContent = "Scraping en cours ..."

    try {
        // Lancer le scraping
        await scrapArticles();

        // Lancer la boucle de polling
        await pollStatus();

        // Recharger les articles
        const updatedArticles = await loadArticles();
        displayArticles(updatedArticles);
    }
    catch (error) {
        console.error("Erreur: ", error)
        alert("Le scraping a échoué !")
    }
    finally {
        button.disabled = false
        button.textContent = "Rafraichir"
    }
})