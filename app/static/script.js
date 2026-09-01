// Méthode qui fetch la liste des articles
async function loadArticles(){
    const response = await fetch("http://127.0.0.1:8000/news/articles", {
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
    const response = await fetch("http://127.0.0.1:8000/news/scrape", {
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

// Fetch la liste des articles
const articles = loadArticles()
    .then(articles => {
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
    })
    .catch(error => {
        console.error(error);
    });

// Rafraichit la liste des articles
const button = document.querySelector(".scrapping-button button") // Récupérer la classe du bouton rafraîchir
