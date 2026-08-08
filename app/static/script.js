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