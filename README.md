# Google Cloud Summit 2026 – Conference Website

A one-day technical conference informational site built with **Python / Flask** and vanilla **HTML, CSS, JavaScript**.

![Python](https://img.shields.io/badge/Python-3.8+-blue) ![Flask](https://img.shields.io/badge/Flask-3.x-green)

---

## Features

| Feature | Description |
|---|---|
| **Schedule Timeline** | 8 talks displayed in a visual timeline with a 60-minute lunch break |
| **Search** | Live search by talk title, speaker name, or keyword |
| **Category Filter** | Dropdown filter for *Cloud Strategy*, *Data & Analytics*, *Infrastructure* |
| **Speaker Profiles** | Each speaker links to their LinkedIn profile |
| **Theme Toggle** | Switch between **Light**, **Dark**, and **AMOLED** (Pure Black) modes |
| **Responsive** | Mobile-friendly layout with a sticky search bar |

---

## Prerequisites

- **Python 3.8+** installed and available on `PATH`
- **pip** (comes with Python)

---

## Quick Start

```bash
# 1. Clone / navigate to the project directory
cd spinning-orion

# 2. Create a virtual environment (recommended)
python -m venv venv
# Windows
venv\Scripts\activate
# macOS / Linux
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the Flask dev server
python app.py
```

Open **http://localhost:5000** in your browser.

---

## Project Structure

```
spinning-orion/
├── app.py               # Flask application (routes, data, API)
├── requirements.txt     # Python dependencies
├── README.md            # This file
├── static/
│   ├── style.css        # All styles (dark theme, timeline, responsive)
│   └── app.js           # Client-side search & filter logic
└── templates/
    └── index.html       # Jinja2 template (hero, schedule, footer)
```

---

## How to Modify

### Add / Edit Talks

Open `app.py` and edit the `TALKS` list. Each talk is a dictionary:

```python
{
    "id": "T9",
    "title": "Your New Talk Title",
    "speakers": ["s1"],           # references keys in SPEAKERS dict
    "category": "Infrastructure", # must match an existing category or add a new one
    "description": "Talk description here.",
    "time": "4:05 PM – 4:45 PM",
    "sort_order": 9,
}
```

### Add / Edit Speakers

Edit the `SPEAKERS` dictionary in `app.py`:

```python
"s11": {
    "first_name": "New",
    "last_name": "Speaker",
    "linkedin": "https://www.linkedin.com/in/newspeaker"
}
```

### Change Conference Details

Update the `CONFERENCE` dictionary at the top of `app.py` (name, date, location, tagline).

### Styling

All styles live in `static/style.css`. The Google Cloud colour palette is defined as CSS custom properties in `:root`.

---

## API

| Endpoint | Method | Params | Description |
|---|---|---|---|
| `/` | GET | — | Renders the full HTML page |
| `/api/talks` | GET | `q` (search query), `category` | Returns filtered talks as JSON |

---

## License

This project is provided as-is for demonstration purposes.
