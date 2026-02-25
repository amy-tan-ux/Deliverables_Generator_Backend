from flask import Flask, request, jsonify
from flask_cors import CORS
from OpenAIService import OpenAIService 
from Deliverable_Content import Deliverable_Content
from config import Config
Config = Config()
import os

if os.getenv("WEBSITE_SITE_NAME") is None:
    from dotenv import load_dotenv
    load_dotenv()

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(
    app,
    resources={r"/*": {"origins": "*"}},
    methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
    max_age=600
)

port = int(os.environ.get("PORT", 8000))

@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok"}), 200

OpenAI = OpenAIService()
deliverable = Deliverable_Content(OpenAI)

@app.route("/generate", methods=["POST", "OPTIONS"])
def generate():
    if request.method == "OPTIONS":
        req_headers = request.headers.get("Access-Control-Request-Headers", "*")
        return ("", 204, {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "POST, OPTIONS",
            "Access-Control-Allow-Headers": req_headers,
            "Access-Control-Max-Age": "600",
        })

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid JSON payload"}), 400

    session = data.get("session", "")
    if session != Config.get_secret("SESSION_SECRET_KEY"):
        return jsonify({"error": "Unauthorized"}), 401
    
    business_problem = data.get("business_problem", "")
    tech_stack = data.get("tech_stack", "")
    time_constraint = data.get("time_constraint", "")
    resource_constraints = data.get("resource_constraints", "")

    problem_requirements = deliverable.generate_problem_requirements(
        business_problem, tech_stack, time_constraint, resource_constraints
    )
    return jsonify({"problem_requirements": problem_requirements}), 200

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=port)
