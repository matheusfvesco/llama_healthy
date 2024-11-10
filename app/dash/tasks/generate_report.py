import requests
import json

def generate_report(data, api_key):
 
    state_cases = data['SG_UF_NOT'].value_counts().reset_index()
    state_cases.columns = ['state', 'cases']

    gender_cases = data['CS_SEXO'].value_counts().reset_index()
    gender_cases.columns = ['gender', 'cases']

    date_cases = data.groupby('DT_NOTIFIC').size().reset_index(name='cases')

    influenza_cases = (
        data[(data['classi_fin'] == 'influenza') & (data['SG_UF_NOT'].notna())]
        .groupby('SG_UF_NOT')
        .size()
        .reset_index(name='influenza_cases')
    )

    summary_data = {
        "state_cases": state_cases.to_dict(orient="records"),
        "gender_cases": gender_cases.to_dict(orient="records"),
        "date_cases": date_cases.to_dict(orient="records"),
        "influenza_cases": influenza_cases.to_dict(orient="records")
    }

    prompt = (
        "Gere um relatório em um parágrafo, diretamente com o conteúdo claro e conciso, contendo no máximo 500 caracteres. "
        "O relatório deve resumir a distribuição dos casos de COVID-19 por estado, destacando os estados com maior e menor número de casos, "
        "a distribuição por gênero, a evolução dos casos ao longo do tempo e um resumo dos casos de influenza observados. "
        # "Quando for o caso, destaque os estados com maiores picos de casos de influenza. "
        "quando for o caso de muitos estados, destaque apenas dois no máximo. "
        # "Sempre respeite o maximo de tokens e nunca corte pela metade uma palavra. "
        # "Finalize com recomendações curtas para vigilância e prevenção.\n\n"
        "Aqui estão os dados:\n"
        f"{json.dumps(summary_data, indent=2)}"
    )

    # Configure API request
    api_url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}"
    }
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
        # "max_tokens": 150
    }

    # Send request to Groq API
    response = requests.post(api_url, headers=headers, json=payload)

    if response.status_code == 200:
        report_text = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return report_text
    else:
        print(f"Erro: {response.status_code} - {response.text}")
        return "Erro ao gerar o relatório."
