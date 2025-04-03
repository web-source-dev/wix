import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from io import BytesIO
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Configure matplotlib for headless environment
plt.switch_backend('Agg')

# Set page config
st.set_page_config(
    page_title="Metal Price Tracker",
    page_icon="💰",
    layout="wide"
)

def setup_driver():
    """Configure ChromeDriver for Streamlit Cloud"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")  # Essential for cloud
    chrome_options.add_argument("--disable-dev-shm-usage")  # Essential for cloud
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920x1080")
    
    # Set path to chromedriver based on environment
    if os.path.exists("/usr/bin/chromedriver"):  # Render path
        service = Service("/usr/bin/chromedriver")
    elif os.path.exists("/app/.apt/usr/bin/chromedriver"):  # Streamlit Cloud path
        service = Service("/app/.apt/usr/bin/chromedriver")
    else:
        service = Service()  # Local development
    
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def get_metal_prices():
    """Scrape metal prices with robust error handling"""
    driver = setup_driver()
    try:
        url = "https://www.metalsdaily.com/live-prices/pgms/"
        driver.get(url)
        
        # Wait for table to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "table"))
        )
        
        rows = driver.find_elements(By.TAG_NAME, "tr")
        metal_prices = {}

        for row in rows:
            cols = row.find_elements(By.TAG_NAME, "td")
            if len(cols) > 2:
                metal = cols[0].text.strip()
                ask_price = cols[2].text.strip()
                
                if "USD/OZ" in metal:
                    metal_name = metal.replace("USD/OZ", "").strip()
                    try:
                        metal_prices[metal_name] = float(ask_price.replace(',', '')) / 28
                    except ValueError:
                        continue
        
        return metal_prices
    except Exception as e:
        st.warning(f"Couldn't fetch live prices: {str(e)}")
        return {}
    finally:
        driver.quit()

def get_metal_data(symbol, period="1y"):
    """Get historical metal price data from Yahoo Finance"""
    try:
        data = yf.download(symbol, period=period, progress=False)
        if data.empty:
            return pd.DataFrame()
        return data
    except Exception as e:
        st.warning(f"Error fetching historical data: {str(e)}")
        return pd.DataFrame()

def plot_metal_chart(data, metal_name):
    """Create a chart for metal price trends"""
    if data.empty:
        return None
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data.index, data['Close'], linewidth=2)
    ax.set_title(f'{metal_name} Price - Last Year', fontsize=16)
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Price (USD/oz)', fontsize=12)
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    
    return fig

# Main app
st.title("📊 Precious Metal Price Tracker")
st.markdown("### Live Prices and Historical Trends")

# Get live prices
with st.spinner("Fetching live metal prices..."):
    metal_prices = get_metal_prices()

# Display live prices
st.subheader("Current Prices (USD per gram)")
col1, col2, col3, col4 = st.columns(4)

# Fallback to Yahoo Finance if scraping fails
if not metal_prices.get("Gold"):
    gold_data = get_metal_data("GC=F")
    if not gold_data.empty:
        metal_prices["Gold"] = gold_data['Close'].iloc[-1] / 28

if not metal_prices.get("Silver"):
    silver_data = get_metal_data("SI=F")
    if not silver_data.empty:
        metal_prices["Silver"] = silver_data['Close'].iloc[-1] / 28

if not metal_prices.get("Platinum"):
    platinum_data = get_metal_data("PL=F")
    if not platinum_data.empty:
        metal_prices["Platinum"] = platinum_data['Close'].iloc[-1] / 28

if not metal_prices.get("Palladium"):
    palladium_data = get_metal_data("PA=F")
    if not palladium_data.empty:
        metal_prices["Palladium"] = palladium_data['Close'].iloc[-1] / 28

# Display prices in columns
with col1:
    st.metric("Gold", f"${metal_prices.get('Gold', 0):.2f}")

with col2:
    st.metric("Silver", f"${metal_prices.get('Silver', 0):.2f}")

with col3:
    st.metric("Platinum", f"${metal_prices.get('Platinum', 0):.2f}")

with col4:
    st.metric("Palladium", f"${metal_prices.get('Palladium', 0):.2f}")

# Historical data section
st.subheader("Historical Price Charts")

tab1, tab2, tab3, tab4 = st.tabs(["Gold", "Silver", "Platinum", "Palladium"])

with tab1:
    gold_hist = get_metal_data("GC=F")
    if not gold_hist.empty:
        st.pyplot(plot_metal_chart(gold_hist, "Gold"))
    else:
        st.info("Gold historical data not available")

with tab2:
    silver_hist = get_metal_data("SI=F")
    if not silver_hist.empty:
        st.pyplot(plot_metal_chart(silver_hist, "Silver"))
    else:
        st.info("Silver historical data not available")

with tab3:
    platinum_hist = get_metal_data("PL=F")
    if not platinum_hist.empty:
        st.pyplot(plot_metal_chart(platinum_hist, "Platinum"))
    else:
        st.info("Platinum historical data not available")

with tab4:
    palladium_hist = get_metal_data("PA=F")
    if not palladium_hist.empty:
        st.pyplot(plot_metal_chart(palladium_hist, "Palladium"))
    else:
        st.info("Palladium historical data not available")

# Footer
st.markdown("---")
st.caption("Data sources: MetalsDaily.com and Yahoo Finance")
