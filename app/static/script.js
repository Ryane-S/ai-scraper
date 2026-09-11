console.log("Script chargé !")

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

// Méthode qui fetch un article en particulier avec son id
async function loadArticle(id){
    const response = await fetch(`/news/articles/${id}`, {
        method: 'GET',
        headers: {
            "Accept": "application/json",
        }
    })
    if (response.ok == true){
        const article = await response.json();
        return article;
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
        <article class="article" data-id="${article.id}">
            <img src="${image_url}" alt="image" class="article-img">
            <div class="article-date">${formattedDate}</div>
            <div class="article-source">${article.source}</div>
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

// Fonction qui affiche le contenu de l'article et son résumé
function showDetail(article){
    const articleOverview = document.querySelector(".detail");

    // Gérer le cas où l'url de l'image n'est pas disponible
    const image_url = article.image_url || "https://placehold.co/800x400";

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

    let articleOverviewData;

    if (!article.content) {
        articleOverviewData = `
        <button type="button" id="backBtn">Retour</button>
        <h1>Article indisponible :(</h1>
        <h2>Veuillez réessayer plus tard.</h2>
        `
    }
    else {
        articleOverviewData = `
        <button type="button" id="backBtn">Retour</button>
        <h3><a href="${article.url}">Click here to read the article</a></h3>
        <h1 class="article-title-detail">${article.title}</h1>
        <img src="${image_url}" alt="image" class="article-img-detail">
        <div class="article-date-detail">${formattedDate}</div>
        <h2 class="article-summary">Summary</h2>
        <p>
            ${article.summary || "Résumé non disponible."}
        </p>
        <h2 class="article-content">Full Content</h2>
        <p>
            ${article.content || "Contenu complet non disponible."}
        </p>
        `
    }

    articleOverview.innerHTML = articleOverviewData
    articleOverview.classList.add("visible")
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
        console.error("Erreur: ", error);
        alert("Le scraping a échoué !");
    }
    finally {
        // Vérifier le statut avant de réactiver : si le scraping tourne encore,
        // on laisse le bouton désactivé (le polling s'en chargera)
        const status = await checkScrapStatus();
        if (status !== "running") {
            button.disabled = false;
            button.textContent = "Rafraichir";
        }
    }
})

// Affiche la vue détaillée d'un article
const main = document.querySelector(".main");
main.addEventListener('click', async (event) => {
    const card = event.target.closest('.article');
    if (!card) return;
    const articleId = card.dataset.id;
    const article = await loadArticle(articleId);
    button.disabled = true;
    main.classList.add("hidden")
    showDetail(article);
})

// Cache la vue détaillée d'un article
const detail = document.querySelector(".detail");
detail.addEventListener('click', async (event) => {
    const backButton = event.target.closest('#backBtn');
    if (!backButton) return;
    detail.classList.remove("visible")
    main.classList.remove("hidden")
    // Vérifier le statut avant de réactiver le bouton
    const status = await checkScrapStatus();
    if (status !== "running") {
        button.disabled = false;
        button.textContent = "Rafraichir";
    }
})