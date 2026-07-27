#!/usr/bin/env python3
"""
YouTube · Upload Pending Videos
================================

Lê `youtube/upload_batch_ready.json` (codes 09-13 no estado atual) e
re-tenta o upload dos vídeos que falharam por limite diário do canal.

Usa os mesmos metadados do `publish_plan.json` (título, descrição, tags,
thumbnail) e reaproveita os arquivos físicos já existentes em
`/var/www/oneverso/current/...` (caminhos declarados no plan).

## Requisitos

- Python 3.10+
- google-api-python-client
- Credenciais OAuth2 (mesmas do `youtube_set_privacy_public.py`)

## Uso

```bash
# Upload de TODOS os pendentes (read do upload_batch_ready.json)
python3 scripts/youtube_upload_pending.py

# Upload de apenas 1 code
python3 scripts/youtube_upload_pending.py --code 09

# Dry-run
python3 scripts/youtube_upload_pending.py --dry-run
```

## Rate Limit

YouTube Data API v3 tem limite de **10.000 units/dia**, com cada upload
custando ~1600 units. Conta gratuita permite ~6 uploads/dia. Conta
verificada pode chegar a 15-20/dia.

Este script é **idempotente**: pula vídeos que já estão no
`upload_results.json`.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

try:
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    from googleapiclient.errors import HttpError
except ImportError:
    print("❌ Dependências faltando. Rode: pip install google-api-python-client google-auth-oauthlib")
    sys.exit(1)

# === CONFIGURAÇÃO ===
ROOT = Path(__file__).resolve().parent.parent
YT = ROOT / "youtube"

CLIENT_SECRET = YT / "client_secret.json"
TOKEN_FILE = YT / "token.json"
PUBLISH_PLAN = YT / "publish_plan.json"
BATCH_READY = YT / "upload_batch_ready.json"
RESULTS_JSON = YT / "upload_results.json"

SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def get_youtube_service():
    """Autentica e retorna cliente da YouTube Data API v3."""
    creds: Optional[Credentials] = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not CLIENT_SECRET.exists():
                print(f"❌ {CLIENT_SECRET} não existe. Veja o docstring.")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(str(CLIENT_SECRET), SCOPES)
            creds = flow.run_local_server(port=0)
        TOKEN_FILE.write_text(creds.to_json(), encoding="utf-8")

    return build("youtube", "v3", credentials=creds)


def upload_video(youtube, item: dict) -> tuple[Optional[str], Optional[str]]:
    """Faz upload de 1 vídeo. Retorna (video_id, error_message)."""
    video_path = item.get("video_path", "")
    title = item.get("youtube_title", item.get("title", ""))
    description = item.get("description", "")
    tags = item.get("tags", [])
    privacy = item.get("privacy_status", "unlisted")
    category_id = str(item.get("category_id", "27"))
    made_for_kids = item.get("made_for_kids", False)

    if not Path(video_path).exists():
        return None, f"arquivo não existe: {video_path}"

    try:
        body = {
            "snippet": {
                "title": title,
                "description": description,
                "tags": tags,
                "categoryId": category_id,
            },
            "status": {
                "privacyStatus": privacy,
                "selfDeclaredMadeForKids": made_for_kids,
            },
        }

        media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        response = youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media,
        ).execute()
        return response.get("id"), None
    except HttpError as e:
        return None, f"HttpError: {e}"


def set_thumbnail(youtube, video_id: str, thumb_path: str) -> Optional[str]:
    """Seta thumbnail customizado."""
    if not Path(thumb_path).exists():
        return f"thumb não existe: {thumb_path}"
    try:
        youtube.thumbnails().set(
            videoId=video_id,
            media_body=MediaFileUpload(thumb_path, mimetype="image/png"),
        ).execute()
        return None
    except HttpError as e:
        return f"HttpError: {e}"


def main() -> int:
    parser = argparse.ArgumentParser(description="Re-tenta upload dos vídeos pendentes")
    parser.add_argument("--code", type=str, help="Upload apenas este code (ex: 09)")
    parser.add_argument("--dry-run", action="store_true", help="Apenas lista, sem upload")
    parser.add_argument("--public", action="store_true", help="Forçar privacy=public no upload")
    args = parser.parse_args()

    # Carrega plan + batch + results
    plan = load_json(PUBLISH_PLAN)
    plan_map = {v["code"]: v for v in plan}
    batch = load_json(BATCH_READY)
    results = load_json(RESULTS_JSON) if RESULTS_JSON.exists() else {"uploaded": [], "errors": []}

    # Filtra alvos
    if args.code:
        targets = [b for b in batch if b.get("code") == args.code]
    else:
        targets = batch

    # Pula codes já upados
    already_uploaded_codes = {v.get("code") for v in results.get("uploaded", [])}
    targets = [t for t in targets if t.get("code") not in already_uploaded_codes]

    if not targets:
        print("✅ Nenhum vídeo pendente para upload.")
        return 0

    print(f"📋 Alvos: {len(targets)}")
    for t in targets:
        s = t.get("status", "?")
        print(f"   [{s:20s}] code={t.get('code'):3s} {t.get('title', '')[:60]}")
        print(f"      video: {t.get('video_path', '')}")
        print(f"      thumb: {t.get('thumbnail_path', '')}")

    if args.dry_run:
        print("\n🔍 DRY-RUN: nenhuma alteração feita.")
        return 0

    # Autentica
    print("\n🔐 Autenticando no YouTube...")
    youtube = get_youtube_service()
    print("✅ Autenticado.\n")

    # Aplica upload
    print("🚀 Iniciando uploads...\n")
    success = error = 0
    for t in targets:
        code = t.get("code", "?")
        print(f"   📤 code={code} uploading...")

        # Override de privacidade se --public
        if args.public:
            t["privacy_status"] = "public"

        video_id, err = upload_video(youtube, t)
        if err:
            print(f"   ❌ code={code} ERRO: {err}")
            results.setdefault("errors", []).append(
                {"code": code, "error": err, "attempted_at": "now"}
            )
            error += 1
            continue

        print(f"   ✅ code={code} uploaded: https://youtu.be/{video_id}")

        # Tenta setar thumbnail
        thumb_path = t.get("thumbnail_path", "")
        if thumb_path:
            thumb_err = set_thumbnail(youtube, video_id, thumb_path)
            if thumb_err:
                print(f"   ⚠️  thumb: {thumb_err}")
            else:
                print(f"   🖼️  thumb set")

        # Atualiza plan + results
        plan_map[code]["status"] = "uploaded"
        plan_map[code]["video_id"] = video_id
        plan_map[code]["url"] = f"https://www.youtube.com/watch?v={video_id}"
        results["uploaded"].append(
            {
                "code": code,
                "youtube_title": t.get("youtube_title", ""),
                "video_id": video_id,
                "url": f"https://www.youtube.com/watch?v={video_id}",
                "thumbnail_set": bool(thumb_path) and not thumb_err if 'thumb_err' in dir() else False,
                "status": t.get("privacy_status", "unlisted"),
                "uploaded_at": "now",
            }
        )
        success += 1

    # Salva results
    save_json(RESULTS_JSON, results)
    save_json(PUBLISH_PLAN, list(plan_map.values()))
    print(f"\n📊 Resumo: {success} ok, {error} erro")
    print(f"💾 Atualizado: {RESULTS_JSON.name}, {PUBLISH_PLAN.name}")
    return 0 if error == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
