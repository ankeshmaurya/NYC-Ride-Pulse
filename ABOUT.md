# About NYC Ride Pulse

## Overview

NYC Ride Pulse is an interactive web application built with [Streamlit](https://streamlit.io) that visualizes real-time pickup patterns across New York City and its major transportation hubs. The app enables exploration of ride-sharing activity through dynamic geographic and temporal analysis.

## Purpose

The application helps analysts, researchers, and curious users understand:
- How pickup demand varies by hour of day
- Which days have different activity patterns
- Where transportation activity concentrates (city vs. airports)
- Minute-by-minute fluctuations during specific hours

## Key Features

### Interactive Controls
- **Hour Slider**: Select any hour (0-23) to view pickup activity for that hour and the next
- **Day Filter**: Compare activity across different days of the week or view aggregated data
- **URL Parameters**: Share specific views with `?pickup_hour=X` query string

### Visualizations
- **Multi-Panel Map View**: 
  - NYC-wide view showing all pickup activity
  - Zoomed views of La Guardia, JFK, and Newark airports
  - Hexagonal layer visualization showing pickup density
  
- **Time Series Chart**: Minute-by-minute breakdown showing pickup distribution within the selected hour

### Metrics Dashboard
- Total pickups in current view
- Number of distinct days represented
- Average pickups per day

## Data

The application uses a **100,000 row sample** of Uber pickup data from **September 2014** in New York City. The dataset includes:
- **Pickup timestamp** (date and time)
- **Latitude and longitude** coordinates
- Geographic coverage: NYC and surrounding areas including all major airports

The data is automatically downloaded on first run and cached locally for faster subsequent loads.

## Technology Stack

- **Framework**: [Streamlit](https://streamlit.io) 1.40+
- **Data Processing**: Pandas 2.0+, NumPy 1.24+
- **Visualization**: Altair 5.0+ (charts), PyDeck 0.8+ (maps)
- **Language**: Python 3.8+

## Performance

- **Caching**: Data and computations are cached to ensure fast interaction
- **Responsive**: Filters update the entire dashboard instantly
- **Lightweight**: All processing happens client-side in the browser

## Use Cases

1. **Urban Planning**: Understand transportation demand patterns
2. **Data Analysis**: Explore temporal and spatial relationships
3. **Business Intelligence**: Identify peak activity windows and locations
4. **Education**: Learn geospatial visualization techniques
5. **Demonstrations**: Show interactive analytics capabilities

## Installation & Running

See [README.md](README.md) for quick start instructions.

## Future Enhancements

Potential additions could include:
- Heatmap animations across hours
- Day-to-day comparison charts
- Statistical analysis and trend detection
- Export functionality for insights
- Real-time data integration (if available)
