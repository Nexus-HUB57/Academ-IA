#!/usr/bin/env python3
"""
YouTube · Set Privacy to Public
================================

Muda a privacidade de TODOS os vídeos unlisted/private do canal Nexus
para `public`, com base em `youtube/upload_results.json` (video_id por code).

## Requisitos

- Python 3.10+
- google-api-python-client (`pip install google-api-python-client`)
- Credenciais OAuth2 do YouTube Data API v3 (client_secret.json)

## Setup

1. Vá em https://console.cloud.google.com → criar projeto
2. Habilite YouTube Data API v3
3. Crie credenciais OAuth2 (tipo "Desktop app" ou "TV and Limited Input")
4. Salve o JSON em `youtube/client_secret.json` (NÃO versionar)
5. Rode o script pela primeira vez para autenticar (gera `youtube/token.json`)

## Uso

```bash
# Mudar TODOS os vídeos para public
python3 scripts/youtube_set_privacy_public.py --all

# Mudar apenas codes específicos
python3 scripts/youtube_set_privacy_public.py --codes 00,01,02,03,04

# Dry-run (apenas lista o que seria mudado, sem alterar)
python3 scripts/youtube_set_privacy_public.py --all --dry-run
```

## Segurança

- NUNCA versionar `client_secret.json` nem `token.json` (já no .gitignore)
- ID do canal já está em constante (NEXUS_CHANNEL_ID) - ajuste se mudar
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Optional

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Dependências faltando. Rode: pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

# === CONFIGURAÇÃO ===
ROOT = Path(__file__).resolve().parent.parent
YT = ROOT / "youtube"
RESULTS_JSON = YT / "upload_results.json"

CLIENT_SECRET = YT / "client_secret.json"
TOKEN_FILE = YT / "token.json"

# Channel ID do canal Nexus Affil'IA'te
NEXUS_CHANNEL_ID = "UC_PLACEHOLDER"  # TODO: pegar do about do canal

# Escopo OAuth2: precisamos de gerenciar vídeos
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def load_uploaded() -> list[dict]:
    """Carrega lista de vídeos upados de upload_results.json."""
    if not RESULTS_JSON.exists():
        print(f"❌ {RESULTS_JSON} não existe")
        sys.exit(1)
    data = json.loads(RESULTS_JSON.read_text(encoding="utf-8"))
    return data.get("uploaded", [])


def get_youtube_service():
    """Autentica e retorna cliente da YouTube Data API v3."""
    creds: Optional[Credentials] = None

    # 1. Tentar carregar token existente
    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    # 2. Se inválido/expirado, fazer fluxo OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"❌ {CLIENT_SECRET} não existe.")
                print("   Veja o setup no docstring do script.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("youtube", "v3", credentials=creds)


def set_video_privacy(youtube, video_id: str, current_status: str, dry_run: bool) -> str:
    """Muda privacidade de um vídeo para 'public'."""
    if current_status == "public":
        return "skip-already-public"

    if dry_run:
        return "dry-run"

    try:
        youtube.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": {
                    "privacyStatus": "public",
                    # mantém embeddable, publicStatsViewable do estado atual
                },
            },
        ).execute()
        return "ok"
    except HttpError as e:
        return f"error: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Muda vídeos do canal Nexus para 'public'")
    parser.add_argument("--all", action="store_true", help="Mudar TODOS os unlisted/private")
    parser.add_argument("--codes", type=str, help="Códigos específicos (ex: 00,01,02)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas lista, sem alterar")
    args = parser.parse_args()

    if not args.all and not args.codes:
        parser.error("Especifique --all ou --codes 00,01,02")

    # Carrega vídeos
    uploaded = load_uploaded()
    print(f"📋 Total upados: {len(uploaded)}")

    # Filtra
    if args.all:
        targets = [v for v in uploaded if v.get("status") in ("unlisted", "private")]
    else:
        codes = {c.strip() for c in args.codes.split(",") if c.strip()}
        targets = [v for v in uploaded if v.get("code") in codes]

    if not targets:
        print("✅ Nenhum vídeo para mudar.")
        return 0

    print(f"🎯 Alvos: {len(targets)}")
    for v in targets:
        s = v.get("status", "?")
        icon = "🔒" if s == "unlisted" else "🔐"
        print(f"   {icon} code={v.get('code'):3s} {s:10s} {v.get('url', '')}")

    if args.dry_run:
        print("\n🔍 DRY-RUN: nenhuma alteração feita.")
        return 0

    # Autentica
    print("\n🔐 Autenticando no YouTube...")
    youtube = get_youtube_service()
    print("✅ Autenticado.\n")

    # Aplica mudança
    print("🚀 Aplicando mudança de privacidade...\n")
    success = error = skip = 0
    for v in targets:
        video_id = v.get("video_id")
        code = v.get("code", "?")
        if not video_id:
            print(f"   ⚠️  code={code}: sem video_id")
            error += 1
            continue

        result = set_video_privacy(youtube, video_id, v.get("status", ""), args.dry_run)
        if result == "ok":
            print(f"   ✅ code={code} {video_id} → public")
            success += 1
        elif result == "skip-already-public":
            print(f"   ⏭️  code={code} {video_id} já é public")
            skip += 1
        else:
            print(f"   ❌ code={code} {video_id} → {result}")
            error += 1

    print(f"\n📊 Resumo: {success} ok, {skip} skip, {error} erro")
    return 0 if error == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
