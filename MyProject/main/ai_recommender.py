import os
import requests
from dotenv import load_dotenv

# Környezeti változók betöltése
load_dotenv()

# YouTube API kulcs betöltése
API_KEY = os.getenv("YOUTUBE_API_KEY")


def fetch_youtube_recommendations(query):
    """
    YouTube keresési eredmények lekérése egy adott kulcsszóra.
    """
    base_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "maxResults": 5,  # Max 5 ajánlás
        "q": query,
        "type": "video",
        "key": API_KEY,
    }

    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Hibák kezelése
        data = response.json()

        # Videók linkjeinek kinyerése
        recommendations = []
        for item in data.get("items", []):
            video_id = item["id"]["videoId"]
            video_title = item["snippet"]["title"]
            recommendations.append({
                "title": video_title,
                "url": f"https://www.youtube.com/watch?v={video_id}",
            })
        return recommendations
    except requests.exceptions.RequestException as e:
        print(f"YouTube API error: {e}")
        return []


def recommend_content(urls):
    """
    Keresési előzmények alapján ajánlások generálása.
    """
    # Témák az URL-ek alapján
    topics = {
        "programming": ["python", "java", "c++", "programming"],
        "news": ["news", "bbc", "cnn", "politics"],
        "shopping": ["shop", "amazon", "ebay"],
        "videos": ["youtube", "vimeo"],
    }

    user_interests = {
        "programming": False,
        "news": False,
        "shopping": False,
        "videos": False,
    }

    for url in urls:
        for topic, keywords in topics.items():
            if any(keyword in url.lower() for keyword in keywords):
                user_interests[topic] = True

    # Ajánlások összegyűjtése
    recommendations = {}
    if user_interests["programming"]:
        recommendations["Programming Videos"] = fetch_youtube_recommendations("programming tutorials")
    if user_interests["news"]:
        recommendations["News Updates"] = fetch_youtube_recommendations("latest news")
    if user_interests["shopping"]:
        recommendations["Shopping Deals"] = fetch_youtube_recommendations("shopping deals")
    if user_interests["videos"]:
        recommendations["Popular Videos"] = fetch_youtube_recommendations("popular videos")

    return recommendations
