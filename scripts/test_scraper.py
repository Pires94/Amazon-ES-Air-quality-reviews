import requests
import re
import sys

def get_ddg_image(query):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    # DuckDuckGo has a 'vqd' token requirement for its image API, 
    # but we can try the basic search or a simple API endpoint if it exists.
    # Alternatively, use a simpler meta-search or a known stable pattern.
    url = f"https://duckduckgo.com/html/?q={query}+image"
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            # DuckDuckGo HTML usually lists images in a simpler way
            matches = re.findall(r'https?://[^"]+\.(?:jpg|png|jpeg)', response.text)
            for m in matches:
                if "duckduckgo" not in m and "gstatic" not in m:
                    return m
        return f"Error: Status {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    query = "Levoit Core 400S Amazon ES"
    print(f"Searching DDG for: {query}")
    print(f"Result: {get_ddg_image(query)}")
