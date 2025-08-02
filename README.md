# IntervCodeAI

# Assistente de Entrevista IA 🎙️🤖

Um assistente em tempo real para entrevistas de emprego por telechamada. O programa escuta o áudio da chamada (a pergunta do entrevistador), envia para a API do Google Gemini e exibe uma resposta sugerida em uma interface gráfica para o usuário ler.

O objetivo é fornecer ao entrevistado sugestões de respostas de alta qualidade de forma rápida e imperceptível.

---

## ✨ Funcionalidades

*   **Captura de Áudio do Sistema:** Escuta o áudio que está sendo reproduzido no sistema (saída de fone de ouvido/alto-falante), não o microfone.
*   **Integração com Gemini API:** Utiliza o modelo `gemini-1.5-flash` para processamento rápido de áudio e geração de texto.
*   **Interface Gráfica Moderna:** Construído com `CustomTkinter` para uma aparência limpa e agradável (incluindo tema escuro).
*   **Seguro:** Mantém a chave de API fora do código-fonte usando um arquivo `.env`.
*   **Multi-thread:** A captura de áudio e as chamadas de API rodam em threads separadas para que a interface nunca trave.

---

## 🛠️ Instalação e Configuração

Este guia foi testado em sistemas baseados em Debian (como Ubuntu). Os passos podem variar para outros sistemas operacionais.

#### **1. Clonar o Repositório**
```bash
git clone https://github.com/kauan-kyoshi/IntervCodeAI.git IntervCodeAI
cd IntervCodeAI
```

#### **2. Criar e Ativar um Ambiente Virtual**
É altamente recomendado usar um ambiente virtual para isolar as dependências.
```bash
# Usar python3 ou python, dependendo do seu sistema
python3 -m venv venv
source venv/bin/activate
```

#### **3. Instalar Dependências do Sistema**
O `PyAudio` requer algumas bibliotecas do sistema para funcionar.
```bash
sudo apt-get update
sudo apt-get install portaudio19-dev python3-tk
```

#### **4. Instalar Dependências do Python**
```bash
pip install -r requirements.txt
```

#### **5. Configurar a Chave de API**
Você precisa de uma chave de API do Google Gemini.

1.  Obtenha sua chave no [Google AI Studio](https://aistudio.google.com/app/apikey).
2.  Renomeie o arquivo de exemplo `.env.example` para `.env`:
    ```bash
    mv .env.example .env
    ```
3.  Abra o arquivo `.env` com um editor de texto e cole sua chave de API:
    ```
    GEMINI_API_KEY=SUA_CHAVE_DE_API_VAI_AQUI
    ```

---

## 🚀 Como Usar

#### **1. Configurar a Captura de Áudio (Loopback)**
O passo mais importante é dizer ao programa para gravar o áudio da **saída** do seu sistema, e não da entrada (microfone). A forma mais fácil é usando o `pavucontrol`.

1.  Instale o `pavucontrol`: `sudo apt-get install pavucontrol`
2.  Comece a tocar um áudio (ex: um vídeo no YouTube).
3.  Abra o `pavucontrol`.
4.  Execute o assistente de entrevista: `python3 src/main.py`.
5.  No assistente, clique no botão **"Ouvir Pergunta"**.
6.  **Rapidamente**, volte para o `pavucontrol` e vá para a aba **"Gravação"**. Você verá sua aplicação Python listada.
7.  Clique no botão ao lado dela (que provavelmente mostra seu microfone) e selecione a opção **"Monitor of [Sua Placa de Som]"**.

#### **2. (Opcional) Configurar o Índice do Dispositivo Manualmente**
Se preferir, você pode definir o dispositivo "Monitor" diretamente no código.

1.  Execute o script auxiliar para listar seus dispositivos de gravação:
    ```bash
    python3 src/list_devices.py
    ```
2.  Procure o índice numérico do dispositivo com "monitor" no nome.
3.  Abra o arquivo `src/main.py`, encontre a linha `INPUT_DEVICE_INDEX = None` e substitua `None` pelo número do índice que você encontrou.

#### **3. Executar o Programa**
Com tudo configurado, basta executar:
```bash
python3 src/main.py
```
Clique em "Ouvir Pergunta" quando o entrevistador falar e em "Parar" quando ele terminar para receber a sugestão de resposta.
