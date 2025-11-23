<div align="center">

# FoodInsight Agent

### Agente Inteligente de Mercado para Food Delivery

<!-- LANGUAGE SWITCHER -->
[![Read in English](https://img.shields.io/badge/Read%20in-English-0077B5?style=for-the-badge&logo=google-translate&logoColor=white)](README.md)

<!-- TECH STACK BADGES -->
<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Orchestration-CrewAI-orange" alt="CrewAI">
  <img src="https://img.shields.io/badge/Inference-Llama%203.3-purple" alt="Llama 3.3">
</p>

<!-- MAIN IMAGE -->
<!-- Substitua o caminho abaixo pela imagem real se houver, ou remova esta linha -->
<img src="assets/foodinsight_demo.png" alt="Fluxo FoodInsight" width="100%">

*Arquitetura de Agentes de IA para P&D Automatizado em Delivery.*

</div>

---

## Sobre
O **FoodInsight** é uma arquitetura de agentes de IA projetada para acelerar o ciclo de inovação em *delivery*. O sistema simula uma esteira de P&D (Pesquisa e Desenvolvimento), varrendo redes sociais em busca de tendências virais de comidas, estruturando os dados e transformando-os em possíveis produtos.

Enfrentei alguns desafios na sua produção que, apesar das dificuldades, me proporcionaram uma boa experiência ao resolvê-los. Esta foi minha primeira implementação de um agente e me abriu os olhos para o potencial dessa ferramenta em outros projetos.

A ideia de nomear o agente explorador de **Huginn** ocorreu-me ao pensar nele como um mensageiro. Na mitologia nórdica, Huginn representa o "pensamento" e, através dele, Odin coletava dados sobre todas as coisas no mundo.

---

## Arquitetura

O projeto implementa o padrão de orquestração **CrewAI**, coordenando três agentes especializados que atuam sequencialmente:

1.  **Huginn (Trend Scout):**
    *   *Função:* Agente explorador que utiliza *Google Search Operators* para minerar micro-tendências no TikTok e Instagram.
    *   *Tecnologia:* Integração com SerperDev API e lógica estocástica para variação de busca.
2.  **Menu Engineer:**
    *   *Função:* Analisa a viabilidade técnica, custos e logística de transporte (embalagem) dos produtos sugeridos.
3.  **Delivery Copywriter:**
    *   *Função:* Gera metadados otimizados para conversão (SEO, Descrições Sensoriais) seguindo templates rígidos de UX Writing.

---

## Desenvolvimento

Abaixo, documento os principais desafios técnicos enfrentados e as soluções aplicadas:

### 1. Conflito Grave de Dependências (urllib3)
*   **Desafio:** A instalação de bibliotecas como Selenium e Kubernetes gerou conflitos no `urllib3`. O Selenium exigia versão `>= 2.5.0` e o Kubernetes exigia `< 2.4.0`. Sem uma versão capaz de satisfazer ambas, o ambiente tornava-se instável.
*   **Solução:** Isolei ambientes de execução, criando *virtual environments* independentes para cada conjunto de dependências, permitindo que cada biblioteca operasse com sua versão compatível.

### 2. Contexto Insuficiente (Tempo Real)
*   **Desafio:** Modelos de IA (LLMs) não possuem conhecimento em tempo real, o que inviabilizaria o projeto, cujo objetivo é identificar o que está em alta nas redes agora.
*   **Solução:** Inseri um mecanismo de pesquisa via API do **Serper**, servindo como ponte entre a IA e os resultados do Google.

### 3. O Problema da Repetição (Loop de Alucinação)
*   **Desafio:** Inicialmente, o agente entrava em um viés de confirmação, sugerindo repetidamente o mesmo produto (ex: "Morango do Amor") devido ao cache agressivo do framework e *prompts* estáticos.
*   **Solução:** Implementação de rotação aleatória de tópicos de busca (`search_angles`) combinada com a desativação programática do cache (`cache=False`) e *seed* baseada em timestamp. Isso forçou a entropia do sistema, garantindo resultados inéditos a cada execução.

### 4. Rate Limiting e Depreciação de Modelos
*   **Desafio:** Durante testes de estresse, atingimos o *Rate Limit* (TPD) da API da Groq e enfrentamos a depreciação súbita do modelo `llama-3-70b`.
*   **Solução:**
    *   Migração imediata para o modelo `llama-3.3-70b-versatile`.
    *   Criação de uma classe de configuração (`AppConfig`) robusta para facilitar a troca rápida de modelos (Fallback para 8B) e validação de variáveis de ambiente.

### 5. Alinhamento de Expectativa (Prompt Engineering)
*   **Desafio:** O agente de marketing gerava nomes abstratos ("GlobeBite") que não performam bem em apps de delivery, onde a clareza é essencial.
*   **Solução:** Refinamento das *System Instructions*. Definimos regras rígidas de formatação e um conceito "Híbrido" (Nome Descritivo + Diferencial Premium), além de proibir a criação de seções de texto isoladas para a embalagem, forçando uma narrativa fluida.

> *Nota do Autor: Solucionar estas problemáticas encareceu o custo de processamento (tokens). Numa aplicação real, é necessário ponderar os custos do agente versus o retorno (ROI), podendo ser necessários ajustes para baratear a operação.*

---

## Resultados

📂 **[Para visualizar os resultados gerados pelo Huginn clique aqui](sample)**

---

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone https://github.com/umbura/foodinsight-agent.git
    cd foodinsight-agent
    ```

2.  **Configure o ambiente:**
    ```bash
    python -m venv .venv
    ```
    *Certifique-se de ativar o ambiente virtual antes de instalar as dependências.*
    ```bash
    pip install -r requirements.txt
    ```
    *Obs: Caso não consiga executar o script, pode ser necessário ajustar temporariamente a política de execução de scripts do seu sistema.*

3.  **Configuração de API:**
    Crie um arquivo `.env` na raiz do projeto e insira a API Key da IA que pretende utilizar (Ex: Groq, OpenAI, VertexAI):
    ```bash
    GROQ_API_KEY=gsk_...
    SERPER_API_KEY=...
    ```

4.  **Execute com Python:**
    Rode o script principal.

---

## Tech Stack

*   **Linguagem:** Python 3.10+
*   **Framework:** CrewAI (Multi-Agent Systems)
*   **LLM Engine:** Llama 3.3 70B via Groq (Selecionado pela latência <1s e alta capacidade de raciocínio).
*   **Tools:** SerperDev (Web Search & Social Listening).
*   **Segurança:** Gerenciamento de segredos via `.env` e validação de tipos.

## License
Distribuído sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
