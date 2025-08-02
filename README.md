# Assistente de Entrevista IA 🎙️🤖

Um assistente em tempo real para entrevistas de emprego por telechamada, otimizado para velocidade e precisão. O programa escuta o áudio da chamada, envia para a API do Google Gemini e exibe uma resposta sugerida palavra por palavra em uma interface gráfica limpa.

O objetivo é fornecer ao entrevistado sugestões de respostas de alta qualidade de forma rápida e imperceptível, servindo como um "teleprompter" inteligente.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

---

## ✨ Funcionalidades Principais

*   **Captura de Áudio Multiplataforma Automática:** Utiliza a biblioteca `soundcard` para detectar e gravar automaticamente o áudio da saída do seu sistema (loopback), eliminando a necessidade de configurações manuais complexas.
*   **Respostas em Tempo Real (Streaming):** Exibe a resposta da IA palavra por palavra à medida que é gerada, melhorando drasticamente a percepção de velocidade e permitindo uma leitura mais natural.
*   **Otimizado para Velocidade:** A captura de áudio é configurada para fala (16kHz, mono), reduzindo o tamanho dos dados enviados e acelerando o tempo de resposta da API.
*   **IA Direta e Profissional:** O prompt foi cuidadosamente elaborado para que a IA gere respostas concisas e diretas, sem introduções ou frases desnecessárias.
*   **Interface Moderna e Leve:** Construído com `CustomTkinter` para uma aparência limpa, moderna e responsiva.
*   **Seguro e Portátil:** Mantém a chave de API fora do código-fonte através de um arquivo `.env` e gerencia as dependências com um `requirements.txt`.

---

## 🛠️ Instalação e Configuração

O projeto foi projetado para ser multiplataforma (testado em Linux e Windows).

#### **1. Clonar o Repositório**
```bash
git clone https://github.com/kauan-kyoshi/IntervCodeAI.git IntervCodeAI
cd IntervCodeAI
```

#### **2. Criar e Ativar um Ambiente Virtual**
É altamente recomendado usar um ambiente virtual para isolar as dependências.

*   **Linux / macOS:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```
*   **Windows (PowerShell):**
    ```powershell
    py -m venv venv
    .\venv\Scripts\activate
    ```

#### **3. Instalar Dependências**
*   **Linux (Sistemas baseados em Debian/Ubuntu):**
    Pode ser necessário instalar as seguintes dependências do sistema, se ainda não as tiver:
    ```bash
    sudo apt-get update
    sudo apt-get install libportaudio2 python3-tk
    ```
*   **Instalar as dependências do Python (para todos os sistemas):**
    ```bash
    pip install -r requirements.txt
    ```

#### **4. Configurar a Chave de API**
1.  Obtenha sua chave de API gratuita no [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Na pasta do projeto, renomeie o arquivo de exemplo `.env.example` para `.env`.
3.  Abra o arquivo `.env` com um editor de texto e cole sua chave de API:
    ```    GEMINI_API_KEY=SUA_CHAVE_DE_API_VAI_AQUI
    ```

---

## 🚀 Como Usar

A configuração de áudio é totalmente automática. O programa irá detectar sua saída de áudio padrão (fones de ouvido/alto-falantes) e gravá-la.

1.  Garanta que o áudio da sua entrevista (ou qualquer fonte de áudio para teste) esteja tocando no seu sistema.
2.  Execute o programa:
    ```bash
    # Em Linux/macOS
    python3 src/main.py

    # Em Windows
    python src\main.py
    ```
3.  Quando o entrevistador fizer uma pergunta, clique em **"Ouvir Pergunta"**.
4.  Quando ele terminar de falar, clique em **"Parar"**.
5.  A resposta da IA começará a aparecer na tela em tempo real.

---

## ⚙️ Tecnologias Utilizadas

*   **Linguagem:** Python 3
*   **IA Generativa:** Google Gemini API
*   **Interface Gráfica:** CustomTkinter
*   **Captura de Áudio:** SoundCard
*   **Processamento de Dados:** NumPy

---

## ⚠️ Aviso Ético

Este projeto foi desenvolvido como uma prova de conceito tecnológica e uma ferramenta de auxílio. Seu uso em entrevistas reais sem o consentimento do entrevistador pode ser considerado antiético e pode violar as políticas da empresa.

Recomenda-se usar esta ferramenta para **praticar**, **estudar** possíveis respostas ou com **total transparência** durante a entrevista. A responsabilidade pelo uso ético do software é inteiramente sua.

---

## 📜 Licença

Este projeto está licenciado sob a Licença MIT. Veja o arquivo `LICENSE` para mais detalhes.````