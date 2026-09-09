from urllib.parse import urljoin

import requests
import trafilatura
from bs4 import BeautifulSoup, Tag


def extract_primary_image(html_content: str, page_url: str) -> str | None:
    """Extrait l'URL de l'image principale (meta og:image, twitter:image, ou heuristique)."""
    soup = BeautifulSoup(html_content, "html.parser")

    # ÉTAPE 1 : Open Graph
    og_image = soup.find("meta", property="og:image")
    if isinstance(og_image, Tag):
        content = og_image.get("content")
        if content is not None and isinstance(content, str):
            return urljoin(page_url, content)

    # ÉTAPE 2 : Twitter Card
    tw_image = soup.find("meta", attrs={"name": "twitter:image"})
    if isinstance(tw_image, Tag):
        content = tw_image.get("content")
        if content is not None and isinstance(content, str):
            return urljoin(page_url, content)

    # ÉTAPE 3 : Heuristique (fallback)
    for tag in soup(["script", "style"]):
        tag.decompose()

    container = soup.find("article") or soup.find("main") or soup.body
    if not container or not isinstance(container, Tag):
        return None

    images = container.find_all("img")
    best_image: str | None = None
    best_score = -1

    for img in images:
        if not isinstance(img, Tag):
            continue

        # Récupération de src (peut être None, str, ou list)
        src_attr = img.get("src")
        if src_attr is None:
            continue
        if isinstance(src_attr, list):
            if not src_attr:  # liste vide
                continue
            src = src_attr[0]
        else:
            src = src_attr
        if not isinstance(src, str):
            continue

        # Largeur / hauteur
        width_attr = img.get("width")
        height_attr = img.get("height")

        def _to_int(value: str | list[str] | None) -> int:
            if value is None:
                return 0
            if isinstance(value, list):
                if not value:
                    return 0
                value = value[0]
            if isinstance(value, str) and value.isdigit():
                return int(value)
            return 0

        w = _to_int(width_attr)
        h = _to_int(height_attr)

        if w < 200 and h < 200 and (w != 0 or h != 0):
            continue

        # Classes (sans valeur par défaut)
        class_attr = img.get("class")
        if class_attr is None:
            class_str = ""
        elif isinstance(class_attr, str):
            class_str = class_attr
        else:
            # AttributeValueList (ou autre séquence)
            class_str = " ".join(class_attr) if class_attr else ""

        class_lower = class_str.lower()

        # Parent id
        parent = img.parent
        parent_id = ""
        if isinstance(parent, Tag):
            pid = parent.get("id")
            if pid is None:
                pass
            elif isinstance(pid, str):
                parent_id = pid
            elif isinstance(pid, list) and pid:
                parent_id = pid[0]
        parent_lower = parent_id.lower()

        score = w + h
        if "featured" in class_lower or "hero" in class_lower or "cover" in class_lower:
            score += 1000
        if "featured" in parent_lower or "hero" in parent_lower:
            score += 500

        srcset_attr = img.get("srcset")
        if srcset_attr:
            score += 300

        if score > best_score:
            best_score = score
            best_image = src

    if best_image:
        return urljoin(page_url, best_image)
    return None


def get_article_content(link: str) -> str | None:
    """Extrait le contenu texte de l'article via trafilatura."""
    response = requests.get(link, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code == 200:
        content = trafilatura.extract(response.text)
        if content:
            return content
    return None


def extract_full_article(url: str) -> dict:
    """Combine les deux fonctions pour retourner à la fois le contenu et l'image."""
    response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"})
    if response.status_code != 200:
        return {
            "content": None,
            "image": None,
            "error": f"HTTP error {response.status_code}",
        }

    html = response.text
    content = trafilatura.extract(html)
    image = extract_primary_image(html, url)

    return {"content": content, "image": image, "error": None}