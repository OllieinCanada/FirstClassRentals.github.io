import requests
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # 1. Parse the incoming JSON from Dialogflow/Vertex
    req_data = request.get_json(silent=True, force=True)
    
    # Extract user query or parameters (depending on your agent’s design)
    user_query = req_data.get("sessionInfo", {}).get("parameters", {}).get("user_query", "default query")

    # 2. Fetch the HTML from your site (example page)
    url = "https://www.firstclassrentalsniagara.ca/templates/index.html"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        # If something goes wrong fetching the site
        return jsonify({
            "fulfillment_response": {
                "messages": [
                    {"text": {"text": [
                        f"Sorry, I couldn’t fetch the data right now. Error: {str(e)}"
                    ]}}
                ]
            }
        })

    # 3. Parse the HTML (example: extract <h2> elements, etc.)
    soup = BeautifulSoup(response.text, "html.parser")
    h2_tags = soup.find_all("h2")

    # Example: Build a string of all <h2> text
    info_text = []
    for tag in h2_tags:
        info_text.append(tag.get_text(strip=True))

    # 4. Craft a response for the user
    #    (Dialogflow CX expects a "fulfillment_response" JSON structure)
    #    Adjust the JSON structure if you’re on Vertex AI’s “Conversational Agents” preview.
    combined_info = "\n".join(info_text) if info_text else "No <h2> tags found."
    reply_text = (
        f"Hi! You asked about: '{user_query}'. "
        f"Here's some info I found on the website:\n\n{combined_info}"
    )

    # Return the JSON in the format Dialogflow CX expects
    return jsonify({
        "fulfillment_response": {
            "messages": [
                {"text": {"text": [reply_text]}}
            ]
        }
    })

if __name__ == "__main__":
    # Run on port 8080 by default for GCP, or pick another
    app.run(host="0.0.0.0", port=8080, debug=True)
