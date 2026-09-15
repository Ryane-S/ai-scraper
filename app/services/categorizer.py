from functools import lru_cache
from sentence_transformers import SentenceTransformer, util

CATEGORIES = {
    "IA": """Artificial intelligence, machine learning, deep learning, large language models, neural networks, 
AI research, AI companies (OpenAI, Anthropic, Google DeepMind), generative AI, computer vision, 
natural language processing, AI ethics, AI regulation.""",

    "Tech": """Technology, software development, programming, hardware, startups, product launches, 
tech companies, cybersecurity, internet, apps, gadgets, computer science, open source, 
cloud computing, semiconductors, consumer electronics.""",

    "Science": """Scientific research, discoveries, physics, biology, chemistry, astronomy, space exploration, 
genetics, neuroscience, ecology, geology, scientific studies, experiments, academic research.""",

    "Politics": """National politics, elections, government policies, legislation, political parties, politicians, 
public policy, political debates, parliamentary decisions, political campaigns, local government.""",

    "Geopolitics": """International relations, diplomacy, foreign policy, conflicts, wars, tensions between countries, 
treaties, international organizations (UN, NATO, EU), global security, cross-border issues, 
world leaders, humanitarian crises.""",

    "Finance": """Financial markets, stock markets, investments, banking, central banks, inflation, interest rates, 
earnings, IPOs, cryptocurrencies, hedge funds, trading, financial regulation.""",

    "Economics": """Economy, economic growth, employment, unemployment, trade, economic policy, business, 
corporations, industry, manufacturing, supply chains, macroeconomic trends, GDP.""",

    "Health": """Health, medicine, medical research, diseases, pandemics, public health, healthcare, 
pharmaceuticals, hospitals, treatments, vaccines, mental health, nutrition.""",

    "Environment": """Environment, climate change, global warming, ecology, biodiversity, renewable energy, 
sustainability, pollution, conservation, natural disasters, environmental policy.""",

    "Society": """Society, culture, education, justice, social issues, migration, demographics, religion, 
arts, media, lifestyle, human rights, inequality, community."""
}

@lru_cache
def _get_model():
    model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    return model

@lru_cache
def _embed_categories():
    model = _get_model()
    embeddings = model.encode(list(CATEGORIES.values()))
    return embeddings

def categorize_article(title:str, summary:str|None, description:str|None) -> str:
    data = title + " " + (summary or description or "")
    model = _get_model()
    data_embedding = model.encode(data)
    categories = _embed_categories()
    similarity_matrix = util.cos_sim(data_embedding, categories)
    best_category = list(CATEGORIES.keys())[similarity_matrix.argmax().item()]
    return best_category
