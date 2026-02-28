#!/usr/bin/env python3
"""
Serveur MCP Ultravox - DUAL MODE (stdio + HTTP)
=========================================
Modes de transport disponibles :
  - stdio         : pour Claude Desktop (défaut)
  - sse           : HTTP avec Server-Sent Events (pour Claude.ai web, n8n, etc.)
  - streamable-http : HTTP stateless moderne (recommandé pour remote)

Usage :
  # Mode stdio (Claude Desktop)
  python ultravox_mcp.py

  # Mode SSE sur port 8000
  python ultravox_mcp.py --transport sse --port 8000

  # Mode streamable-http sur port 8000
  python ultravox_mcp.py --transport streamable-http --port 8000

  # Via variables d'environnement
  MCP_TRANSPORT=sse MCP_PORT=8000 python ultravox_mcp.py

Configuration claude_desktop_config.json (stdio) :
  {
    "mcpServers": {
      "ultravox": {
        "command": "python",
        "args": ["C:\\Users\\Bloody\\Documents\\ultravox-mcp\\ultravox_mcp.py"],
        "env": { "ULTRAVOX_API_KEY": "VOTRE_CLE_API" }
      }
    }
  }

Configuration Claude.ai / n8n (HTTP SSE) :
  URL : http://localhost:8000/sse
  ou   http://votre-serveur:8000/sse

Configuration streamable-http :
  URL : http://localhost:8000/mcp
"""

import os
import sys
import argparse
import httpx
from typing import Optional
from fastmcp import FastMCP
from dotenv import load_dotenv

# ─── Configuration ────────────────────────────────────────────────────────────

load_dotenv()

ULTRAVOX_API_KEY = os.getenv("ULTRAVOX_API_KEY", "")
if not ULTRAVOX_API_KEY:
    print("❌ ERREUR : ULTRAVOX_API_KEY non défini.", file=sys.stderr)
    sys.exit(1)

ULTRAVOX_API_BASE = "https://api.ultravox.ai/api"

HEADERS = {
    "X-API-Key": ULTRAVOX_API_KEY,
    "Content-Type": "application/json",
}

# ─── Helper HTTP ──────────────────────────────────────────────────────────────

def api_get(path: str, params: dict = None) -> dict:
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.get(f"{ULTRAVOX_API_BASE}{path}", headers=HEADERS, params=params)
            if r.status_code == 200:
                return r.json()
            return {"error": f"HTTP {r.status_code}", "detail": r.text}
    except httpx.RequestError as e:
        return {"error": "Erreur réseau", "message": str(e)}
    except Exception as e:
        return {"error": "Erreur inattendue", "message": str(e)}

def api_post(path: str, body: dict = None) -> dict:
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.post(f"{ULTRAVOX_API_BASE}{path}", headers=HEADERS, json=body or {})
            if r.status_code in (200, 201):
                return r.json()
            return {"error": f"HTTP {r.status_code}", "detail": r.text}
    except Exception as e:
        return {"error": "Erreur inattendue", "message": str(e)}

def api_patch(path: str, body: dict = None) -> dict:
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.patch(f"{ULTRAVOX_API_BASE}{path}", headers=HEADERS, json=body or {})
            if r.status_code == 200:
                return r.json()
            return {"error": f"HTTP {r.status_code}", "detail": r.text}
    except Exception as e:
        return {"error": "Erreur inattendue", "message": str(e)}

def api_delete(path: str) -> dict:
    try:
        with httpx.Client(timeout=15.0) as client:
            r = client.delete(f"{ULTRAVOX_API_BASE}{path}", headers=HEADERS)
            if r.status_code in (200, 204):
                return {"success": True, "status": r.status_code}
            return {"error": f"HTTP {r.status_code}", "detail": r.text}
    except Exception as e:
        return {"error": "Erreur inattendue", "message": str(e)}

# ─── Serveur MCP ──────────────────────────────────────────────────────────────

mcp = FastMCP(
    name="ultravox",
    instructions=(
        "Serveur MCP pour l'API Ultravox. "
        "Permet de gérer les appels vocaux, agents, voix, webhooks et outils. "
        "Utilisez list_calls pour voir les appels, get_call_messages pour les transcriptions, "
        "list_agents pour voir les agents configurés."
    ),
)

# ════════════════════════════════════════════════════════════════════════════════
# COMPTE
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def get_account_info() -> dict:
    """Récupère les informations du compte Ultravox (quota, plan, etc.)."""
    return api_get("/accounts/me")

# ════════════════════════════════════════════════════════════════════════════════
# CALLS - Appels
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_calls(limit: int = 20, offset: int = 0) -> dict:
    """Liste les appels Ultravox. Retourne id, statut, durée, agent utilisé."""
    return api_get("/calls", {"limit": limit, "offset": offset})

@mcp.tool()
def get_call(call_id: str) -> dict:
    """Récupère les détails complets d'un appel par son ID."""
    return api_get(f"/calls/{call_id}")

@mcp.tool()
def get_call_messages(call_id: str) -> dict:
    """Récupère la transcription complète (messages) d'un appel."""
    return api_get(f"/calls/{call_id}/messages")

@mcp.tool()
def get_call_recording(call_id: str) -> dict:
    """Récupère l'URL de l'enregistrement audio d'un appel."""
    return api_get(f"/calls/{call_id}/recording")

@mcp.tool()
def get_call_stages(call_id: str) -> dict:
    """Récupère les étapes/stages d'un appel."""
    return api_get(f"/calls/{call_id}/stages")

@mcp.tool()
def get_call_tools(call_id: str) -> dict:
    """Récupère les outils utilisés durant un appel."""
    return api_get(f"/calls/{call_id}/tools")

@mcp.tool()
def get_call_usage() -> dict:
    """Récupère les statistiques d'utilisation des appels (minutes, coûts)."""
    return api_get("/calls/usage")

@mcp.tool()
def delete_call(call_id: str) -> dict:
    """Supprime un appel. ⚠️ Action destructive irréversible."""
    return api_delete(f"/calls/{call_id}")

@mcp.tool()
def get_deleted_calls(limit: int = 20) -> dict:
    """Liste les appels supprimés."""
    return api_get("/calls/deleted", {"limit": limit})

# ════════════════════════════════════════════════════════════════════════════════
# AGENTS
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_agents(limit: int = 20) -> dict:
    """Liste tous les agents vocaux configurés dans le compte."""
    return api_get("/agents", {"limit": limit})

@mcp.tool()
def get_agent(agent_id: str) -> dict:
    """Récupère les détails complets d'un agent (prompt système, voix, outils, etc.)."""
    return api_get(f"/agents/{agent_id}")

@mcp.tool()
def list_agent_calls(agent_id: str, limit: int = 20) -> dict:
    """Liste tous les appels associés à un agent spécifique."""
    return api_get(f"/agents/{agent_id}/calls", {"limit": limit})

@mcp.tool()
def update_agent_prompt(agent_id: str, system_prompt: str) -> dict:
    """Met à jour le prompt système d'un agent. Attention : modifie le comportement de l'agent."""
    return api_patch(f"/agents/{agent_id}", {"systemPrompt": system_prompt})

@mcp.tool()
def delete_agent(agent_id: str) -> dict:
    """Supprime un agent. ⚠️ Action destructive irréversible."""
    return api_delete(f"/agents/{agent_id}")

# ════════════════════════════════════════════════════════════════════════════════
# VOIX
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_voices(limit: int = 50) -> dict:
    """Liste toutes les voix disponibles (synthèse vocale TTS)."""
    return api_get("/voices", {"limit": limit})

@mcp.tool()
def get_voice(voice_id: str) -> dict:
    """Récupère les détails d'une voix spécifique (nom, langue, genre, provider)."""
    return api_get(f"/voices/{voice_id}")

# ════════════════════════════════════════════════════════════════════════════════
# MODÈLES LLM
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_models() -> dict:
    """Liste les modèles LLM disponibles dans Ultravox."""
    return api_get("/models")

# ════════════════════════════════════════════════════════════════════════════════
# OUTILS (Tools pour agents)
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_tools(limit: int = 20) -> dict:
    """Liste les outils personnalisés disponibles pour les agents."""
    return api_get("/tools", {"limit": limit})

@mcp.tool()
def get_tool(tool_id: str) -> dict:
    """Récupère les détails d'un outil personnalisé (schéma, URL webhook, etc.)."""
    return api_get(f"/tools/{tool_id}")

# ════════════════════════════════════════════════════════════════════════════════
# WEBHOOKS
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def list_webhooks() -> dict:
    """Liste tous les webhooks configurés dans le compte."""
    return api_get("/webhooks")

@mcp.tool()
def get_webhook(webhook_id: str) -> dict:
    """Récupère les détails d'un webhook spécifique."""
    return api_get(f"/webhooks/{webhook_id}")

@mcp.tool()
def create_webhook(url: str, events: list) -> dict:
    """
    Crée un nouveau webhook.
    
    Args:
        url: URL HTTPS qui recevra les événements
        events: Liste des événements à écouter (ex: ["call.started", "call.ended"])
    """
    return api_post("/webhooks", {"url": url, "events": events})

@mcp.tool()
def delete_webhook(webhook_id: str) -> dict:
    """Supprime un webhook. ⚠️ Action irréversible."""
    return api_delete(f"/webhooks/{webhook_id}")

# ════════════════════════════════════════════════════════════════════════════════
# SCHÉMA API
# ════════════════════════════════════════════════════════════════════════════════

@mcp.tool()
def get_open_api_schema() -> dict:
    """Récupère le schéma OpenAPI complet de l'API Ultravox (endpoints disponibles)."""
    result = api_get("/openapi.json")
    if "paths" in result:
        return {
            "version": result.get("info", {}).get("version"),
            "endpoints_count": len(result["paths"]),
            "endpoints": list(result["paths"].keys()),
        }
    return result

# ════════════════════════════════════════════════════════════════════════════════
# POINT D'ENTRÉE - DUAL MODE
# ════════════════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(
        description="Serveur MCP Ultravox - supporte stdio, SSE et streamable-http"
    )
    parser.add_argument(
        "--transport",
        choices=["stdio", "sse", "streamable-http"],
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="Transport à utiliser (défaut: stdio)",
    )
    parser.add_argument(
        "--host",
        default=os.getenv("MCP_HOST", "0.0.0.0"),
        help="Adresse d'écoute HTTP (défaut: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=int(os.getenv("MCP_PORT", "8000")),
        help="Port HTTP (défaut: 8000)",
    )
    args = parser.parse_args()

    if args.transport == "stdio":
        print("🎤 Ultravox MCP démarré en mode stdio", file=sys.stderr)
        mcp.run(transport="stdio")

    elif args.transport == "sse":
        print(f"🌐 Ultravox MCP démarré en mode SSE → http://{args.host}:{args.port}/sse", file=sys.stderr)
        mcp.run(transport="sse", host=args.host, port=args.port)

    elif args.transport == "streamable-http":
        print(f"🌐 Ultravox MCP démarré en mode streamable-http → http://{args.host}:{args.port}/mcp", file=sys.stderr)
        mcp.run(transport="streamable-http", host=args.host, port=args.port)


if __name__ == "__main__":
    main()
