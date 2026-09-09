from transformers import BartTokenizer, BartForConditionalGeneration

# Charger le tokenizer et le modèle (spécifiquement pour la génération conditionnelle)
model_name = "facebook/bart-large-cnn"
tokenizer = BartTokenizer.from_pretrained(model_name)
model = BartForConditionalGeneration.from_pretrained(model_name)

def summarize_article(article_content:str) -> str:
    # Tokenizer l'article
    inputs = tokenizer(article_content, return_tensors="pt", truncation=True, max_length=1024)

    # Générer le résumé
    summary_ids = model.generate(
        inputs.input_ids,
        max_length=120,
        min_length=30,
        do_sample=False,
        num_beams=4,
        early_stopping=True
    )

    # Décoder le résultat
    summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    return summary