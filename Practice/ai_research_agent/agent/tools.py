import requests
import json

def web_search(query: str) -> str:
    """ 
    Searches the web for information using a free search endpoint.
    """
    print(f"  [Tool Action] Searching the web for: '{query}'...")
    try:
        url = f"https://api.duckduckgo.com/?q={requests.utils.quote(query)}&format=json"
        response = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
        data = response.json()
        
        results = []
        if data.get("AbstractText"):
            results.append(data["AbstractText"])
        
        for topic in data.get("RelatedTopics", [])[:3]:
            if "Text" in topic:
                results.append(topic["Text"])
                
        if not results:
            return f"No direct matches found for '{query}'. Try refinement."
            
        return "\n".join(results)
    except Exception as e:
        return f"Error executing web search: {str(e)}"

def text_summarizer(text: str) -> str:
    """Condenses large blocks of text."""
    print("  [Tool Action] Synthesizing and summarizing content...")
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    return " ".join(lines[:5]) + " (Summary excerpt)"

# Dictionary map containing tool metadata and execution references
AVAILABLE_TOOLS = {
    "web_search": {
        "function": web_search,
        "description": "Searches the web for real-time information based on a text query."
    },
    "text_summarizer": {
        "function": text_summarizer,
        "description": "Summarizes large text bodies to pull critical highlights."
    }
}