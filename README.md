# 🌸 Elysia (爱莉希雅) - Chinese Learning Bot

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Discord.py](https://img.shields.io/badge/Discord.py-2.0%2B-5865F2?logo=discord&logoColor=white)
![Status](https://img.shields.io/badge/Status-Online-success)

**Elysia** é um bot de Discord interativo e moderno focado no ensino de Mandarim (Chinês). Baseado no projeto *ChineseLessons*, este bot transforma o estudo em um jogo contínuo (Gamification), utilizando áudio gerado em tempo real, banco de dados para progresso e exercícios infinitos.

---

## ✨ Funcionalidades Principais

* **🗣️ Pronúncia Nativa (TTS):** Integração com `gTTS` para gerar áudio de qualquer palavra ou frase em chinês instantaneamente.
* **♾️ Modo Estudo Contínuo:** Sistema de Flashcards que nunca para. Estude centenas de palavras sem interrupções.
* **🧠 Quiz Infinito:** Jogos de múltipla escolha gerados proceduralmente baseados no vocabulário do banco de dados.
* **📈 Sistema de RPG (XP & Níveis):**
  * Ganhe XP estudando e acertando questões.
  * Suba de nível e acompanhe seu progresso no cartão de estudante.
  * Ranking global dos melhores alunos.
* **💾 Banco de Dados Robusto:** Utiliza `SQLite` (via `aiosqlite`) para salvar dados de forma assíncrona e segura.
* **📂 Categorias Dinâmicas:** Vocabulário organizado em Profissões, Cores, Alimentos, HSK1, etc.

---

## 🛠️ Tecnologias Utilizadas

* **Linguagem:** Python 3.10+
* **Core:** `discord.py` (Interactions & Slash Commands)
* **Database:** `aiosqlite` (SQLite assíncrono)
* **Áudio:** `gTTS` (Google Text-to-Speech)
* **Gestão de Variáveis:** `python-dotenv`

---

## 🚀 Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/PedroZxK/ChineseLessons.git
cd ChineseLessons
```

### 2. Instale as dependências

```bash
pip install discord.py aiosqlite gTTS python-dotenv
```

> **Nota:** É necessário ter o **FFmpeg** instalado no sistema apenas se for usar canais de voz futuramente. Para envio de arquivos MP3 no chat, as bibliotecas acima já são suficientes.

### 3. Configuração de Segurança

Crie um arquivo chamado `.env` na raiz do projeto e adicione o token do seu bot:

```env
DISCORD_TOKEN=SEU_TOKEN_DO_DISCORD_AQUI
```

> ⚠️ **Nunca compartilhe este arquivo publicamente.**

### 4. Inicie a Elysia

```bash
python main.py
```

