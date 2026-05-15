# NYC Ride Pulse

NYC Ride Pulse is an interactive Streamlit app for exploring pickup activity across New York City and nearby airports. Use the hour slider and day-of-week filter to compare where activity concentrates, then inspect the minute-by-minute distribution for the selected window.

## Run locally

1) Create and activate a virtual environment (optional but recommended).
2) Install dependencies.
3) Start the Streamlit app.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

If you are already in an activated environment, you can skip the first two lines.

## Data

The app loads a 100k-row sample of September 2014 pickup data and will download it automatically if it is not present locally.
