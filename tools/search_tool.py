from duckduckgo_search import DDGS

def web_search(query: str) -> str:
    try:
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(f"Title: {r['title']}\nURL: {r['href']}\nSummary: {r['body']}\n")
        
        if not results:
            return "Tidak ada hasil ditemukan."
        
        return "\n---\n".join(results)
    
    except Exception as e:
        return f"Error search: {str(e)}"