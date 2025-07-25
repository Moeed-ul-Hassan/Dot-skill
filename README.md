# Career Roadmap Flask Backend

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the Flask app:
   ```bash
   python app.py
   ```

## Endpoints

- `POST /suggest`
  - Input: `{ "interests": ["coding", ...], "time_commitment": "part-time", "goals": ["job"] }`
  - Output: `{ "suggestions": ["Web Developer", ...] }`

- `GET /roadmap/<track>`
  - Returns roadmap steps for the given career track (e.g., `Web Developer`)

- `POST /ai-counselor` (optional)
  - Input: `{ "query": "Mujhe coding pasand hai lekin maths weak hai, kya karun?" }`
  - Output: `{ "advice": "..." }`

## Data

- Roadmap data is in `roadmap_data/roadmaps.json`.

---

You can now build a frontend (React, Streamlit, etc.) to connect to this backend! 