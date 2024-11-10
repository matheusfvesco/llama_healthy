# Suporte para Vigilância Epidemiológica com Dados do DATASUS

Esse projeto oferece um sistema de visualização e análise de dados voltado para apoiar a vigilância epidemiológica no Brasil, com foco nos dados do DATASUS. Ao integrar dados como sintomas, comorbidades e evolução de casos, a plataforma permite uma análise rápida e abrangente de frequências e distribuições regionais, auxiliando na tomada de decisões para saúde pública. A capacidade de filtrar dados por critérios específicos e gerar relatórios em tempo real aprimora a eficiência na resposta a surtos e a identificação de tendências epidemiológicas.

## Funcionalidades

- Visualização interativa de dados com mapas e gráficos.
- Filtros de dados por tempo e variáveis epidemiológicas.
- Geração de relatórios automatizados baseados em prompts.
- Análise de frequência de sintomas e comorbidades.
- Funcionalidade de leitura de texto em português para acessibilidade.

## Tecnologias Utilizadas

- **Python**: Linguagem principal.
- **Flask**: Framework para desenvolvimento da API e renderização de páginas.
- **Pandas**: Manipulação e análise de dados.
- **Folium**: Geração de mapas interativos.
- **Matplotlib** e **Chart.js**: Visualização gráfica dos dados.
- **Requests**: Conexão com APIs externas.

## Requisitos

Antes de rodar o projeto, certifique-se de ter as dependências instaladas. Você pode instalá-las a partir do `requirements.txt` com:

```bash
pip install -r requirements.txt
```

## Configuração e Uso

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/seu_usuario/nome_do_repositorio.git
   cd nome_do_repositorio
   ```

2. **Instale as dependências**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configuração de Variáveis de Ambiente**:
   Insira sua chave de API e outras variáveis necessárias no ambiente. Exemplo para um arquivo `.env`:

   ```plaintext
   GROQ_API_KEY="sua_chave_de_api"
   ```

4. **Inicie o servidor**:

   ```bash
   flask run
   ```

5. **Acesse a aplicação**: Abra o navegador e vá para `http://127.0.0.1:5000`.

## Estrutura do Projeto

- `app.py`: Arquivo principal da aplicação, gerencia rotas e renderiza o dashboard.
- `dash/tasks/filter_data.py`: Funções para filtrar dados conforme o prompt do usuário.
- `dash/tasks/generate_report.py`: Gera relatórios de acordo com as necessidades de vigilância.
- `templates/`: Contém o layout HTML para o dashboard.
- `static/`: Arquivos de estilo CSS e JavaScript para interatividade da interface.
