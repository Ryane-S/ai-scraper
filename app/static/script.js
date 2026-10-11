console.log("Script chargé !")

let allArticles = []
let currentCategory = "all"
let currentDisplayedArticles = 20
let hasMoreArticles = true

// Méthode qui fetch la liste des articles
async function loadArticles(skip=0, limit=20){
    const response = await fetch(`/news/articles?skip=${skip}&limit=${limit}`, {
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

// Fonction qui affiche les articles dans le DOM
function displayArticles() {
    // Construire le HTML à injecter dans le DOM
    let html = ''

    // Filtre les articles si une catégorie particulière a été sélectionnée
    const filtered = currentCategory === "all"
        ? allArticles
        : allArticles.filter(a => a.category === currentCategory);

    // Récupérer les infos des articles et remplir le HTML progressivement
    filtered.forEach(article => {
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
            <div class="article-category">${article.category}</div>
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

    if (!article.summary) {
        articleOverviewData = `
        <button type="button" id="back-btn">Retour</button>
        <h1>Article indisponible :(</h1>
        <h2>Veuillez réessayer plus tard.</h2>
        `
    }
    else {
        articleOverviewData = `
        <button type="button" id="back-btn">Retour</button>
        <h3><a href="${article.url}">Click here to read the article</a></h3>
        <h1 class="article-title-detail">${article.title}</h1>
        <div class="article-date-detail">${formattedDate}</div>
        <img src="${image_url}" alt="image" class="article-img-detail">
        <h2 class="article-summary">Summary</h2>
        <p>
            ${article.summary || "Résumé non disponible."}
        </p>
        `
    }

    articleOverview.innerHTML = articleOverviewData
    articleOverview.classList.add("visible")
    document.querySelector(".category-buttons").classList.add("disabled")
}

// Génère les boutons de catégories à partir des articles chargés
function displayCategoryButtons() {
    const otherBtns = document.querySelector(".other-btns");

    // Récupérer les catégories uniques (Set = pas de doublons)
    const uniqueCategories = [...new Set(
        allArticles
            .map(a => a.category)
            .filter(c => c)  // ignore null/undefined
    )].sort();  // tri alphabétique

    // Construire le HTML des boutons
    let html = '';
    uniqueCategories.forEach(category => {
        html += `<button type="button" class="category-btn" data-category="${category}">${category}</button>`;
    });

    otherBtns.innerHTML = html;
}

// Charge la liste des articles au démarrage
async function init() {
    try {
        allArticles = await loadArticles();
        // Si on a reçu 20 articles, il en reste peut-être d'autres
        hasMoreArticles = allArticles.length === 20;
        displayArticles();
        displayCategoryButtons();
        if (Object.entries(allArticles).length != 0){
            document.getElementById("all-btn").classList.add("active");
        }
        else {
            document.getElementById("all-btn").classList.add("hidden");
        }
        // Cache le bouton "Charger plus" s'il n'y a pas plus de 20 articles
        if (!hasMoreArticles) {
            loadMoreBtn.classList.add("hidden");
        }
    } catch (error) {
        console.error(error);
    }
}
init();

// Charge plus d'articles
const loadMoreBtn = document.getElementById("load-more-btn")
loadMoreBtn.addEventListener('click', async () => {
    if (Object.entries(allArticles).length == 0) return;
    const newArticles = await loadArticles(currentDisplayedArticles, 20);
    currentDisplayedArticles += newArticles.length;
    allArticles.push(...newArticles);
    displayArticles();

    // Si on a reçu moins de 20 articles, on est à la fin
    hasMoreArticles = newArticles.length === 20;
    if (!hasMoreArticles) {
        loadMoreBtn.classList.add("hidden");
    }
})

// Filtre les articles par catégorie
const categoryButtons = document.querySelector(".category-buttons");
categoryButtons.addEventListener('click', (event) => {
    const btn = event.target.closest('.category-btn, #all-btn');
    if (!btn) return;

    currentCategory = btn.dataset.category;
    displayArticles();
    updateActiveButton(btn);
    // On ne cache le bouton "Charger plus" que si on n'est PAS sur "Tous" ou s'il n'y a plus d'articles
    if (currentCategory !== "all" || !hasMoreArticles) {
        loadMoreBtn.classList.add('hidden');
    } else {
        loadMoreBtn.classList.remove('hidden');
    }
});

// Met à jour la classe .active sur le bon bouton
function updateActiveButton(activeBtn) {
    document.querySelectorAll('.category-btn, #all-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    activeBtn.classList.add('active');
}

// Recharge simplement la liste des articles depuis la BDD
const button = document.getElementById("refresh-btn");
button.addEventListener('click', async () => {
    // Feedback visuel
    button.disabled = true;

    try {
        // Recharger les articles (première page uniquement)
        allArticles = await loadArticles();

        // Reset des variables d'état (compteur de pagination + filtre catégorie)
        currentDisplayedArticles = 20;
        currentCategory = "all";
        hasMoreArticles = allArticles.length === 20;

        // Afficher les articles et régénérer les boutons de catégories
        displayArticles();
        displayCategoryButtons();

        // Remettre le bouton "Tous" comme seul bouton actif (et le rendre visible)
        const allBtn = document.getElementById("all-btn");
        document.querySelectorAll('.category-btn, #all-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        allBtn.classList.add("active");
        allBtn.classList.remove("hidden");

        // Réafficher ou cacher le bouton "Charger plus" selon hasMoreArticles
        if (hasMoreArticles) {
            loadMoreBtn.classList.remove("hidden");
        } else {
            loadMoreBtn.classList.add("hidden");
        }
    }
    catch (error) {
        console.error("Erreur: ", error);
        alert("Impossible de recharger la liste.");
    }
    finally {
        // Réactiver le bouton
        button.disabled = false;
    }
})

// Affiche la vue détaillée d'un article
const main = document.querySelector(".main");
main.addEventListener('click', async (event) => {
    const card = event.target.closest('.article');
    if (!card) return;
    const articleId = card.dataset.id;
    const article = await loadArticle(articleId);
    window.scrollTo({top:0, behavior:'smooth'})
    button.disabled = true;
    loadMoreBtn.classList.add("hidden")
    main.classList.add("hidden")
    showDetail(article);
})

// Cache la vue détaillée d'un article
const detail = document.querySelector(".detail");
detail.addEventListener('click', async (event) => {
    const backButton = event.target.closest('#back-btn');
    if (!backButton) return;
    detail.classList.remove("visible")
    // Réafficher le bouton seulement si on est sur "Tous" et qu'il reste des articles
    if (currentCategory === "all" && hasMoreArticles) {
        loadMoreBtn.classList.remove("hidden")
    }
    main.classList.remove("hidden")
    // Réactiver le bouton de rechargement et les filtres
    button.disabled = false;
    document.querySelector(".category-buttons").classList.remove("disabled");
})