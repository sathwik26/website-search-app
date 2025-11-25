# backend/app.py

from flask import Flask, request, jsonify
from flask_cors import CORS

from utils.parser import html_to_chunks
from utils.vector_store import insert_chunks, search_chunks

app = Flask(__name__)
CORS(app)


@app.route("/search", methods=["POST"])
def search_api():
    try:
        data = request.get_json() or {}
        url = data.get("url", "").strip()
        query = data.get("query", "").strip()

        if not url or not query:
            return jsonify({"error": "Both url and query are required"}), 400
        chunks = html_to_chunks(url)

        if not chunks:
            return jsonify({"error": "Could not extract any content from page"}), 400

        insert_chunks(chunks)

        results = search_chunks(query)

        return jsonify({"results": results})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/")
def health():
    return "Backend running "


if __name__ == "__main__":
    app.run(port=5000, debug=True)
