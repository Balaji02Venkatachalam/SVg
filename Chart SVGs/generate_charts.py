import random
import math
import os

random.seed(42)

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "copy")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Color palettes ---
COLORS = [
    "#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261",
    "#264653", "#6A0572", "#AB83A1", "#1D3557", "#A8DADC",
    "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#FFEAA7",
    "#DFE6E9", "#74B9FF", "#A29BFE", "#FD79A8", "#00B894",
]

CHART_STYLES = """
  <defs>
   <style type="text/css">
    .bg {{ fill: #FFFFFF; }}
    .title {{ font-family: Arial, sans-serif; font-size: 22px; font-weight: bold; fill: #333333; }}
    .subtitle {{ font-family: Arial, sans-serif; font-size: 14px; fill: #666666; }}
    .axis-line {{ stroke: #CCCCCC; stroke-width: 1; fill: none; }}
    .axis-line-bold {{ stroke: #999999; stroke-width: 1.5; fill: none; }}
    .tick-label {{ font-family: Arial, sans-serif; font-size: 12px; fill: #666666; text-anchor: middle; }}
    .y-tick-label {{ font-family: Arial, sans-serif; font-size: 12px; fill: #666666; text-anchor: end; }}
    .bar-label {{ font-family: Arial, sans-serif; font-size: 11px; fill: #333333; text-anchor: end; }}
    .legend-text {{ font-family: Arial, sans-serif; font-size: 11px; fill: #333333; }}
    .source-text {{ font-family: Arial, sans-serif; font-size: 10px; fill: #999999; }}
   </style>
  </defs>
"""

# ========== CHART DEFINITIONS (100 charts) ==========

def gen_line_data(n, base, volatility, trend=0):
    data = []
    v = base
    for i in range(n):
        v += trend + random.gauss(0, volatility)
        v = max(v, base * 0.1)
        data.append(v)
    return data

def gen_bar_data(n, low, high):
    return sorted([random.uniform(low, high) for _ in range(n)], reverse=True)

# Chart definitions
CHARTS = [
    # --- TYPE 1: SIMPLE LINE CHARTS (charts 1-15) ---
    {"id": 1, "type": "line", "title": "US GDP Growth Rate", "subtitle": "Annual percentage change", "years": list(range(2000, 2026)), "series": [{"name": "GDP Growth", "color": "#E63946", "data": [4.1, 1.0, 1.7, 2.9, 3.8, 3.5, 2.9, 1.9, -0.1, -2.5, 2.6, 1.6, 2.2, 1.8, 2.5, 3.1, 1.7, 2.4, 3.0, 2.2, -3.4, 5.9, 2.1, 2.5, 2.8, 2.3]}]},
    {"id": 2, "type": "line", "title": "UK Inflation Rate (CPI)", "subtitle": "Per cent, year-on-year", "years": list(range(2010, 2026)), "series": [{"name": "CPI", "color": "#457B9D", "data": [3.3, 4.5, 2.8, 2.6, 1.5, 0.0, 0.7, 2.7, 2.5, 1.8, 0.9, 2.6, 9.1, 7.3, 4.0, 2.8]}]},
    {"id": 3, "type": "line", "title": "Japan Interest Rate", "subtitle": "Bank of Japan policy rate, per cent", "years": list(range(2010, 2026)), "series": [{"name": "Policy Rate", "color": "#2A9D8F", "data": [0.1, 0.1, 0.1, 0.1, 0.1, 0.0, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0.25, 0.5]}]},
    {"id": 4, "type": "line", "title": "Euro Area Unemployment Rate", "subtitle": "Per cent of labour force", "years": list(range(2010, 2026)), "series": [{"name": "Unemployment", "color": "#E9C46A", "data": [10.2, 10.2, 11.4, 12.0, 11.6, 10.9, 10.0, 9.1, 8.2, 7.6, 7.9, 7.7, 6.7, 6.5, 6.4, 6.2]}]},
    {"id": 5, "type": "line", "title": "India GDP Growth Rate", "subtitle": "Annual percentage change", "years": list(range(2010, 2026)), "series": [{"name": "GDP Growth", "color": "#F4A261", "data": [8.5, 5.2, 5.5, 6.4, 7.4, 8.0, 8.3, 6.8, 6.5, 3.9, -5.8, 9.1, 7.2, 7.8, 7.0, 6.5]}]},
    {"id": 6, "type": "line", "title": "Brazil Selic Interest Rate", "subtitle": "Per cent per annum", "years": list(range(2015, 2026)), "series": [{"name": "Selic Rate", "color": "#264653", "data": [14.25, 13.75, 7.0, 6.5, 4.5, 2.0, 9.25, 13.75, 13.25, 10.5, 12.25]}]},
    {"id": 7, "type": "line", "title": "Australia House Price Index", "subtitle": "Index, 2010 = 100", "years": list(range(2010, 2026)), "series": [{"name": "House Prices", "color": "#6A0572", "data": [100, 99, 98, 107, 117, 127, 137, 150, 157, 161, 170, 192, 207, 200, 210, 218]}]},
    {"id": 8, "type": "line", "title": "South Korea Export Growth", "subtitle": "Year-on-year percentage change", "years": list(range(2015, 2026)), "series": [{"name": "Export Growth", "color": "#1D3557", "data": [-8.0, -5.9, 15.8, 5.4, -10.4, -5.5, 25.7, 6.1, -7.4, 9.3, 8.5]}]},
    {"id": 9, "type": "line", "title": "Canada Housing Starts", "subtitle": "Thousands of units, annualized", "years": list(range(2015, 2026)), "series": [{"name": "Housing Starts", "color": "#A8DADC", "data": [196, 198, 220, 213, 209, 217, 271, 262, 240, 245, 238]}]},
    {"id": 10, "type": "line", "title": "Mexico Remittances", "subtitle": "USD billions", "years": list(range(2015, 2026)), "series": [{"name": "Remittances", "color": "#FF6B6B", "data": [24.8, 26.9, 30.0, 33.5, 36.0, 40.6, 51.6, 58.5, 63.3, 64.7, 62.0]}]},
    {"id": 11, "type": "line", "title": "Nigeria Crude Oil Production", "subtitle": "Million barrels per day", "years": list(range(2015, 2026)), "series": [{"name": "Production", "color": "#4ECDC4", "data": [2.11, 1.83, 1.86, 1.93, 2.00, 1.57, 1.37, 1.21, 1.42, 1.55, 1.63]}]},
    {"id": 12, "type": "line", "title": "Switzerland Consumer Confidence", "subtitle": "Index", "years": list(range(2015, 2026)), "series": [{"name": "Confidence", "color": "#45B7D1", "data": [-6, -15, -10, -5, -4, -12, -28, -15, -27, -30, -22]}]},
    {"id": 13, "type": "line", "title": "Singapore GDP per Capita", "subtitle": "USD thousands", "years": list(range(2015, 2026)), "series": [{"name": "GDP per Capita", "color": "#96CEB4", "data": [56.3, 57.2, 60.4, 64.6, 65.6, 60.7, 72.8, 82.8, 84.7, 88.4, 91.2]}]},
    {"id": 14, "type": "line", "title": "New Zealand Tourism Arrivals", "subtitle": "Millions of visitors", "years": list(range(2015, 2026)), "series": [{"name": "Arrivals", "color": "#FFEAA7", "data": [3.1, 3.5, 3.7, 3.8, 3.9, 1.1, 0.3, 1.4, 3.2, 3.5, 3.6]}]},
    {"id": 15, "type": "line", "title": "Taiwan Semiconductor Revenue", "subtitle": "USD billions", "years": list(range(2015, 2026)), "series": [{"name": "Revenue", "color": "#74B9FF", "data": [36.5, 34.2, 37.0, 38.5, 35.8, 47.6, 56.8, 75.9, 69.3, 87.5, 95.0]}]},

    # --- TYPE 2: MULTI-LINE CHARTS (charts 16-30) ---
    {"id": 16, "type": "multiline", "title": "CO2 Emissions by Country", "subtitle": "Billion metric tons", "years": list(range(2010, 2026)), "series": [
        {"name": "China", "color": "#E63946", "data": [8.5, 9.2, 9.5, 9.8, 9.9, 9.8, 9.7, 10.0, 10.3, 10.5, 10.7, 11.5, 12.1, 12.6, 13.0, 13.3]},
        {"name": "USA", "color": "#457B9D", "data": [5.4, 5.3, 5.1, 5.3, 5.3, 5.2, 5.1, 5.1, 5.3, 5.1, 4.6, 5.0, 5.0, 4.9, 4.8, 4.7]},
        {"name": "India", "color": "#2A9D8F", "data": [1.7, 1.8, 2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.6, 2.4, 2.7, 2.8, 3.0, 3.1, 3.0]},
        {"name": "EU", "color": "#E9C46A", "data": [3.6, 3.5, 3.4, 3.2, 3.1, 3.1, 3.1, 3.2, 3.0, 2.8, 2.6, 2.7, 2.7, 2.6, 2.5, 2.5]},
    ]},
    {"id": 17, "type": "multiline", "title": "Global Smartphone Shipments", "subtitle": "Units, millions, by manufacturer", "years": list(range(2018, 2026)), "series": [
        {"name": "Samsung", "color": "#1D3557", "data": [292, 296, 267, 272, 261, 227, 226, 234]},
        {"name": "Apple", "color": "#A8DADC", "data": [218, 198, 206, 236, 232, 234, 232, 240]},
        {"name": "Xiaomi", "color": "#FF6B6B", "data": [122, 126, 149, 191, 153, 146, 169, 175]},
        {"name": "Others", "color": "#96CEB4", "data": [748, 752, 670, 650, 580, 560, 545, 530]},
    ]},
    {"id": 18, "type": "multiline", "title": "Renewable Energy Capacity", "subtitle": "Gigawatts, by source", "years": list(range(2015, 2026)), "series": [
        {"name": "Solar", "color": "#E9C46A", "data": [227, 303, 398, 486, 580, 714, 843, 1047, 1346, 1700, 2050]},
        {"name": "Wind", "color": "#457B9D", "data": [432, 487, 539, 591, 651, 743, 825, 899, 1012, 1120, 1230]},
        {"name": "Hydro", "color": "#2A9D8F", "data": [1064, 1096, 1114, 1132, 1150, 1170, 1197, 1230, 1250, 1270, 1290]},
    ]},
    {"id": 19, "type": "multiline", "title": "Global EV Sales by Region", "subtitle": "Millions of units", "years": list(range(2018, 2026)), "series": [
        {"name": "China", "color": "#E63946", "data": [1.1, 1.2, 1.3, 3.3, 5.9, 8.1, 8.9, 10.2]},
        {"name": "Europe", "color": "#457B9D", "data": [0.4, 0.6, 1.4, 2.3, 2.7, 3.2, 3.5, 3.8]},
        {"name": "USA", "color": "#2A9D8F", "data": [0.4, 0.3, 0.3, 0.6, 0.8, 1.4, 1.8, 2.1]},
        {"name": "Rest of World", "color": "#E9C46A", "data": [0.2, 0.2, 0.2, 0.4, 0.6, 0.9, 1.3, 1.6]},
    ]},
    {"id": 20, "type": "multiline", "title": "Central Bank Policy Rates", "subtitle": "Per cent", "years": list(range(2018, 2026)), "series": [
        {"name": "US Fed", "color": "#E63946", "data": [2.5, 1.75, 0.25, 0.25, 4.5, 5.5, 5.25, 4.5]},
        {"name": "ECB", "color": "#457B9D", "data": [0.0, 0.0, 0.0, 0.0, 2.5, 4.5, 4.0, 3.0]},
        {"name": "BoE", "color": "#2A9D8F", "data": [0.75, 0.75, 0.1, 0.25, 3.5, 5.25, 5.0, 4.5]},
        {"name": "BoJ", "color": "#E9C46A", "data": [-0.1, -0.1, -0.1, -0.1, -0.1, -0.1, 0.25, 0.5]},
    ]},
    {"id": 21, "type": "multiline", "title": "Global Steel Production", "subtitle": "Million metric tons, by country", "years": list(range(2015, 2026)), "series": [
        {"name": "China", "color": "#E63946", "data": [804, 808, 832, 928, 996, 1065, 1033, 1018, 1019, 1005, 990]},
        {"name": "India", "color": "#2A9D8F", "data": [89, 96, 101, 109, 111, 100, 118, 125, 140, 148, 155]},
        {"name": "Japan", "color": "#E9C46A", "data": [105, 105, 105, 104, 99, 83, 96, 89, 87, 85, 84]},
    ]},
    {"id": 22, "type": "multiline", "title": "Internet Users by Region", "subtitle": "Billions", "years": list(range(2015, 2026)), "series": [
        {"name": "Asia", "color": "#E63946", "data": [1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.1, 3.2, 3.3]},
        {"name": "Europe", "color": "#457B9D", "data": [0.6, 0.62, 0.64, 0.66, 0.67, 0.69, 0.70, 0.71, 0.72, 0.72, 0.73]},
        {"name": "Americas", "color": "#2A9D8F", "data": [0.6, 0.63, 0.66, 0.68, 0.70, 0.72, 0.74, 0.76, 0.77, 0.78, 0.79]},
        {"name": "Africa", "color": "#F4A261", "data": [0.22, 0.26, 0.32, 0.37, 0.42, 0.48, 0.54, 0.60, 0.66, 0.72, 0.78]},
    ]},
    {"id": 23, "type": "multiline", "title": "Gold Price vs Silver Price", "subtitle": "Index, 2015 = 100", "years": list(range(2015, 2026)), "series": [
        {"name": "Gold", "color": "#E9C46A", "data": [100, 106, 110, 108, 120, 153, 154, 155, 169, 204, 250]},
        {"name": "Silver", "color": "#A8DADC", "data": [100, 105, 109, 96, 97, 128, 155, 133, 147, 183, 210]},
    ]},
    {"id": 24, "type": "multiline", "title": "Air Passenger Traffic by Region", "subtitle": "Billion passenger-kilometres", "years": list(range(2015, 2026)), "series": [
        {"name": "Asia Pacific", "color": "#E63946", "data": [2.4, 2.6, 2.8, 3.1, 3.2, 1.0, 0.4, 1.8, 3.1, 3.4, 3.6]},
        {"name": "Europe", "color": "#457B9D", "data": [1.8, 1.9, 2.0, 2.1, 2.2, 0.7, 0.4, 1.5, 2.1, 2.3, 2.4]},
        {"name": "North America", "color": "#2A9D8F", "data": [1.6, 1.7, 1.8, 1.9, 1.9, 0.7, 0.5, 1.5, 1.8, 2.0, 2.0]},
    ]},
    {"id": 25, "type": "multiline", "title": "Global Food Price Indices", "subtitle": "Index, 2014-2016 = 100", "years": list(range(2015, 2026)), "series": [
        {"name": "Cereals", "color": "#E9C46A", "data": [96, 86, 88, 95, 98, 107, 128, 150, 130, 118, 115]},
        {"name": "Meat", "color": "#E63946", "data": [102, 85, 92, 93, 99, 96, 107, 118, 117, 113, 110]},
        {"name": "Dairy", "color": "#457B9D", "data": [95, 73, 91, 108, 101, 105, 119, 142, 119, 115, 112]},
        {"name": "Oils", "color": "#2A9D8F", "data": [97, 86, 95, 93, 87, 100, 164, 178, 128, 122, 118]},
    ]},
    {"id": 26, "type": "multiline", "title": "Lithium Carbonate vs Cobalt Price", "subtitle": "USD per metric ton, thousands", "years": list(range(2018, 2026)), "series": [
        {"name": "Lithium", "color": "#6A0572", "data": [16, 8, 7, 18, 70, 75, 15, 12]},
        {"name": "Cobalt", "color": "#457B9D", "data": [80, 33, 30, 50, 72, 35, 28, 30]},
    ]},
    {"id": 27, "type": "multiline", "title": "Container Shipping Rates", "subtitle": "USD per 40-foot container, by route", "years": list(range(2018, 2026)), "series": [
        {"name": "Shanghai-Rotterdam", "color": "#E63946", "data": [1800, 1500, 4500, 10000, 6500, 1500, 4200, 2800]},
        {"name": "Shanghai-LA", "color": "#457B9D", "data": [1600, 1400, 4000, 9500, 5000, 1400, 3800, 2500]},
        {"name": "Shanghai-NY", "color": "#2A9D8F", "data": [2500, 2200, 6000, 12000, 7500, 2000, 5500, 3500]},
    ]},
    {"id": 28, "type": "multiline", "title": "Social Media Monthly Active Users", "subtitle": "Billions", "years": list(range(2018, 2026)), "series": [
        {"name": "Facebook", "color": "#457B9D", "data": [2.32, 2.50, 2.80, 2.91, 2.96, 3.05, 3.07, 3.10]},
        {"name": "YouTube", "color": "#E63946", "data": [1.90, 2.00, 2.29, 2.56, 2.68, 2.70, 2.73, 2.75]},
        {"name": "Instagram", "color": "#F4A261", "data": [1.00, 1.00, 1.22, 1.39, 1.48, 2.00, 2.30, 2.50]},
        {"name": "TikTok", "color": "#2A9D8F", "data": [0.27, 0.50, 0.69, 1.00, 1.05, 1.22, 1.58, 1.80]},
    ]},
    {"id": 29, "type": "multiline", "title": "Global Copper vs Aluminium Prices", "subtitle": "USD per metric ton", "years": list(range(2015, 2026)), "series": [
        {"name": "Copper", "color": "#E63946", "data": [5510, 4868, 6170, 6530, 6010, 6181, 9317, 8822, 8479, 9200, 9600]},
        {"name": "Aluminium", "color": "#457B9D", "data": [1665, 1604, 1968, 2110, 1794, 1704, 2480, 2704, 2256, 2400, 2550]},
    ]},
    {"id": 30, "type": "multiline", "title": "Global Wheat vs Corn Production", "subtitle": "Million metric tons", "years": list(range(2015, 2026)), "series": [
        {"name": "Wheat", "color": "#E9C46A", "data": [734, 750, 760, 731, 765, 774, 779, 781, 783, 790, 795]},
        {"name": "Corn", "color": "#2A9D8F", "data": [976, 1069, 1076, 1100, 1120, 1123, 1210, 1162, 1230, 1225, 1240]},
    ]},

    # --- TYPE 3: STACKED AREA CHARTS (charts 31-45) ---
    {"id": 31, "type": "area", "title": "Global Energy Consumption by Source", "subtitle": "Exajoules", "years": list(range(2010, 2026)), "series": [
        {"name": "Oil", "color": "#E63946", "data": [170, 174, 176, 179, 181, 184, 186, 189, 191, 188, 175, 185, 188, 190, 192, 193]},
        {"name": "Gas", "color": "#457B9D", "data": [114, 118, 120, 122, 124, 126, 129, 133, 137, 141, 137, 145, 147, 148, 150, 152]},
        {"name": "Coal", "color": "#666666", "data": [152, 156, 155, 157, 159, 156, 152, 153, 157, 157, 152, 159, 161, 158, 155, 153]},
        {"name": "Renewables", "color": "#2A9D8F", "data": [20, 22, 25, 28, 31, 35, 39, 43, 48, 52, 54, 60, 68, 76, 85, 95]},
    ]},
    {"id": 32, "type": "area", "title": "World Population by Continent", "subtitle": "Billions", "years": list(range(2000, 2025, 5)), "series": [
        {"name": "Asia", "color": "#E63946", "data": [3.7, 3.9, 4.2, 4.4, 4.6]},
        {"name": "Africa", "color": "#F4A261", "data": [0.8, 0.9, 1.0, 1.2, 1.4]},
        {"name": "Europe", "color": "#457B9D", "data": [0.73, 0.73, 0.74, 0.74, 0.74]},
        {"name": "Americas", "color": "#2A9D8F", "data": [0.84, 0.89, 0.94, 0.98, 1.02]},
        {"name": "Oceania", "color": "#E9C46A", "data": [0.03, 0.03, 0.04, 0.04, 0.04]},
    ]},
    {"id": 33, "type": "area", "title": "US Federal Budget by Category", "subtitle": "USD trillions", "years": list(range(2018, 2026)), "series": [
        {"name": "Social Security", "color": "#E63946", "data": [0.98, 1.04, 1.10, 1.13, 1.22, 1.35, 1.40, 1.46]},
        {"name": "Healthcare", "color": "#457B9D", "data": [1.10, 1.15, 1.37, 1.48, 1.41, 1.52, 1.60, 1.65]},
        {"name": "Defense", "color": "#666666", "data": [0.62, 0.69, 0.72, 0.75, 0.77, 0.82, 0.87, 0.89]},
        {"name": "Interest", "color": "#E9C46A", "data": [0.33, 0.38, 0.35, 0.35, 0.48, 0.66, 0.87, 0.95]},
    ]},
    {"id": 34, "type": "area", "title": "Global Cloud Computing Market Share", "subtitle": "Per cent of market", "years": list(range(2018, 2026)), "series": [
        {"name": "AWS", "color": "#F4A261", "data": [33, 32, 31, 32, 34, 32, 31, 31]},
        {"name": "Azure", "color": "#457B9D", "data": [16, 18, 20, 21, 22, 24, 25, 26]},
        {"name": "Google Cloud", "color": "#E63946", "data": [8, 8, 9, 10, 10, 11, 12, 13]},
        {"name": "Others", "color": "#96CEB4", "data": [43, 42, 40, 37, 34, 33, 32, 30]},
    ]},
    {"id": 35, "type": "area", "title": "European Electricity Generation Mix", "subtitle": "Terawatt hours", "years": list(range(2015, 2026)), "series": [
        {"name": "Fossil Fuels", "color": "#666666", "data": [1550, 1500, 1460, 1420, 1350, 1300, 1250, 1200, 1100, 1050, 1000]},
        {"name": "Nuclear", "color": "#F4A261", "data": [830, 820, 810, 800, 790, 780, 770, 700, 680, 650, 640]},
        {"name": "Wind & Solar", "color": "#2A9D8F", "data": [380, 410, 470, 510, 570, 620, 700, 810, 880, 960, 1040]},
        {"name": "Hydro", "color": "#457B9D", "data": [580, 590, 540, 560, 600, 620, 610, 580, 600, 590, 600]},
    ]},
    {"id": 36, "type": "area", "title": "Global Semiconductor Revenue", "subtitle": "USD billions", "years": list(range(2015, 2026)), "series": [
        {"name": "Memory", "color": "#E63946", "data": [77, 73, 117, 158, 110, 112, 153, 130, 96, 140, 170]},
        {"name": "Logic", "color": "#457B9D", "data": [92, 95, 98, 103, 107, 115, 128, 145, 165, 185, 200]},
        {"name": "Analog", "color": "#2A9D8F", "data": [47, 46, 49, 55, 53, 54, 61, 72, 67, 75, 80]},
        {"name": "Other", "color": "#E9C46A", "data": [120, 122, 125, 130, 135, 140, 148, 155, 160, 168, 175]},
    ]},
    {"id": 37, "type": "area", "title": "US Vehicle Sales by Type", "subtitle": "Millions of units", "years": list(range(2015, 2026)), "series": [
        {"name": "SUV/CUV", "color": "#E63946", "data": [5.9, 6.4, 6.8, 7.1, 7.4, 6.5, 7.2, 7.5, 7.8, 8.0, 8.2]},
        {"name": "Pickup", "color": "#457B9D", "data": [2.7, 2.8, 3.0, 3.1, 3.2, 2.9, 3.0, 3.1, 3.2, 3.3, 3.3]},
        {"name": "Sedan", "color": "#2A9D8F", "data": [5.8, 5.3, 4.6, 4.1, 3.6, 3.0, 2.8, 2.6, 2.5, 2.4, 2.3]},
        {"name": "Other", "color": "#E9C46A", "data": [3.0, 2.9, 2.8, 2.7, 2.5, 2.2, 2.1, 2.0, 1.9, 1.8, 1.8]},
    ]},
    {"id": 38, "type": "area", "title": "Global Data Center Energy Use", "subtitle": "Terawatt hours", "years": list(range(2018, 2026)), "series": [
        {"name": "Traditional", "color": "#666666", "data": [110, 108, 105, 100, 95, 90, 85, 80]},
        {"name": "Hyperscale", "color": "#457B9D", "data": [60, 70, 85, 100, 120, 140, 170, 200]},
        {"name": "AI Training", "color": "#E63946", "data": [2, 3, 5, 8, 15, 30, 55, 85]},
    ]},
    {"id": 39, "type": "area", "title": "UN Peacekeeping Personnel", "subtitle": "Thousands", "years": list(range(2010, 2026)), "series": [
        {"name": "Military", "color": "#457B9D", "data": [84, 82, 78, 80, 82, 83, 80, 77, 73, 69, 65, 63, 61, 60, 58, 57]},
        {"name": "Police", "color": "#2A9D8F", "data": [14, 14, 15, 13, 12, 13, 12, 12, 11, 11, 10, 10, 10, 9, 9, 9]},
        {"name": "Civilian", "color": "#E9C46A", "data": [6, 6, 5, 5, 5, 5, 5, 5, 5, 5, 4, 4, 4, 4, 4, 4]},
    ]},
    {"id": 40, "type": "area", "title": "Global Mobile Traffic by Type", "subtitle": "Exabytes per month", "years": list(range(2018, 2026)), "series": [
        {"name": "Video", "color": "#E63946", "data": [16, 22, 30, 42, 55, 72, 95, 120]},
        {"name": "Social Media", "color": "#457B9D", "data": [4, 5, 7, 9, 11, 14, 17, 20]},
        {"name": "Web/Other", "color": "#2A9D8F", "data": [6, 7, 8, 9, 10, 11, 12, 13]},
    ]},
    {"id": 41, "type": "area", "title": "China Electricity Generation Mix", "subtitle": "Terawatt hours", "years": list(range(2015, 2026)), "series": [
        {"name": "Coal", "color": "#666666", "data": [3900, 3910, 4150, 4430, 4600, 4630, 5030, 5200, 5200, 5100, 5000]},
        {"name": "Hydro", "color": "#457B9D", "data": [1130, 1180, 1190, 1230, 1300, 1360, 1340, 1350, 1400, 1450, 1500]},
        {"name": "Wind & Solar", "color": "#2A9D8F", "data": [290, 375, 420, 530, 625, 730, 950, 1200, 1500, 1850, 2200]},
        {"name": "Nuclear", "color": "#F4A261", "data": [170, 213, 248, 295, 348, 366, 407, 418, 435, 460, 490]},
    ]},
    {"id": 42, "type": "area", "title": "Global Ad Spending by Medium", "subtitle": "USD billions", "years": list(range(2018, 2026)), "series": [
        {"name": "Digital", "color": "#E63946", "data": [283, 325, 356, 438, 515, 567, 616, 660]},
        {"name": "TV", "color": "#457B9D", "data": [183, 176, 160, 169, 168, 165, 162, 158]},
        {"name": "Print", "color": "#666666", "data": [59, 53, 42, 38, 35, 33, 31, 29]},
        {"name": "Other", "color": "#E9C46A", "data": [55, 53, 47, 50, 48, 47, 46, 45]},
    ]},
    {"id": 43, "type": "area", "title": "India Energy Consumption", "subtitle": "Exajoules", "years": list(range(2015, 2026)), "series": [
        {"name": "Coal", "color": "#666666", "data": [10.2, 10.8, 11.2, 12.0, 12.2, 11.8, 12.5, 13.0, 13.5, 14.0, 14.3]},
        {"name": "Oil", "color": "#E63946", "data": [8.5, 8.9, 9.4, 9.6, 9.8, 8.7, 9.1, 9.5, 10.0, 10.3, 10.6]},
        {"name": "Gas", "color": "#457B9D", "data": [1.7, 1.7, 1.8, 1.9, 2.0, 2.0, 2.1, 2.2, 2.2, 2.3, 2.4]},
        {"name": "Renewables", "color": "#2A9D8F", "data": [0.8, 0.9, 1.1, 1.3, 1.5, 1.7, 1.9, 2.4, 3.0, 3.6, 4.2]},
    ]},
    {"id": 44, "type": "area", "title": "Global Box Office Revenue by Region", "subtitle": "USD billions", "years": list(range(2015, 2026)), "series": [
        {"name": "North America", "color": "#457B9D", "data": [11.1, 11.4, 11.1, 11.9, 11.3, 2.2, 4.5, 7.4, 9.0, 9.5, 9.8]},
        {"name": "China", "color": "#E63946", "data": [6.8, 6.6, 7.9, 9.0, 9.2, 3.0, 7.3, 6.0, 7.7, 8.5, 8.8]},
        {"name": "Europe", "color": "#2A9D8F", "data": [4.5, 4.3, 4.8, 4.7, 4.5, 0.9, 2.5, 3.8, 4.0, 4.3, 4.5]},
        {"name": "Rest of World", "color": "#E9C46A", "data": [4.0, 4.2, 4.5, 4.7, 5.0, 1.8, 3.2, 4.3, 5.0, 5.5, 5.7]},
    ]},
    {"id": 45, "type": "area", "title": "Global Shipping Trade Volume", "subtitle": "Billion tonnes loaded", "years": list(range(2015, 2026)), "series": [
        {"name": "Dry Bulk", "color": "#666666", "data": [4.7, 4.8, 5.0, 5.2, 5.2, 5.0, 5.1, 5.2, 5.3, 5.4, 5.5]},
        {"name": "Tanker", "color": "#E63946", "data": [2.9, 3.1, 3.1, 3.1, 3.0, 2.8, 2.9, 3.0, 3.0, 3.1, 3.1]},
        {"name": "Container", "color": "#457B9D", "data": [1.7, 1.7, 1.8, 1.9, 1.9, 1.8, 1.9, 2.0, 2.0, 2.1, 2.1]},
    ]},

    # --- TYPE 4: BAR CHARTS (charts 46-65) ---
    {"id": 46, "type": "bar", "title": "Top Countries by GDP (Nominal)", "subtitle": "USD trillions, 2025 estimates", "items": [
        ("United States", 31.8), ("China", 20.7), ("Germany", 5.3), ("India", 4.5),
        ("Japan", 4.5), ("United Kingdom", 4.2), ("France", 3.6), ("Italy", 2.7),
        ("Russia", 2.5), ("Canada", 2.4), ("Brazil", 2.3), ("Spain", 2.0),
        ("Mexico", 2.0), ("Australia", 1.9), ("South Korea", 1.9), ("Turkey", 1.6),
    ]},
    {"id": 47, "type": "bar", "title": "Countries by Population 2025", "subtitle": "Millions", "items": [
        ("India", 1450), ("China", 1410), ("United States", 339), ("Indonesia", 279),
        ("Pakistan", 229), ("Brazil", 221), ("Nigeria", 217), ("Bangladesh", 168),
        ("Russia", 147), ("Mexico", 128), ("Japan", 124), ("Ethiopia", 126),
        ("Philippines", 115), ("Egypt", 110), ("Vietnam", 104), ("DR Congo", 102),
    ]},
    {"id": 48, "type": "bar", "title": "Top CO2 Emitting Countries", "subtitle": "Billion metric tons, 2023", "items": [
        ("China", 13.3), ("United States", 4.7), ("India", 3.0), ("Russia", 2.1),
        ("Japan", 0.94), ("Iran", 0.78), ("Indonesia", 0.67), ("Saudi Arabia", 0.62),
        ("Germany", 0.58), ("Canada", 0.58), ("South Korea", 0.57), ("Mexico", 0.49),
        ("Brazil", 0.48), ("Turkey", 0.44), ("South Africa", 0.40), ("Australia", 0.37),
    ]},
    {"id": 49, "type": "bar", "title": "Countries by Military Spending", "subtitle": "USD billions, 2024", "items": [
        ("United States", 886), ("China", 296), ("Russia", 140), ("India", 83),
        ("Saudi Arabia", 76), ("United Kingdom", 75), ("Germany", 67), ("France", 60),
        ("Japan", 55), ("South Korea", 48), ("Ukraine", 41), ("Italy", 35),
        ("Australia", 33), ("Brazil", 22), ("Canada", 21), ("Poland", 32),
    ]},
    {"id": 50, "type": "bar", "title": "Top Countries by Renewable Energy", "subtitle": "Gigawatts installed capacity, 2024", "items": [
        ("China", 1450), ("United States", 425), ("India", 195), ("Germany", 170),
        ("Brazil", 175), ("Japan", 115), ("United Kingdom", 60), ("Spain", 72),
        ("France", 68), ("Australia", 55), ("Italy", 62), ("South Korea", 30),
        ("Canada", 35), ("Netherlands", 32), ("Turkey", 55), ("Vietnam", 48),
    ]},
    {"id": 51, "type": "bar", "title": "Countries by Internet Penetration", "subtitle": "Per cent of population, 2025", "items": [
        ("Denmark", 99), ("South Korea", 98), ("United Kingdom", 97), ("Japan", 96),
        ("Germany", 96), ("Netherlands", 96), ("Canada", 95), ("Australia", 95),
        ("United States", 95), ("France", 93), ("Spain", 93), ("Italy", 91),
        ("Brazil", 84), ("China", 76), ("Mexico", 76), ("India", 52),
    ]},
    {"id": 52, "type": "bar", "title": "Top Countries by Tourism Revenue", "subtitle": "USD billions, 2024", "items": [
        ("United States", 195), ("Spain", 96), ("France", 76), ("Turkey", 58),
        ("United Kingdom", 56), ("Italy", 55), ("UAE", 50), ("Germany", 46),
        ("Japan", 43), ("Australia", 40), ("Thailand", 38), ("Canada", 30),
        ("Mexico", 30), ("Portugal", 26), ("Greece", 24), ("Saudi Arabia", 23),
    ]},
    {"id": 53, "type": "bar", "title": "Top Coffee Producing Countries", "subtitle": "Million 60-kg bags, 2024/2025", "items": [
        ("Brazil", 67), ("Vietnam", 30), ("Colombia", 14), ("Indonesia", 12),
        ("Ethiopia", 8.7), ("Honduras", 7.0), ("India", 5.8), ("Uganda", 5.5),
        ("Mexico", 3.8), ("Peru", 3.7), ("Guatemala", 3.6), ("Nicaragua", 2.9),
        ("Ivory Coast", 2.2), ("Costa Rica", 1.3), ("Kenya", 0.85), ("Tanzania", 0.82),
    ]},
    {"id": 54, "type": "bar", "title": "Fastest Growing Economies 2025", "subtitle": "Real GDP growth rate, per cent", "items": [
        ("Guyana", 24.4), ("Libya", 12.5), ("Palau", 11.2), ("Macao", 10.1),
        ("Niger", 9.5), ("Senegal", 8.8), ("India", 7.0), ("Philippines", 6.3),
        ("Cambodia", 6.2), ("Rwanda", 6.1), ("Bangladesh", 5.9), ("Vietnam", 5.8),
        ("Indonesia", 5.3), ("Kenya", 5.0), ("Uzbekistan", 5.0), ("Egypt", 4.5),
    ]},
    {"id": 55, "type": "bar", "title": "Countries by Life Expectancy", "subtitle": "Years, 2024 estimates", "items": [
        ("Japan", 84.6), ("Switzerland", 84.0), ("Spain", 83.9), ("Singapore", 83.8),
        ("Australia", 83.6), ("South Korea", 83.5), ("Italy", 83.5), ("Norway", 83.3),
        ("Sweden", 83.1), ("Israel", 83.0), ("France", 82.8), ("Canada", 82.5),
        ("Netherlands", 82.3), ("New Zealand", 82.2), ("Germany", 81.9), ("UK", 81.7),
    ]},
    {"id": 56, "type": "bar", "title": "Top Rice Producing Countries", "subtitle": "Million metric tons, 2024", "items": [
        ("China", 206), ("India", 195), ("Bangladesh", 56), ("Indonesia", 54),
        ("Vietnam", 44), ("Thailand", 32), ("Myanmar", 26), ("Philippines", 19),
        ("Japan", 10), ("Pakistan", 9), ("Brazil", 8), ("United States", 7),
        ("Cambodia", 6), ("South Korea", 5), ("Nepal", 4.6), ("Nigeria", 4.5),
    ]},
    {"id": 57, "type": "bar", "title": "Countries by Debt-to-GDP Ratio", "subtitle": "Per cent of GDP, 2025 estimates", "items": [
        ("Japan", 252), ("Greece", 168), ("Italy", 139), ("United States", 123),
        ("Singapore", 120), ("France", 112), ("Spain", 107), ("Canada", 105),
        ("Belgium", 105), ("United Kingdom", 100), ("Portugal", 98), ("Brazil", 87),
        ("India", 82), ("China", 80), ("Germany", 62), ("Australia", 52),
    ]},
    {"id": 58, "type": "bar", "title": "Top Countries by Patent Applications", "subtitle": "Thousands, 2024", "items": [
        ("China", 1580), ("United States", 588), ("Japan", 289), ("South Korea", 234),
        ("Germany", 65), ("India", 64), ("France", 16), ("United Kingdom", 15),
        ("Switzerland", 14), ("Netherlands", 11), ("Russia", 22), ("Canada", 10),
        ("Sweden", 9), ("Israel", 8), ("Australia", 8), ("Italy", 7),
    ]},
    {"id": 59, "type": "bar", "title": "Top Wheat Producing Countries", "subtitle": "Million metric tons, 2024", "items": [
        ("China", 137), ("India", 110), ("Russia", 92), ("United States", 50),
        ("Canada", 35), ("France", 34), ("Australia", 32), ("Ukraine", 25),
        ("Pakistan", 27), ("Germany", 22), ("Turkey", 19), ("Argentina", 18),
        ("UK", 16), ("Kazakhstan", 16), ("Poland", 14), ("Egypt", 10),
    ]},
    {"id": 60, "type": "bar", "title": "Top Natural Gas Producing Countries", "subtitle": "Billion cubic meters, 2024", "items": [
        ("United States", 1035), ("Russia", 638), ("Iran", 260), ("China", 235),
        ("Canada", 188), ("Qatar", 178), ("Australia", 155), ("Norway", 123),
        ("Saudi Arabia", 117), ("Algeria", 100), ("Turkmenistan", 83), ("Indonesia", 60),
        ("Malaysia", 55), ("Egypt", 52), ("UK", 38), ("Argentina", 44),
    ]},
    {"id": 61, "type": "bar", "title": "Top Countries by FDI Inflows", "subtitle": "USD billions, 2024", "items": [
        ("United States", 310), ("China", 163), ("Singapore", 141), ("Brazil", 66),
        ("Canada", 48), ("India", 44), ("Australia", 38), ("France", 35),
        ("Mexico", 33), ("Hong Kong", 32), ("United Kingdom", 30), ("Germany", 28),
        ("UAE", 27), ("Indonesia", 22), ("Poland", 20), ("Spain", 18),
    ]},
    {"id": 62, "type": "bar", "title": "Global Car Production by Country", "subtitle": "Millions of units, 2024", "items": [
        ("China", 30.2), ("Japan", 9.0), ("India", 5.9), ("South Korea", 4.3),
        ("Germany", 4.1), ("United States", 3.9), ("Spain", 2.4), ("Mexico", 2.1),
        ("Brazil", 2.3), ("Thailand", 1.9), ("Turkey", 1.7), ("France", 1.5),
        ("Czech Republic", 1.3), ("Indonesia", 1.2), ("Russia", 1.2), ("UK", 1.0),
    ]},
    {"id": 63, "type": "bar", "title": "Top Countries by Forest Area", "subtitle": "Million square kilometres, 2024", "items": [
        ("Russia", 8.15), ("Brazil", 4.96), ("Canada", 3.47), ("United States", 3.10),
        ("China", 2.20), ("DR Congo", 1.52), ("Australia", 1.34), ("Indonesia", 0.92),
        ("Peru", 0.74), ("India", 0.73), ("Mexico", 0.66), ("Colombia", 0.59),
        ("Angola", 0.58), ("Bolivia", 0.55), ("Zambia", 0.49), ("Venezuela", 0.47),
    ]},
    {"id": 64, "type": "bar", "title": "Top Countries by Electricity Production", "subtitle": "Terawatt hours, 2024", "items": [
        ("China", 9200), ("United States", 4260), ("India", 1900), ("Russia", 1130),
        ("Japan", 930), ("Brazil", 680), ("Canada", 650), ("Germany", 550),
        ("South Korea", 590), ("France", 530), ("UK", 310), ("Australia", 265),
        ("Mexico", 320), ("Turkey", 330), ("Indonesia", 310), ("Saudi Arabia", 380),
    ]},
    {"id": 65, "type": "bar", "title": "Global University Rankings - Top Countries", "subtitle": "Number of institutions in top 200, 2025", "items": [
        ("United States", 56), ("United Kingdom", 26), ("Germany", 11), ("Australia", 10),
        ("China", 10), ("Canada", 8), ("Netherlands", 8), ("Switzerland", 7),
        ("Japan", 5), ("Singapore", 4), ("France", 5), ("South Korea", 5),
        ("Hong Kong", 5), ("Sweden", 4), ("Belgium", 3), ("Denmark", 3),
    ]},

    # --- TYPE 5: VOLATILITY / OSCILLATING CHARTS (charts 66-80) ---
    {"id": 66, "type": "oscillating", "title": "EU Trade Balance with China", "subtitle": "EUR billions, monthly", "years": list(range(2020, 2026)), "series": [{"name": "Trade Balance", "color": "#E63946", "data": gen_line_data(72, -20, 5, -0.1)}]},
    {"id": 67, "type": "oscillating", "title": "US Consumer Sentiment Index", "subtitle": "Index (1966=100)", "years": list(range(2018, 2026)), "series": [{"name": "Sentiment", "color": "#457B9D", "data": gen_line_data(96, 80, 8, -0.2)}]},
    {"id": 68, "type": "oscillating", "title": "German Industrial Production", "subtitle": "Month-on-month percentage change", "years": list(range(2020, 2026)), "series": [{"name": "Production", "color": "#2A9D8F", "data": gen_line_data(72, 0, 3)}]},
    {"id": 69, "type": "oscillating", "title": "Japan Trade Balance", "subtitle": "JPY trillions, monthly", "years": list(range(2020, 2026)), "series": [{"name": "Trade Balance", "color": "#E9C46A", "data": gen_line_data(72, -0.5, 0.4)}]},
    {"id": 70, "type": "oscillating", "title": "China PMI Manufacturing Index", "subtitle": "Index, 50 = expansion threshold", "years": list(range(2020, 2026)), "series": [{"name": "PMI", "color": "#E63946", "data": gen_line_data(72, 50, 2)}]},
    {"id": 71, "type": "oscillating", "title": "US Weekly Jobless Claims", "subtitle": "Thousands, seasonally adjusted", "years": list(range(2020, 2026)), "series": [{"name": "Claims", "color": "#F4A261", "data": gen_line_data(72, 250, 40, -0.5)}]},
    {"id": 72, "type": "oscillating", "title": "Brazil Real vs USD Exchange Rate", "subtitle": "BRL per USD", "years": list(range(2018, 2026)), "series": [{"name": "BRL/USD", "color": "#2A9D8F", "data": gen_line_data(96, 5.0, 0.3, 0.01)}]},
    {"id": 73, "type": "oscillating", "title": "UK Retail Sales Growth", "subtitle": "Year-on-year percentage change", "years": list(range(2020, 2026)), "series": [{"name": "Retail Growth", "color": "#457B9D", "data": gen_line_data(72, 2, 4)}]},
    {"id": 74, "type": "oscillating", "title": "India Rupee vs USD", "subtitle": "INR per USD", "years": list(range(2018, 2026)), "series": [{"name": "INR/USD", "color": "#E63946", "data": gen_line_data(96, 78, 2, 0.05)}]},
    {"id": 75, "type": "oscillating", "title": "Australian Dollar vs USD", "subtitle": "AUD per USD", "years": list(range(2018, 2026)), "series": [{"name": "AUD/USD", "color": "#96CEB4", "data": gen_line_data(96, 0.70, 0.03)}]},
    {"id": 76, "type": "oscillating", "title": "Euro Area Consumer Confidence", "subtitle": "Index", "years": list(range(2018, 2026)), "series": [{"name": "Confidence", "color": "#A29BFE", "data": gen_line_data(96, -8, 5)}]},
    {"id": 77, "type": "oscillating", "title": "South Africa Rand vs USD", "subtitle": "ZAR per USD", "years": list(range(2018, 2026)), "series": [{"name": "ZAR/USD", "color": "#FD79A8", "data": gen_line_data(96, 17, 1, 0.02)}]},
    {"id": 78, "type": "oscillating", "title": "Turkey Lira vs USD", "subtitle": "TRY per USD", "years": list(range(2018, 2026)), "series": [{"name": "TRY/USD", "color": "#00B894", "data": gen_line_data(96, 20, 3, 0.3)}]},
    {"id": 79, "type": "oscillating", "title": "Russia Ruble vs USD", "subtitle": "RUB per USD", "years": list(range(2018, 2026)), "series": [{"name": "RUB/USD", "color": "#636E72", "data": gen_line_data(96, 75, 8, 0.2)}]},
    {"id": 80, "type": "oscillating", "title": "VIX Volatility Index", "subtitle": "CBOE Volatility Index", "years": list(range(2018, 2026)), "series": [{"name": "VIX", "color": "#E63946", "data": gen_line_data(96, 18, 5)}]},

    # --- TYPE 6: DUAL LINE COMPARISON CHARTS (charts 81-90) ---
    {"id": 81, "type": "multiline", "title": "US vs China GDP", "subtitle": "USD trillions", "years": list(range(2010, 2026)), "series": [
        {"name": "United States", "color": "#457B9D", "data": [14.99, 15.54, 16.20, 16.78, 17.52, 18.21, 18.71, 19.48, 20.53, 21.37, 21.06, 23.32, 25.46, 27.36, 28.75, 31.82]},
        {"name": "China", "color": "#E63946", "data": [6.09, 7.55, 8.53, 9.57, 10.48, 11.06, 11.23, 12.31, 13.89, 14.28, 14.69, 17.73, 17.96, 17.79, 18.74, 20.65]},
    ]},
    {"id": 82, "type": "multiline", "title": "Brent Crude vs WTI Oil Price", "subtitle": "USD per barrel, annual average", "years": list(range(2015, 2026)), "series": [
        {"name": "Brent Crude", "color": "#E63946", "data": [52, 44, 54, 71, 64, 42, 71, 99, 83, 80, 75]},
        {"name": "WTI", "color": "#457B9D", "data": [49, 43, 51, 65, 57, 39, 68, 95, 78, 76, 72]},
    ]},
    {"id": 83, "type": "multiline", "title": "USD-EUR vs USD-GBP Exchange Rates", "subtitle": "Exchange rate", "years": list(range(2015, 2026)), "series": [
        {"name": "EUR/USD", "color": "#E63946", "data": [1.11, 1.05, 1.13, 1.18, 1.12, 1.14, 1.18, 1.05, 1.08, 1.09, 1.07]},
        {"name": "GBP/USD", "color": "#457B9D", "data": [1.53, 1.36, 1.29, 1.33, 1.28, 1.28, 1.38, 1.23, 1.24, 1.27, 1.25]},
    ]},
    {"id": 84, "type": "multiline", "title": "Apple vs Microsoft Market Cap", "subtitle": "USD trillions", "years": list(range(2018, 2026)), "series": [
        {"name": "Apple", "color": "#666666", "data": [0.91, 1.29, 2.07, 2.91, 2.07, 3.0, 3.4, 3.7]},
        {"name": "Microsoft", "color": "#457B9D", "data": [0.78, 1.20, 1.68, 2.53, 1.79, 2.8, 3.1, 3.3]},
    ]},
    {"id": 85, "type": "multiline", "title": "US 10Y vs 2Y Treasury Yields", "subtitle": "Per cent", "years": list(range(2018, 2026)), "series": [
        {"name": "10-Year", "color": "#E63946", "data": [2.91, 1.92, 0.89, 1.52, 3.88, 4.57, 4.28, 4.10]},
        {"name": "2-Year", "color": "#457B9D", "data": [2.68, 1.57, 0.12, 0.73, 4.43, 5.03, 4.60, 4.00]},
    ]},
    {"id": 86, "type": "multiline", "title": "US CPI vs Core CPI", "subtitle": "Year-on-year percentage change", "years": list(range(2018, 2026)), "series": [
        {"name": "CPI", "color": "#E63946", "data": [2.4, 1.8, 1.2, 4.7, 8.0, 4.1, 2.9, 2.5]},
        {"name": "Core CPI", "color": "#457B9D", "data": [2.1, 2.2, 1.6, 3.6, 6.2, 4.8, 3.4, 2.8]},
    ]},
    {"id": 87, "type": "multiline", "title": "Bitcoin vs Ethereum Price", "subtitle": "Index, Jan 2020 = 100", "years": list(range(2020, 2026)), "series": [
        {"name": "Bitcoin", "color": "#F4A261", "data": [100, 405, 640, 360, 580, 1320]},
        {"name": "Ethereum", "color": "#457B9D", "data": [100, 2770, 2890, 1450, 2300, 3100]},
    ]},
    {"id": 88, "type": "multiline", "title": "Global Crude Steel Production", "subtitle": "Million metric tons, top producers", "years": list(range(2018, 2026)), "series": [
        {"name": "China", "color": "#E63946", "data": [928, 996, 1065, 1033, 1018, 1019, 1005, 990]},
        {"name": "India", "color": "#2A9D8F", "data": [109, 111, 100, 118, 125, 140, 148, 155]},
        {"name": "EU", "color": "#457B9D", "data": [168, 159, 139, 153, 137, 127, 130, 132]},
    ]},
    {"id": 89, "type": "multiline", "title": "US Personal Savings Rate", "subtitle": "Per cent of disposable income", "years": list(range(2015, 2026)), "series": [
        {"name": "Savings Rate", "color": "#2A9D8F", "data": [7.6, 6.8, 6.8, 7.6, 7.6, 16.8, 12.0, 3.4, 4.7, 5.0, 4.8]},
    ]},
    {"id": 90, "type": "multiline", "title": "Fertilizer Price Indices", "subtitle": "Index, 2010 = 100", "years": list(range(2015, 2026)), "series": [
        {"name": "Urea", "color": "#2A9D8F", "data": [78, 65, 72, 75, 80, 95, 185, 280, 145, 120, 115]},
        {"name": "DAP", "color": "#E63946", "data": [90, 75, 78, 82, 80, 85, 135, 220, 160, 130, 125]},
        {"name": "Potash", "color": "#E9C46A", "data": [95, 82, 78, 82, 80, 78, 95, 250, 175, 140, 130]},
    ]},

    # --- TYPE 7: MORE LINE/MULTI-LINE CHARTS (charts 91-100) ---
    {"id": 91, "type": "line", "title": "Global Average Temperature Anomaly", "subtitle": "Degrees Celsius above pre-industrial baseline", "years": list(range(2000, 2026)), "series": [{"name": "Anomaly", "color": "#E63946", "data": [0.39, 0.53, 0.63, 0.62, 0.53, 0.67, 0.64, 0.66, 0.54, 0.64, 0.72, 0.61, 0.64, 0.68, 0.74, 0.90, 1.01, 0.92, 0.83, 0.98, 1.29, 1.16, 1.15, 1.48, 1.55, 1.43]}]},
    {"id": 92, "type": "multiline", "title": "FAANG Stock Performance", "subtitle": "Index, Jan 2020 = 100", "years": list(range(2020, 2026)), "series": [
        {"name": "Apple", "color": "#666666", "data": [100, 163, 195, 182, 230, 268]},
        {"name": "Amazon", "color": "#F4A261", "data": [100, 125, 101, 79, 118, 140]},
        {"name": "Google", "color": "#E63946", "data": [100, 146, 148, 103, 165, 195]},
        {"name": "Meta", "color": "#457B9D", "data": [100, 141, 102, 47, 157, 210]},
    ]},
    {"id": 93, "type": "line", "title": "Global Sea Level Rise", "subtitle": "Millimetres above 1993 baseline", "years": list(range(2000, 2026)), "series": [{"name": "Sea Level", "color": "#457B9D", "data": [20, 23, 28, 30, 31, 35, 38, 42, 45, 48, 51, 54, 58, 62, 66, 70, 74, 79, 83, 87, 90, 95, 100, 105, 110, 115]}]},
    {"id": 94, "type": "multiline", "title": "Global Arms Exports by Country", "subtitle": "SIPRI Trend Indicator Values, billions", "years": list(range(2015, 2026)), "series": [
        {"name": "United States", "color": "#457B9D", "data": [10.5, 10.2, 12.4, 10.7, 10.6, 9.4, 11.2, 15.5, 13.8, 14.2, 14.5]},
        {"name": "Russia", "color": "#E63946", "data": [5.5, 6.2, 6.1, 6.4, 5.7, 3.2, 2.8, 1.8, 1.5, 1.8, 2.0]},
        {"name": "France", "color": "#2A9D8F", "data": [2.0, 2.2, 1.6, 1.8, 2.0, 1.7, 2.1, 3.0, 3.5, 3.2, 3.4]},
        {"name": "China", "color": "#E9C46A", "data": [1.8, 2.4, 2.3, 1.9, 2.2, 1.4, 1.6, 1.2, 1.0, 1.1, 1.0]},
    ]},
    {"id": 95, "type": "line", "title": "Amazon Deforestation Rate", "subtitle": "Square kilometres per year", "years": list(range(2010, 2026)), "series": [{"name": "Deforestation", "color": "#2A9D8F", "data": [7000, 6418, 4571, 5891, 5012, 6207, 7893, 6947, 7536, 10129, 11088, 13235, 11568, 9001, 8200, 7500]}]},
    {"id": 96, "type": "multiline", "title": "Global LNG Trade by Importer", "subtitle": "Billion cubic metres", "years": list(range(2018, 2026)), "series": [
        {"name": "Japan", "color": "#E63946", "data": [113, 106, 102, 100, 97, 95, 90, 85]},
        {"name": "China", "color": "#457B9D", "data": [73, 85, 94, 108, 87, 93, 106, 115]},
        {"name": "South Korea", "color": "#2A9D8F", "data": [62, 56, 55, 62, 65, 64, 63, 62]},
        {"name": "Europe", "color": "#E9C46A", "data": [66, 85, 102, 101, 165, 158, 140, 135]},
    ]},
    {"id": 97, "type": "line", "title": "Global Refugee Population", "subtitle": "Millions of people", "years": list(range(2010, 2026)), "series": [{"name": "Refugees", "color": "#E63946", "data": [10.5, 10.4, 10.5, 11.7, 14.4, 16.1, 17.2, 19.9, 20.4, 20.4, 20.7, 21.3, 26.6, 35.8, 36.4, 37.0]}]},
    {"id": 98, "type": "multiline", "title": "Central Government Debt by Country", "subtitle": "Per cent of GDP", "years": list(range(2015, 2026)), "series": [
        {"name": "Japan", "color": "#E63946", "data": [231, 236, 235, 237, 238, 259, 263, 264, 255, 252, 250]},
        {"name": "USA", "color": "#457B9D", "data": [105, 107, 106, 107, 108, 134, 128, 123, 123, 123, 124]},
        {"name": "UK", "color": "#2A9D8F", "data": [87, 87, 87, 86, 85, 106, 102, 101, 100, 100, 100]},
        {"name": "Germany", "color": "#E9C46A", "data": [72, 69, 65, 62, 59, 69, 69, 66, 65, 62, 62]},
    ]},
    {"id": 99, "type": "line", "title": "Arctic Sea Ice Minimum Extent", "subtitle": "Million square kilometres, September", "years": list(range(2000, 2026)), "series": [{"name": "Sea Ice", "color": "#74B9FF", "data": [6.3, 6.7, 5.96, 6.15, 6.05, 5.57, 5.92, 4.30, 4.73, 5.39, 4.93, 4.63, 3.63, 5.35, 5.28, 4.63, 4.72, 4.87, 4.71, 4.32, 3.92, 4.72, 4.67, 4.50, 4.30, 4.20]}]},
    {"id": 100, "type": "multiline", "title": "World Happiness Score by Region", "subtitle": "Score out of 10", "years": list(range(2015, 2026)), "series": [
        {"name": "Western Europe", "color": "#457B9D", "data": [6.9, 6.9, 6.9, 7.0, 7.0, 7.0, 7.0, 6.9, 6.9, 7.0, 7.0]},
        {"name": "North America", "color": "#2A9D8F", "data": [7.1, 7.1, 7.0, 7.0, 6.9, 6.9, 6.9, 6.8, 6.7, 6.7, 6.7]},
        {"name": "East Asia", "color": "#E63946", "data": [5.8, 5.9, 5.9, 5.9, 5.9, 5.8, 5.9, 6.0, 6.0, 6.1, 6.1]},
        {"name": "Sub-Saharan Africa", "color": "#F4A261", "data": [4.3, 4.3, 4.3, 4.4, 4.4, 4.4, 4.5, 4.5, 4.5, 4.5, 4.5]},
    ]},
]


# ========== SVG GENERATION FUNCTIONS ==========

def svg_header():
    return '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\n<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720" preserveAspectRatio="xMidYMid meet">\n'


def svg_footer():
    return '</svg>\n'


def map_value(val, min_val, max_val, top, bottom):
    if max_val == min_val:
        return (top + bottom) / 2
    return bottom - (val - min_val) / (max_val - min_val) * (bottom - top)


def generate_line_chart(chart, multi=False):
    """Generate a line chart SVG."""
    svg = svg_header()
    svg += CHART_STYLES.format()

    # Background
    svg += '  <rect class="bg" x="0" y="0" width="960" height="720" />\n'

    # Title
    svg += f'  <text class="title" x="70" y="42">{chart["title"]}</text>\n'
    svg += f'  <text class="subtitle" x="70" y="72">{chart["subtitle"]}</text>\n'

    # Chart area
    left, right, top, bottom = 80, 920, 95, 580

    # Find data range
    all_vals = []
    for s in chart["series"]:
        all_vals.extend(s["data"])
    min_val = min(all_vals)
    max_val = max(all_vals)
    padding = (max_val - min_val) * 0.1 if max_val != min_val else 1
    min_val -= padding
    max_val += padding

    # Y-axis grid lines
    n_grid = 6
    for i in range(n_grid + 1):
        y = top + i * (bottom - top) / n_grid
        v = max_val - i * (max_val - min_val) / n_grid
        svg += f'  <line class="axis-line" x1="{left}" y1="{y:.0f}" x2="{right}" y2="{y:.0f}" />\n'
        svg += f'  <text class="y-tick-label" x="{left - 8}" y="{y + 4:.0f}">{v:.1f}</text>\n'

    # X-axis
    years = chart["years"]
    n_pts = len(years)
    step = max(1, n_pts // 8)
    for i in range(0, n_pts, step):
        x = left + i * (right - left) / (n_pts - 1) if n_pts > 1 else left
        svg += f'  <line class="axis-line" x1="{x:.0f}" y1="{bottom}" x2="{x:.0f}" y2="{bottom + 6}" />\n'
        svg += f'  <text class="tick-label" x="{x:.0f}" y="{bottom + 22}">{years[i]}</text>\n'

    # Bold baseline
    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" />\n'
    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" />\n'

    # Data lines
    for s in chart["series"]:
        data = s["data"]
        color = s["color"]
        pts = []
        for i, v in enumerate(data):
            x = left + i * (right - left) / (len(data) - 1) if len(data) > 1 else left
            y = map_value(v, min_val, max_val, top, bottom)
            pts.append(f"{x:.0f},{y:.0f}")
        svg += f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2.5" />\n'

    # Legend
    ly = 650
    lx = left
    for i, s in enumerate(chart["series"]):
        x = lx + i * 180
        svg += f'  <line x1="{x}" y1="{ly}" x2="{x + 20}" y2="{ly}" stroke="{s["color"]}" stroke-width="2.5" />\n'
        svg += f'  <text class="legend-text" x="{x + 25}" y="{ly + 4}">{s["name"]}</text>\n'

    svg += svg_footer()
    return svg


def generate_area_chart(chart):
    """Generate a stacked area chart SVG."""
    svg = svg_header()
    svg += CHART_STYLES.format()
    svg += '  <rect class="bg" x="0" y="0" width="960" height="720" />\n'
    svg += f'  <text class="title" x="70" y="42">{chart["title"]}</text>\n'
    svg += f'  <text class="subtitle" x="70" y="72">{chart["subtitle"]}</text>\n'

    left, right, top, bottom = 80, 920, 95, 580

    # Compute stacked totals
    n_pts = min(len(chart["years"]), min(len(s["data"]) for s in chart["series"]))
    n_series = len(chart["series"])
    stacked = [[0] * n_pts for _ in range(n_series + 1)]
    for si in range(n_series):
        for i in range(n_pts):
            stacked[si + 1][i] = stacked[si][i] + chart["series"][si]["data"][i]

    max_val = max(stacked[n_series])
    min_val = 0

    # Y grid
    n_grid = 6
    for i in range(n_grid + 1):
        y = top + i * (bottom - top) / n_grid
        v = max_val - i * max_val / n_grid
        svg += f'  <line class="axis-line" x1="{left}" y1="{y:.0f}" x2="{right}" y2="{y:.0f}" />\n'
        svg += f'  <text class="y-tick-label" x="{left - 8}" y="{y + 4:.0f}">{v:.1f}</text>\n'

    # X-axis labels
    years = chart["years"]
    step = max(1, n_pts // 8)
    for i in range(0, n_pts, step):
        x = left + i * (right - left) / (n_pts - 1) if n_pts > 1 else left
        svg += f'  <text class="tick-label" x="{x:.0f}" y="{bottom + 22}">{years[i]}</text>\n'

    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" />\n'
    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" />\n'

    # Draw areas (top to bottom so first series appears on top)
    for si in range(n_series - 1, -1, -1):
        color = chart["series"][si]["color"]
        upper_pts = []
        lower_pts = []
        for i in range(n_pts):
            x = left + i * (right - left) / (n_pts - 1) if n_pts > 1 else left
            y_upper = map_value(stacked[si + 1][i], min_val, max_val, top, bottom)
            y_lower = map_value(stacked[si][i], min_val, max_val, top, bottom)
            upper_pts.append(f"{x:.0f},{y_upper:.0f}")
            lower_pts.append(f"{x:.0f},{y_lower:.0f}")
        lower_pts.reverse()
        all_pts = " ".join(upper_pts + lower_pts)
        svg += f'  <polygon points="{all_pts}" fill="{color}" fill-opacity="0.7" stroke="{color}" stroke-width="1" />\n'

    # Legend
    ly = 650
    lx = left
    for i, s in enumerate(chart["series"]):
        x = lx + i * 180
        svg += f'  <rect x="{x}" y="{ly - 6}" width="14" height="14" fill="{s["color"]}" fill-opacity="0.7" />\n'
        svg += f'  <text class="legend-text" x="{x + 20}" y="{ly + 5}">{s["name"]}</text>\n'

    svg += svg_footer()
    return svg


def generate_bar_chart(chart):
    """Generate a horizontal bar chart SVG."""
    svg = svg_header()
    svg += CHART_STYLES.format()
    svg += '  <rect class="bg" x="0" y="0" width="960" height="720" />\n'
    svg += f'  <text class="title" x="130" y="42">{chart["title"]}</text>\n'
    svg += f'  <text class="subtitle" x="130" y="72">{chart["subtitle"]}</text>\n'

    items = chart["items"]
    n = len(items)
    label_width = 120
    left = label_width + 10
    right = 920
    top = 90
    bar_total_height = 580
    bar_height = min(22, bar_total_height / n * 0.7)
    gap = (bar_total_height - n * bar_height) / (n + 1)

    max_val = max(v for _, v in items)

    # Vertical grid lines
    for i in range(7):
        v = max_val * i / 6
        x = left + (v / max_val) * (right - left) if max_val > 0 else left
        svg += f'  <line class="axis-line" x1="{x:.0f}" y1="{top}" x2="{x:.0f}" y2="{top + bar_total_height}" />\n'

    # X-axis labels
    for i in range(7):
        v = max_val * i / 6
        x = left + (v / max_val) * (right - left) if max_val > 0 else left
        label = f"{v:.0f}" if v == int(v) else f"{v:.1f}"
        svg += f'  <text class="tick-label" x="{x:.0f}" y="{top + bar_total_height + 22}">{label}</text>\n'

    # Baseline
    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{top}" x2="{left}" y2="{top + bar_total_height}" />\n'

    # Bars
    colors_cycle = ["#E63946", "#457B9D", "#2A9D8F", "#E9C46A", "#F4A261", "#264653", "#6A0572", "#1D3557",
                     "#FF6B6B", "#4ECDC4", "#45B7D1", "#96CEB4", "#A29BFE", "#FD79A8", "#00B894", "#74B9FF"]

    for i, (label, val) in enumerate(items):
        y = top + gap + i * (bar_height + gap)
        w = (val / max_val) * (right - left) if max_val > 0 else 0
        color = colors_cycle[i % len(colors_cycle)]
        svg += f'  <rect x="{left}" y="{y:.0f}" width="{w:.0f}" height="{bar_height:.0f}" fill="{color}" />\n'
        svg += f'  <text class="bar-label" x="{left - 5}" y="{y + bar_height * 0.75:.0f}">{label}</text>\n'

    svg += svg_footer()
    return svg


def generate_oscillating_chart(chart):
    """Generate a line chart with positive/negative shading."""
    svg = svg_header()
    svg += CHART_STYLES.format()
    svg += '  <rect class="bg" x="0" y="0" width="960" height="720" />\n'
    svg += f'  <text class="title" x="70" y="42">{chart["title"]}</text>\n'
    svg += f'  <text class="subtitle" x="70" y="72">{chart["subtitle"]}</text>\n'

    left, right, top, bottom = 80, 920, 95, 580
    data = chart["series"][0]["data"]
    color = chart["series"][0]["color"]

    min_val = min(data)
    max_val = max(data)
    padding = (max_val - min_val) * 0.1 if max_val != min_val else 1
    min_val -= padding
    max_val += padding

    # Determine a "zero" or baseline
    baseline = 0 if min_val < 0 < max_val else (min_val + max_val) / 2
    baseline_y = map_value(baseline, min_val, max_val, top, bottom)

    # Y grid
    n_grid = 6
    for i in range(n_grid + 1):
        y = top + i * (bottom - top) / n_grid
        v = max_val - i * (max_val - min_val) / n_grid
        svg += f'  <line class="axis-line" x1="{left}" y1="{y:.0f}" x2="{right}" y2="{y:.0f}" />\n'
        svg += f'  <text class="y-tick-label" x="{left - 8}" y="{y + 4:.0f}">{v:.1f}</text>\n'

    # Baseline bold
    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{baseline_y:.0f}" x2="{right}" y2="{baseline_y:.0f}" />\n'

    # X-axis labels
    years = chart["years"]
    n_yrs = len(years)
    n_pts = len(data)
    step = max(1, n_yrs // 6)
    for yi in range(0, n_yrs, step):
        xi = int(yi * (n_pts - 1) / (n_yrs - 1)) if n_yrs > 1 else 0
        x = left + xi * (right - left) / (n_pts - 1) if n_pts > 1 else left
        svg += f'  <text class="tick-label" x="{x:.0f}" y="{bottom + 22}">{years[yi]}</text>\n'

    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{bottom}" x2="{right}" y2="{bottom}" />\n'
    svg += f'  <line class="axis-line-bold" x1="{left}" y1="{top}" x2="{left}" y2="{bottom}" />\n'

    # Draw filled areas above/below baseline
    pts_above = []
    pts_below = []
    for i, v in enumerate(data):
        x = left + i * (right - left) / (len(data) - 1) if len(data) > 1 else left
        y = map_value(v, min_val, max_val, top, bottom)
        if y <= baseline_y:
            pts_above.append((x, y))
        else:
            pts_below.append((x, y))

    # Draw main line
    pts = []
    for i, v in enumerate(data):
        x = left + i * (right - left) / (len(data) - 1) if len(data) > 1 else left
        y = map_value(v, min_val, max_val, top, bottom)
        pts.append(f"{x:.0f},{y:.0f}")
    svg += f'  <polyline points="{" ".join(pts)}" fill="none" stroke="{color}" stroke-width="2" />\n'

    svg += svg_footer()
    return svg


# ========== MAIN GENERATION ==========

def main():
    for chart in CHARTS:
        ctype = chart["type"]
        cid = chart["id"]
        safe_title = chart['title'].replace('/', '-').replace('\\', '-').replace(':', '-')
        filename = f"{cid:03d}. {safe_title}.svg"
        filepath = os.path.join(OUTPUT_DIR, filename)

        if ctype in ("line",):
            svg_content = generate_line_chart(chart)
        elif ctype in ("multiline",):
            svg_content = generate_line_chart(chart, multi=True)
        elif ctype == "area":
            svg_content = generate_area_chart(chart)
        elif ctype == "bar":
            svg_content = generate_bar_chart(chart)
        elif ctype == "oscillating":
            svg_content = generate_oscillating_chart(chart)
        else:
            svg_content = generate_line_chart(chart)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(svg_content)

        print(f"Generated: {filename}")

    print(f"\nDone! Generated {len(CHARTS)} SVG files in {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
