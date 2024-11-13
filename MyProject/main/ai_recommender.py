from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Példaként használt külső tartalmak
sample_contents = [
    "latest technology news and updates",
    "machine learning and AI advancements",
    "top programming languages",
    "how to start in data science",
    "recent trends in artificial intelligence"
]


# Ajánló függvény
def recommend_content(user_history, sample_contents=sample_contents):
    vectorizer = TfidfVectorizer()
    all_texts = user_history + sample_contents
    vectors = vectorizer.fit_transform(all_texts)

    # Csak a felhasználói előzményeken alapuló vektorok
    user_vector = vectors[:len(user_history)]
    content_vectors = vectors[len(user_history):]

    # Hasonlóságok kiszámítása
    similarity_matrix = cosine_similarity(user_vector, content_vectors)
    avg_similarity = similarity_matrix.mean(axis=0)
    recommendations = avg_similarity.argsort()[-3:][::-1]  # Top 3 ajánlás

    # Ajánlott tartalmak visszaadása
    return [sample_contents[i] for i in recommendations]
