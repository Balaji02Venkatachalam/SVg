# NOVA-C — Narrative Output from Visual Analytics – Charts

An AI-powered SVG chart analysis tool that extracts data from SVG charts, detects trends and anomalies, and generates analyst-quality narratives using Google Gemini.

## Features

- **SVG Chart Parsing** — Supports multiple SVG formats (legacy and generated charts)
- **Auto Chart Type Detection** — Line, area, bar, dual-tone, log-scale
- **Trend Engine** — Detects rising/falling/flat regimes, peaks, troughs, anomalies
- **AI Narratives** — Generates Bloomberg-style commentary via Google Gemini
- **Chatbot** — Ask questions about your chart data using AI
- **News Integration** — Fetches relevant news headlines via Google News RSS
- **ML Forecasting** — Time-series prediction with multiple models (Linear, Ridge, Lasso, SVR, Random Forest, GB, MLP, LSTM)
- **Interactive Dashboard** — Dark-themed UI with Chart.js, drag-drop upload, hover tooltips

## Prerequisites

- Python 3.10+
- A Google Gemini API key (free tier available)

## Setup

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd codezilla
```

### 2. Install Python dependencies

```bash
pip install -r backend/requirements.txt
```

### 3. Get a Google Gemini API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key

### 4. Set the API key as an environment variable

**Windows (PowerShell):**
```powershell
$env:GEMINI_API_KEY = "your-gemini-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GEMINI_API_KEY=your-gemini-api-key-here
```

**Linux / macOS:**
```bash
export GEMINI_API_KEY="your-gemini-api-key-here"
```

To make it permanent, add the above line to your shell profile (`~/.bashrc`, `~/.zshrc`, etc.) or set it in Windows System Environment Variables.

### 5. (Optional) Choose a different Gemini model

By default, the app uses `gemini-2.0-flash`. You can change it:

```powershell
$env:GEMINI_MODEL = "gemini-2.0-flash"
```

Available models: `gemini-2.0-flash`, `gemini-1.5-flash`, `gemini-1.5-pro`, etc.

### 6. Start the server

```bash
cd codezilla
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Then open: **http://127.0.0.1:8000**

## Usage

1. **Sign up / Log in** using any email and password
2. **Upload an SVG chart** or click **Load Demo Charts** to analyze the bundled charts
3. View the extracted data, trends, anomalies, and AI-generated narrative
4. Use the **Chatbot** to ask questions about the chart
5. Use the **Predictions** panel to forecast future values with ML models
6. Select a time range on the chart to get news context for that period

## Project Structure

```
codezilla/
├── backend/
│   ├── requirements.txt
│   └── app/
│       ├── main.py              # FastAPI routes & endpoints
│       ├── models/
│       │   └── schemas.py       # Pydantic data models
│       ├── routers/
│       │   └── auth.py          # Authentication routes
│       ├── services/
│       │   ├── auth.py          # JWT auth service
│       │   ├── svg_parser.py    # SVG parsing (multi-format)
│       │   ├── axis_calibrator.py # Pixel-to-value calibration
│       │   ├── trend_engine.py  # Trend/anomaly detection
│       │   ├── llm_narrator.py  # Google Gemini integration
│       │   ├── news_search.py   # Google News RSS scraping
│       │   └── predictor.py     # ML forecasting models
│       └── static/
│           └── index.html       # Frontend dashboard
├── Chart SVGs/                  # Demo chart files
│   ├── *.svg                    # Legacy format SVGs
│   └── copy/                    # Generated format SVGs
│       └── *.svg
├── users.json                   # Local user database
└── README.md
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GEMINI_API_KEY` | **Yes** | _(empty)_ | Your Google Gemini API key |
| `GEMINI_MODEL` | No | `gemini-2.0-flash` | Gemini model to use |
| `JWT_SECRET` | No | _(built-in default)_ | Secret for JWT token signing |

## Supported SVG Formats

The parser auto-detects and handles two SVG formats:

- **Format A (Legacy):** Uses `.s0`/`.s4`/`.s5` CSS classes, clip-path groups, `rotate(360)` transforms
- **Format B (Generated):** Uses `.title`/`.subtitle`/`.y-tick-label`/`.tick-label` CSS classes, flat structure with inline stroke attributes

Both uploaded SVGs and demo SVGs from either format work seamlessly.

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/signup` | Register a new user |
| POST | `/api/auth/login` | Sign in |
| POST | `/api/upload` | Upload and analyze an SVG chart |
| POST | `/api/narrative` | Regenerate narrative with different tone |
| POST | `/api/compare` | Compare multiple charts |
| POST | `/api/chat` | Chat with AI about chart data |
| POST | `/api/predict` | ML time-series forecasting |
| POST | `/api/range-analysis` | News summary for a time range |
| GET | `/api/demo` | Load all demo charts |
| GET | `/api/charts` | List analyzed charts |
| GET | `/api/charts/{id}` | Get specific chart analysis |
| GET | `/api/health` | Health check |
