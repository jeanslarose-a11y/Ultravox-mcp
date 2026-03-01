# 🎤 Ultravox MCP Server

> 🇫🇷 **Français** | 🇬🇧 [English below](#-ultravox-mcp-server--english)

Serveur MCP (Model Context Protocol) pour l'API [Ultravox](https://ultravox.ai) — compatible **Claude Desktop** (stdio) et **Claude.ai / n8n** (HTTP). Fonctionne facilement avec votre agent **[OpenClaw](https://openclaw.ai)**.

Développé par [Mak3it AI Technologie](https://mak3it.com) — Solutions IA souveraines au Québec. 🍁

---

## 🎬 Démo vidéo / Video Demo

[![Ultravox MCP Server - Démo par Mak3it AI](https://img.youtube.com/vi/V0v74xxrmI8/maxresdefault.jpg)](https://www.youtube.com/watch?v=V0v74xxrmI8&t=3s)

▶️ [Voir la démo sur YouTube / Watch Demo on YouTube](https://www.youtube.com/watch?v=V0v74xxrmI8&t=3s)

---

## ✨ Fonctionnalités

- ✅ **Dual transport** : stdio (local) + SSE/streamable-http (remote)
- 📞 **Appels** : lister, détailler, transcrire, enregistrer, supprimer
- 🤖 **Agents** : lister, configurer, mettre à jour le prompt, supprimer
- 🎙️ **Voix** : lister toutes les voix disponibles
- 🧠 **Modèles** : lister les LLMs disponibles
- 🔧 **Outils** : gérer les outils personnalisés des agents
- 🪝 **Webhooks** : créer, lister, supprimer
- 📊 **Usage** : statistiques d'utilisation

---

## 🚀 Installation

### Prérequis

```bash
pip install fastmcp httpx python-dotenv
```

### Configuration

Crée un fichier `.env` dans le même dossier :

```env
ULTRAVOX_API_KEY=votre_cle_api_ultravox
```

---

## 🖥️ Utilisation

### Mode stdio — Claude Desktop

```bash
python ultravox_mcp.py
```

**`claude_desktop_config.json`** :

```json
{
  "mcpServers": {
    "ultravox": {
      "command": "python",
      "args": ["C:\\chemin\\vers\\ultravox_mcp.py"],
      "env": {
        "ULTRAVOX_API_KEY": "votre_cle_api"
      }
    }
  }
}
```

### Mode SSE — Claude.ai / n8n / Web

```bash
python ultravox_mcp.py --transport sse --port 8000
```

URL de connexion : `http://votre-serveur:8000/sse`

### Mode streamable-http — Standard moderne

```bash
python ultravox_mcp.py --transport streamable-http --port 8000
```

URL de connexion : `http://votre-serveur:8000/mcp`

### Via variables d'environnement

```bash
MCP_TRANSPORT=sse MCP_PORT=8000 ULTRAVOX_API_KEY=xxx python ultravox_mcp.py
```

---

## 🛠️ Outils MCP disponibles (22 tools)

| Catégorie | Outil | Description |
|-----------|-------|-------------|
| Compte | `get_account_info` | Infos du compte |
| Appels | `list_calls` | Liste des appels |
| Appels | `get_call` | Détails d'un appel |
| Appels | `get_call_messages` | Transcription complète |
| Appels | `get_call_recording` | URL enregistrement audio |
| Appels | `get_call_stages` | Étapes d'un appel |
| Appels | `get_call_tools` | Outils utilisés dans un appel |
| Appels | `get_call_usage` | Statistiques d'utilisation |
| Appels | `delete_call` | Supprimer un appel |
| Appels | `get_deleted_calls` | Appels supprimés |
| Agents | `list_agents` | Liste des agents |
| Agents | `get_agent` | Détails d'un agent |
| Agents | `list_agent_calls` | Appels d'un agent |
| Agents | `update_agent_prompt` | Modifier le prompt système |
| Agents | `delete_agent` | Supprimer un agent |
| Voix | `list_voices` | Voix disponibles |
| Voix | `get_voice` | Détails d'une voix |
| Modèles | `list_models` | LLMs disponibles |
| Outils | `list_tools` | Outils personnalisés |
| Outils | `get_tool` | Détails d'un outil |
| Webhooks | `list_webhooks` | Liste des webhooks |
| Webhooks | `get_webhook` | Détails d'un webhook |
| Webhooks | `create_webhook` | Créer un webhook |
| Webhooks | `delete_webhook` | Supprimer un webhook |
| API | `get_open_api_schema` | Schéma OpenAPI Ultravox |

---

## 📦 Structure du projet

```
ultravox-mcp/
├── ultravox_mcp.py    # Serveur MCP principal
├── .env               # Clé API (ne pas committer !)
├── .env.example       # Exemple de configuration
└── README.md
```

---

## 🏢 À propos

Développé par **Mak3it AI Technologie** — Jean-Sébastien Larose Québec 🍁

---

# 🎤 Ultravox MCP Server — English

> 🇬🇧 **English** | 🇫🇷 [Français ci-dessus](#-ultravox-mcp-server)

MCP (Model Context Protocol) server for the [Ultravox](https://ultravox.ai) API — compatible with **Claude Desktop** (stdio) and **Claude.ai / n8n** (HTTP). Works seamlessly with your **[OpenClaw](https://openclaw.ai)** agent.

Developed by [Mak3it AI Technologie](https://mak3it.com) — Sovereign AI solutions from Quebec, Canada. 🍁

---

## ✨ Features

- ✅ **Dual transport**: stdio (local) + SSE/streamable-http (remote)
- 📞 **Calls**: list, detail, transcribe, record, delete
- 🤖 **Agents**: list, configure, update system prompt, delete
- 🎙️ **Voices**: list all available voices
- 🧠 **Models**: list available LLMs
- 🔧 **Tools**: manage custom agent tools
- 🪝 **Webhooks**: create, list, delete
- 📊 **Usage**: usage statistics

---

## 🚀 Installation

### Prerequisites

```bash
pip install fastmcp httpx python-dotenv
```

### Configuration

Create a `.env` file in the same directory:

```env
ULTRAVOX_API_KEY=your_ultravox_api_key
```

---

## 🖥️ Usage

### stdio Mode — Claude Desktop

```bash
python ultravox_mcp.py
```

**`claude_desktop_config.json`**:

```json
{
  "mcpServers": {
    "ultravox": {
      "command": "python",
      "args": ["C:\\path\\to\\ultravox_mcp.py"],
      "env": {
        "ULTRAVOX_API_KEY": "your_api_key"
      }
    }
  }
}
```

### SSE Mode — Claude.ai / n8n / Web

```bash
python ultravox_mcp.py --transport sse --port 8000
```

Connection URL: `http://your-server:8000/sse`

### streamable-http Mode — Modern Standard

```bash
python ultravox_mcp.py --transport streamable-http --port 8000
```

Connection URL: `http://your-server:8000/mcp`

### Via environment variables

```bash
MCP_TRANSPORT=sse MCP_PORT=8000 ULTRAVOX_API_KEY=xxx python ultravox_mcp.py
```

---

## 🛠️ Available MCP Tools (22 tools)

| Category | Tool | Description |
|----------|------|-------------|
| Account | `get_account_info` | Account information |
| Calls | `list_calls` | List all calls |
| Calls | `get_call` | Call details |
| Calls | `get_call_messages` | Full transcript |
| Calls | `get_call_recording` | Audio recording URL |
| Calls | `get_call_stages` | Call stages |
| Calls | `get_call_tools` | Tools used in a call |
| Calls | `get_call_usage` | Usage statistics |
| Calls | `delete_call` | Delete a call |
| Calls | `get_deleted_calls` | Deleted calls |
| Agents | `list_agents` | List agents |
| Agents | `get_agent` | Agent details |
| Agents | `list_agent_calls` | Agent call history |
| Agents | `update_agent_prompt` | Update system prompt |
| Agents | `delete_agent` | Delete an agent |
| Voices | `list_voices` | Available voices |
| Voices | `get_voice` | Voice details |
| Models | `list_models` | Available LLMs |
| Tools | `list_tools` | Custom tools |
| Tools | `get_tool` | Tool details |
| Webhooks | `list_webhooks` | List webhooks |
| Webhooks | `get_webhook` | Webhook details |
| Webhooks | `create_webhook` | Create a webhook |
| Webhooks | `delete_webhook` | Delete a webhook |
| API | `get_open_api_schema` | Ultravox OpenAPI schema |

---

## 📦 Project Structure

```
ultravox-mcp/
├── ultravox_mcp.py    # Main MCP server
├── .env               # API key (do not commit!)
├── .env.example       # Configuration example
└── README.md
```

---

## 🏢 About

Developed by **Mak3it AI Technologie** — Jean-Sébastien Larose, Quebec, Canada 🍁

