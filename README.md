# 🎤 Ultravox MCP Server

Serveur MCP (Model Context Protocol) pour l'API [Ultravox](https://ultravox.ai) — compatible **Claude Desktop** (stdio) et **Claude.ai / n8n** (HTTP).

Développé par [Mak3it AI Technologie](https://mak3it.com) — Solutions IA souveraines au Québec.

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

Développé par **Mak3it AI Technologie** — Petite-Vallée, Gaspésie, Québec 🍁

Solutions IA vocales souveraines pour les entreprises québécoises.

**Ralf** — L'agent vocal intelligent fait au Québec.
