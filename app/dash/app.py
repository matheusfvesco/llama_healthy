from flask import Flask, render_template, request
import pandas as pd
import folium
import base64
from dash.tasks import state_coordinates, filter_data
from dash.tasks.generate_report import generate_report 
from dotenv import load_dotenv 
import os

load_dotenv()

app = Flask(__name__)

def load_data():
    data = pd.read_csv('../last_month_processed.tsv', sep='\t')
    return data


@app.route('/')
def dashboard():
    data = load_data()

    prompt = request.args.get('prompt')
    print(f"Prompt for filtering: {prompt}")
    if prompt:
        api_key = os.getenv("GROQ_API_KEY")

        time_filter = filter_data.interpret_time_filter(prompt, api_key)
        
        if time_filter:

            data = filter_data.filter_data_by_time(data, time_filter)
            print(f"Data filtered by time: {data.head()}")
        else:
            print("Failed to interpret time filter; using full data set.")

    api_key = os.getenv("GROQ_API_KEY")
    report_text = generate_report(data, api_key)

    uf_counts = data['SG_UF_NOT'].value_counts().sort_index().to_dict()
    sexo_counts = data['CS_SEXO'].value_counts().to_dict()
    evolucao_data = data[data['evolucao'].isin(['cura', 'obito'])]
    evolucao_counts = evolucao_data.groupby(['DT_NOTIFIC', 'evolucao']).size().unstack(fill_value=0).to_dict(orient='list')
    dates_evolucao = evolucao_data['DT_NOTIFIC'].sort_values().unique().tolist()

    folium_map = folium.Map(location=[-25.7797, -40.9297], zoom_start=5)
    for uf, group in data.groupby('SG_UF_NOT'):
        location = state_coordinates.get(uf)
        if location:
        
            influenza_data = group[group['classi_fin'] == 'influenza']
            influenza_counts = influenza_data.groupby('DT_NOTIFIC').size().tolist()
            dates = influenza_data['DT_NOTIFIC'].unique().tolist()

            chart_html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
            </head>
            <body>
                <canvas id="myChart" width="400" height="300"></canvas>
                <script>
                    var ctx = document.getElementById('myChart').getContext('2d');
                    new Chart(ctx, {{
                        type: 'bar',
                        data: {{
                            labels: {dates},
                            datasets: [{{
                                label: 'Casos de Influenza',
                                data: {influenza_counts},
                                backgroundColor: 'rgba(75, 192, 192, 0.6)',
                                borderColor: 'rgba(75, 192, 192, 1)',
                                borderWidth: 1
                            }}]
                        }},
                        options: {{
                            responsive: true,
                            plugins: {{
                                legend: {{ display: true }}
                            }},
                            scales: {{
                                x: {{
                                    grid: {{ display: false }},  // Remove grid from x-axi
                                    ticks: {{
                                        font: {{
                                            size: 10
                                        }},
                                        maxRotation: 90,
                                        minRotation: 90
                                    }}
                                }},
                                y: {{
                                    grid: {{ display: false }},  // Remove grid from x-axi
                                    beginAtZero: true
                                }}
                            }}
                        }}
                    }});
                </script>
            </body>
            </html>
            """
            
            encoded_html = base64.b64encode(chart_html.encode('utf-8')).decode('utf-8')
            data_uri = f"data:text/html;base64,{encoded_html}"

            iframe = folium.IFrame(f'<iframe src="{data_uri}" width="400" height="350"></iframe>', width=400, height=350)
            popup = folium.Popup(iframe, max_width=500)
            marker = folium.Marker(location=location, popup=popup)
            marker.add_to(folium_map)

    map_html = folium_map._repr_html_()

    return render_template(
        'dash.html',
        uf_counts=uf_counts,
        sexo_counts=sexo_counts,
        evolucao_counts=evolucao_counts,
        dates_evolucao=dates_evolucao,
        map_html=map_html,
        report_text=report_text
    )

if __name__ == '__main__':
    app.run(debug=True)
