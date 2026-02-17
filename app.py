"""
Google Cloud Conference – 1-Day Event Website
Flask backend serving conference schedule, speakers, and search API.
"""

from flask import Flask, render_template, request, jsonify
from datetime import date

app = Flask(__name__)

# ─── Dummy Data ───────────────────────────────────────────────────────────────

CONFERENCE = {
    "name": "Google Cloud Summit 2026",
    "date": "February 10, 2026",
    "location": "Moscone Center, San Francisco, CA",
    "tagline": "One day. Eight talks. Infinite possibilities in the cloud.",
}

SPEAKERS = {
    "s1":  {"first_name": "Priya",    "last_name": "Sharma",    "linkedin": "https://www.linkedin.com/in/priyasharma"},
    "s2":  {"first_name": "James",    "last_name": "Carter",    "linkedin": "https://www.linkedin.com/in/jamescarter"},
    "s3":  {"first_name": "Mei",      "last_name": "Chen",      "linkedin": "https://www.linkedin.com/in/meichen"},
    "s4":  {"first_name": "Carlos",   "last_name": "Rivera",    "linkedin": "https://www.linkedin.com/in/carlosrivera"},
    "s5":  {"first_name": "Aisha",    "last_name": "Okafor",    "linkedin": "https://www.linkedin.com/in/aishaokafor"},
    "s6":  {"first_name": "Liam",     "last_name": "Nguyen",    "linkedin": "https://www.linkedin.com/in/liamnguyen"},
    "s7":  {"first_name": "Sofia",    "last_name": "Petrov",    "linkedin": "https://www.linkedin.com/in/sofiapetrov"},
    "s8":  {"first_name": "David",    "last_name": "Kim",       "linkedin": "https://www.linkedin.com/in/davidkim"},
    "s9":  {"first_name": "Elena",    "last_name": "Rossi",     "linkedin": "https://www.linkedin.com/in/elenarossi"},
    "s10": {"first_name": "Marcus",   "last_name": "Johnson",   "linkedin": "https://www.linkedin.com/in/marcusjohnson"},
}

TALKS = [
    {
        "id": "T1",
        "title": "Keynote: The Future of Google Cloud",
        "speakers": ["s1", "s2"],
        "category": "Cloud Strategy",
        "description": "An inspiring opening keynote exploring the latest innovations across Google Cloud Platform, from next-gen compute to AI-powered developer tools.",
        "time": "9:00 AM – 9:45 AM",
        "sort_order": 1,
    },
    {
        "id": "T2",
        "title": "Building Scalable Apps with Google Kubernetes Engine",
        "speakers": ["s3"],
        "category": "Infrastructure",
        "description": "Discover best practices for deploying, managing, and scaling containerized applications on GKE, including Autopilot mode and service mesh integration.",
        "time": "9:50 AM – 10:30 AM",
        "sort_order": 2,
    },
    {
        "id": "T3",
        "title": "Serverless Data Pipelines with Dataflow & Pub/Sub",
        "speakers": ["s4", "s5"],
        "category": "Data & Analytics",
        "description": "Learn how to build real-time and batch data processing pipelines using Apache Beam on Dataflow, integrated with Pub/Sub for event-driven architectures.",
        "time": "10:35 AM – 11:15 AM",
        "sort_order": 3,
    },
    {
        "id": "T4",
        "title": "Securing Your Cloud: IAM, VPC & Zero Trust",
        "speakers": ["s6"],
        "category": "Cloud Strategy",
        "description": "A deep dive into Google Cloud's security model — from identity-aware proxies and fine-grained IAM policies to VPC Service Controls and BeyondCorp Enterprise.",
        "time": "11:20 AM – 12:00 PM",
        "sort_order": 4,
    },
    # ── Lunch Break 12:00 PM – 1:00 PM ──
    {
        "id": "T5",
        "title": "Machine Learning at Scale with Vertex AI",
        "speakers": ["s7", "s8"],
        "category": "Data & Analytics",
        "description": "From training custom models to deploying predictions at scale, see how Vertex AI unifies the ML workflow with AutoML, custom training, and Model Garden.",
        "time": "1:00 PM – 1:45 PM",
        "sort_order": 5,
    },
    {
        "id": "T6",
        "title": "Cloud-Native Databases: Spanner, Firestore & AlloyDB",
        "speakers": ["s9"],
        "category": "Infrastructure",
        "description": "Compare Google Cloud's managed database offerings and learn when to choose Spanner's global consistency, Firestore's real-time sync, or AlloyDB's PostgreSQL compatibility.",
        "time": "1:50 PM – 2:30 PM",
        "sort_order": 6,
    },
    {
        "id": "T7",
        "title": "CI/CD on Google Cloud with Cloud Build & Artifact Registry",
        "speakers": ["s10", "s3"],
        "category": "Infrastructure",
        "description": "Automate your entire release pipeline — from source to production — using Cloud Build triggers, Artifact Registry for container images, and Cloud Deploy for GKE.",
        "time": "2:35 PM – 3:15 PM",
        "sort_order": 7,
    },
    {
        "id": "T8",
        "title": "Closing Panel: Multi-Cloud, Sustainability & What's Next",
        "speakers": ["s1", "s5"],
        "category": "Cloud Strategy",
        "description": "Industry leaders discuss multi-cloud strategies, Google's carbon-intelligent computing initiatives, and predictions for the next wave of cloud technology.",
        "time": "3:20 PM – 4:00 PM",
        "sort_order": 8,
    },
]

CATEGORIES = sorted({t["category"] for t in TALKS})


def _enrich_talk(talk: dict) -> dict:
    """Attach full speaker objects to a talk dict."""
    enriched = dict(talk)
    enriched["speaker_details"] = [SPEAKERS[sid] for sid in talk["speakers"]]
    return enriched


def _matches(talk: dict, query: str, category: str) -> bool:
    """Return True if a talk matches the search filters."""
    if category and talk["category"] != category:
        return False
    if query:
        q = query.lower()
        # Search in title
        if q in talk["title"].lower():
            return True
        # Search in speaker names
        for sid in talk["speakers"]:
            sp = SPEAKERS[sid]
            full_name = f"{sp['first_name']} {sp['last_name']}".lower()
            if q in full_name:
                return True
        # Search in description
        if q in talk["description"].lower():
            return True
        return False
    return True


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    enriched_talks = [_enrich_talk(t) for t in TALKS]
    return render_template(
        "index.html",
        conference=CONFERENCE,
        talks=enriched_talks,
        categories=CATEGORIES,
    )


@app.route("/api/talks")
def api_talks():
    query = request.args.get("q", "").strip()
    category = request.args.get("category", "").strip()
    filtered = [_enrich_talk(t) for t in TALKS if _matches(t, query, category)]
    return jsonify(filtered)


# ─── Entry Point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(debug=True, port=5000)
