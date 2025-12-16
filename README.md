Seoul Bike Sharing Demand Analysis
📌 Project Overview

This project analyzes bike-sharing usage patterns in Seoul to support data-driven operational and promotional decisions.
The analysis focuses on identifying differences in bike rental demand across time, weather conditions, seasons, and holidays, with the goal of improving bike availability during peak hours and optimizing promotional strategies.

This project was developed as an end-to-end Data Analyst case study, combining exploratory analysis, statistical testing, business insights, and stakeholder-facing visualization.

🎯 Business Problem

Bike-sharing demand in Seoul fluctuates significantly depending on:

time of day,

weekday versus holiday usage,

weather conditions, and

seasonal patterns.

Without data-driven insights, operators risk:

bike shortages during peak commuting hours,

underutilized resources during low-demand periods, and

ineffective promotional strategies.

Key question:

How can bike-sharing operators optimize bike availability and promotional strategies based on usage patterns and external factors?

🧠 Business Objectives

Understand demand patterns across time, weather, and holidays

Identify behavioral differences between weekday and holiday users

Provide actionable, data-driven recommendations for operational optimization

📊 Dataset Overview

Dataset: Seoul Bike Sharing Demand

Source: UCI Machine Learning Repository

Time Period: December 2017 – November 2018

Granularity: Hourly data

Target Variable: Rented Bike Count

Key features include weather variables, seasonal indicators, holiday flags, and time-based attributes.

🔍 Analytical Approach

The analysis followed a structured data analytics workflow:

Data understanding and validation

Exploratory Data Analysis (EDA)

Time-based pattern analysis (hourly, daily, seasonal)

Comparison between weekday and holiday usage

Statistical validation using A/B Testing

Business interpretation and recommendation formulation

The focus of this project is decision support, not predictive modeling.

📈 Key Insights

Weekday vs Holiday Patterns
Weekdays show strong commuting behavior with demand peaks during morning (07.00–09.00) and evening (17.00–18.00) hours, while holiday usage is more evenly distributed.

Weather & Temperature Effects
Bike rental demand has a moderate positive correlation with temperature. Rainfall and extreme weather conditions consistently reduce usage.

Seasonality
Demand increases from spring, peaks during summer, and declines significantly in winter.

Statistical Validation
A/B testing confirms that differences in demand across weekdays vs holidays, peak vs non-peak hours, and seasonal conditions are statistically significant.

💡 Business Recommendations
Operational Optimization

Increase bike availability during weekday morning rush hours (07.00–09.00).

Adjust promotional strategies for holidays and clear-weather afternoons.

Incorporate daily weather forecasts into operational planning.

Example Scenario

Average weekday demand (07.00–09.00): ~2,336 rentals

Recommended buffer (10%): ~2,570 bikes

Additional bikes needed: ~234 units

These actions can improve bike availability during peak periods and enhance customer experience.

🛠 Tools & Technologies

Data Analysis: Python (Google Colab)

Visualization & Dashboard: Power BI

Statistical Analysis: A/B Testing (t-test)

Planned Deployment: Streamlit (public-facing analytics app)

📦 Project Structure
seoul-bike-sharing-demand-analysis/
├─ app/            # Streamlit application
├─ notebooks/      # Google Colab notebook (.ipynb)
├─ powerbi/        # Dashboard screenshots & notes
├─ data/           # Dataset or data instructions
├─ requirements.txt
└─ README.md

🚀 Deliverables

Exploratory data analysis and business insights

Interactive Power BI dashboard for stakeholder analysis

Business recommendations supported by data

Planned Streamlit application for public access

⚠️ Limitations & Future Improvements

Limitations

Analysis is based on historical data from a single year

External factors such as city events are not included

Future Improvements

Integration of real-time weather and event data

Demand forecasting models

Interactive operational planning via Streamlit

🔗 Links

📊 Power BI Dashboard (screenshot available in /powerbi)

🌐 Streamlit App (to be deployed)

👤 Author

[Your Name]
Data Analyst
📧 Email | 🔗 LinkedIn | 💻 GitHub
