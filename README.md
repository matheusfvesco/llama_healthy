# Support for Epidemiological Surveillance with DATASUS Data

This project provides a data visualization and analysis system designed to support epidemiological surveillance in Brazil, focusing on DATASUS data. By integrating data such as symptoms, comorbidities, and case progression, the platform enables quick and comprehensive analysis of frequencies and regional distributions, aiding in public health decision-making. The ability to filter data by specific criteria and generate real-time reports enhances response efficiency to outbreaks and the identification of epidemiological trends.

## Features

- Interactive data visualization with maps and charts.
- Data filters by time and epidemiological variables.
- Automated report generation based on prompts.
- Symptom and comorbidity frequency analysis.
- Portuguese text-to-speech functionality for accessibility.

## Technologies Used

- **Python**: Primary programming language.
- **Flask**: Framework for API development and page rendering.
- **Pandas**: Data manipulation and analysis.
- **Folium**: Generation of interactive maps.
- **Matplotlib** and **Chart.js**: Data visualization.
- **Requests**: External API connection.

## Requirements

Before running the project, ensure that dependencies are installed. You can install them from `requirements.txt` with:

```bash
pip install -r requirements.txt
```

## Setup and Usage

1. **Clone the repository**:

   ```bash
   git clone https://github.com/your_username/repository_name.git
   cd repository_name
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Variable Configuration**:
   Insert your API key and other necessary variables into the environment. Example for a `.env` file:

   ```plaintext
   GROQ_API_KEY="your_api_key"
   ```

4. **Start the server**:

   ```bash
   flask run
   ```

5. **Access the application**: Open your browser and go to `http://127.0.0.1:5000`.

## Project Structure

- `app.py`: Main application file, manages routes, and renders the dashboard.
- `dash/tasks/filter_data.py`: Functions to filter data based on user prompts.
- `dash/tasks/generate_report.py`: Generates reports according to surveillance needs.
- `templates/`: Contains the HTML layout for the dashboard.
- `static/`: CSS and JavaScript files for interface interactivity.
