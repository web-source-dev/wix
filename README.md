# Metal Price Tracker

## Overview
This application tracks and displays precious metal prices (Gold, Silver, Platinum, and Palladium) in real-time with historical price charts. It uses Streamlit for the UI and scrapes data from MetalsDaily.com with fallback to Yahoo Finance API.

## Features
- Real-time metal prices per gram
- Historical price charts for the past year
- Responsive UI with tabs for different metals
- Fallback data sources for reliability

## Deployment on Render

### Option 1: Deploy via Render Dashboard

1. Create a new account or log in to [Render](https://render.com/)
2. Click on "New +" and select "Web Service"
3. Connect your GitHub repository or upload the code directly
4. Configure the service with these settings:
   - **Name**: metal-price-tracker (or your preferred name)
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app2.py`
5. Under the "Advanced" section, add the following environment variable:
   - **PYTHON_VERSION**: 3.9.0
6. Click "Create Web Service"

### Option 2: Deploy using render.yaml

1. Push your code to a Git repository
2. Log in to [Render](https://render.com/)
3. Click on "New +" and select "Blueprint"
4. Connect your repository
5. Render will automatically detect the `render.yaml` file and set up the service

### Option 3: Deploy using Docker

1. Log in to [Render](https://render.com/)
2. Click on "New +" and select "Web Service"
3. Connect your repository
4. Select "Docker" as the environment
5. Render will automatically detect the Dockerfile and build your application

## Local Development

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the application:
   ```
   streamlit run app2.py
   ```

## Dependencies
- streamlit
- yfinance
- pandas
- matplotlib
- selenium
- webdriver-manager

## Notes
- The application requires Chrome/Chromium for web scraping
- All necessary system dependencies are included in the Dockerfile for containerized deployment
