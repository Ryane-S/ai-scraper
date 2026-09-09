import requests
import trafilatura
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def extract_primary_image(html_content, page_url):
    """Extrait l'URL de l'image principale (meta og:image, twitter:image, ou heuristique)."""
    soup = BeautifulSoup(html_content, "html.parser")
    
    # ÉTAPE 1 : Open Graph
    og_image = soup.find("meta", property="og:image")
    if og_image and og_image.get("content"):
        return urljoin(page_url, og_image["content"])
    
    # ÉTAPE 2 : Twitter Card
    tw_image = soup.find("meta", attrs={"name": "twitter:image"})
    if tw_image and tw_image.get("content"):
        return urljoin(page_url, tw_image["content"])
    
    # ÉTAPE 3 : Heuristique (fallback)
    for tag in soup(["script", "style"]):
        tag.decompose()
    
    container = soup.find("article") or soup.find("main") or soup.body
    if not container:
        return None
    
    images = container.find_all("img")
    best_image = None
    best_score = -1
    
    for img in images:
        src = img.get("src")
        if not src:
            continue
        
        width = img.get("width")
        height = img.get("height")
        try:
            w = int(width) if width and width.isdigit() else 0
            h = int(height) if height and height.isdigit() else 0
        except (ValueError, TypeError):
            w, h = 0, 0
        
        if w < 200 and h < 200 and (w != 0 or h != 0):
            continue
        
        classes = " ".join(img.get("class", []))
        parent_id = img.parent.get("id", "") if img.parent else ""
        
        score = w + h
        if "featured" in classes.lower() or "hero" in classes.lower() or "cover" in classes.lower():
            score += 1000
        if "featured" in parent_id.lower() or "hero" in parent_id.lower():
            score += 500
        if img.get("srcset"):
            score += 300
        
        if score > best_score:
            best_score = score
            best_image = src
    
    if best_image:
        return urljoin(page_url, best_image)
    return None


def get_article_content(link: str) -> str:
    """Extrait le contenu texte de l'article via trafilatura."""
    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        content = trafilatura.extract(response.text)
        if content:
            return content
    return None


def extract_full_article(url: str) -> dict:
    """Combine les deux fonctions pour retourner à la fois le contenu et l'image."""
    # 1. Récupération du HTML
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return {
            "content": None,
            "image": None,
            "error": f"HTTP error {response.status_code}"
        }
    
    html = response.text
    
    # 2. Extraction du contenu
    content = trafilatura.extract(html)
    
    # 3. Extraction de l'image
    image = extract_primary_image(html, url)
    
    return {
        "content": content,
        "image": image,
        "error": None
    }
