#!/usr/bin/env python3
"""Voice Resolver — AcademIA Nexus
Camada única para resolver voice IDs das personas a partir do registro canônico.
Uso em pipelines TTS, scripts de produção de vídeo e geradores de áudio.

Fonte da verdade: marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md

ATENÇÃO: O caminho canônico foi migrado de `personas/` para `marca/personas/`
em 2026-07-23. A pasta `personas/` foi removida do repo.
"""
from __future__ import annotations
import json
import os
import subprocess
from pathlib import Path

# Constantes do registro (espelham OFFICIAL_VOICES_REGISTRY.md)
ROOT = Path('/workspace/Academ-IA')
MARCA = ROOT / 'marca' / 'personas'
IVE_WAV = MARCA / 'ive' / 'audio' / 'official_voice.wav'
ALENCAR_WAV = MARCA / 'alencar' / 'audio' / 'official_voice.wav'
IVE_MD5 = '073d4964d3de3713f0349731dd3bf683'
ALENCAR_MD5 = '9f1cbd7aaef82b70f8972e4dc7374eba'

# Voice IDs clonados (preenchidos após clone_voice)
IVE_CLONE_ID = os.environ.get('IVE_CLONE_ID', '').strip()
ALENCAR_CLONE_ID = os.environ.get('ALENCAR_CLONE_ID', '').strip()

# Fallback (proibido em produção oficial, mas disponível para emergências)
FALLBACK_IVE = 'Portuguese_CharmingQueen'
FALLBACK_ALENCAR = 'Portuguese_Steadymentor'


def md5(path: Path) -> str:
    import hashlib
    h = hashlib.md5()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            h.update(chunk)
    return h.hexdigest()


def verify_official_wavs() -> dict:
    """Verifica se os WAVs oficiais batem com os hashes do registry."""
    return {
        'ive': {'path': str(IVE_WAV), 'md5': md5(IVE_WAV), 'expected': IVE_MD5, 'ok': md5(IVE_WAV) == IVE_MD5},
        'alencar': {'path': str(ALENCAR_WAV), 'md5': md5(ALENCAR_WAV), 'expected': ALENCAR_MD5, 'ok': md5(ALENCAR_WAV) == ALENCAR_MD5},
    }


def get_voice_id(persona: str, allow_fallback: bool = False) -> str:
    """Resolve o voice_id para uma persona.

    Args:
        persona: 'ive' | 'alencar'
        allow_fallback: se True, retorna voice genérico quando clone não disponível.
                        Default False (recomendado em produção oficial).

    Returns:
        voice_id string (clone ID ou fallback).
    """
    p = persona.lower()
    clone_map = {'ive': IVE_CLONE_ID, 'alencar': ALENCAR_CLONE_ID}
    fallback_map = {'ive': FALLBACK_IVE, 'alencar': FALLBACK_ALENCAR}
    if p not in clone_map:
        raise ValueError(f"persona inválida: {persona!r}. Use 'ive' ou 'alencar'.")
    clone = clone_map[p]
    if clone:
        return clone
    if allow_fallback:
        return fallback_map[p]
    raise RuntimeError(
        f"Voice clone ID para {p!r} não configurado. "
        f"Defina ${p.upper()}_CLONE_ID ou passe allow_fallback=True. "
        f"Veja marca/personas/voice_registry/OFFICIAL_VOICES_REGISTRY.md."
    )


def describe_voices() -> dict:
    """Retorna um dict com info completa das vozes (para logging/auditoria)."""
    return {
        'ive': {
            'canonical_wav': str(IVE_WAV),
            'clone_id': IVE_CLONE_ID or None,
            'fallback_id': FALLBACK_IVE,
            'active_id': get_voice_id('ive', allow_fallback=True),
            'official': bool(IVE_CLONE_ID),
        },
        'alencar': {
            'canonical_wav': str(ALENCAR_WAV),
            'clone_id': ALENCAR_CLONE_ID or None,
            'fallback_id': FALLBACK_ALENCAR,
            'active_id': get_voice_id('alencar', allow_fallback=True),
            'official': bool(ALENCAR_CLONE_ID),
        },
    }


if __name__ == '__main__':
    print("=" * 60)
    print("Voice Resolver — AcademIA Nexus")
    print("=" * 60)
    print("\n[1] Verificando WAVs oficiais...")
    v = verify_official_wavs()
    for k, info in v.items():
        status = 'OK' if info['ok'] else 'MISMATCH'
        print(f"  {k:9s} {status}  md5={info['md5']}  path={info['path']}")
    print("\n[2] Resolvendo voice IDs...")
    d = describe_voices()
    for k, info in d.items():
        tag = 'OFFICIAL' if info['official'] else 'FALLBACK'
        print(f"  {k:9s} [{tag:8s}] active={info['active_id']}  clone={info['clone_id']}  wav={info['canonical_wav']}")
    print("\n" + "=" * 60)
