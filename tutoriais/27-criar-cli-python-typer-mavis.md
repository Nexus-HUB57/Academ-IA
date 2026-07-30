---
version: "1.0-mavis-recovery"
recovery_note: "Versão recuperada após force-push de 2026-07-29. Coexiste com o canônico em tutoriais/(sem equivalente canônico).md"
title: "Tutorial 27 · Criar CLI Python com Typer"
description: "Como construir command-line tools profissionais com Typer (alternativa moderna ao argparse)"
tags: [tutorial, 27, cli, typer, python, terminal, devx]
tier: "Agente"
duracao_estimada: "20 min"
pre_requisitos: ["tutoriais/14-ler-skill-manifest.md"]
ultima_atualizacao: 2026-07-27
---

# Tutorial 27 · Criar CLI Python com Typer

> **Por que importa**: CLIs são a forma mais rápida de expor ferramentas para o time. Typer (criado pelo autor do FastAPI) usa type hints, é auto-documentado, e tem UX excelente.

## 🎯 O que você vai aprender

- Criar CLI profissional com Typer
- Adicionar sub-comandos, argumentos, opções
- Adicionar auto-complete para bash/zsh/fish
- Publicar como executável

## ⏱️ Duração: 20 minutos

---

## 📋 Passo 1: Instalar

```bash
pip install typer[all]  # Inclui rich, shellingham, etc.
```

## 📋 Passo 2: CLI Básico

```python
# nexus_cli.py
import typer
from typing import Optional
from rich.console import Console

app = typer.Typer(help="Nexus CLI — Operações de afiliados e agentes")
console = Console()

@app.command()
def hello(
    name: str = typer.Argument(..., help="Seu nome"),
    formal: bool = typer.Option(False, "--formal", "-f", help="Usar tratamento formal"),
    repeat: int = typer.Option(1, "--repeat", "-r", help="Vezes para repetir")
):
    """Saudação personalizada."""
    greeting = "Boa noite" if formal else "Oi"
    for _ in range(repeat):
        console.print(f"[bold cyan]{greeting}, {name}![/bold cyan]")

@app.command()
def version():
    """Mostra a versão do CLI."""
    console.print("[bold]Nexus CLI v1.0.0[/bold]")

if __name__ == "__main__":
    app()
```

```bash
# Testar
python nexus_cli.py hello --help
python nexus_cli.py hello Maria --formal --repeat 3
python nexus_cli.py version
```

## 📋 Passo 3: Sub-comandos (Skill Manager)

```python
# skills_cli.py
import typer
import json
from pathlib import Path
from typing import Optional
from datetime import datetime

app = typer.Typer(help="Gerenciador de skills do Nexus")
console = Console()

# Sub-app para 'list' e 'show'
skills_app = typer.Typer(help="Operações em skills")
app.add_typer(skills_app, name="skill")

@skills_app.command("list")
def list_skills(
    tier: Optional[str] = typer.Option(None, "--tier", help="Filtrar por tier: fundamental, agente, master, elite"),
    active_only: bool = typer.Option(False, "--active", help="Apenas skills ativas")
):
    """Lista todas as skills."""
    skills = load_skills()
    if tier:
        skills = [s for s in skills if s['tier'] == tier]
    if active_only:
        skills = [s for s in skills if s.get('active', True)]

    console.print(f"[bold]Total: {len(skills)} skills[/bold]\n")
    for s in skills:
        status = "🟢" if s.get('active', True) else "⚪"
        console.print(f"  {status} [cyan]{s['id']:30}[/cyan] | {s['name']}")

@skills_app.command("show")
def show_skill(
    skill_id: str = typer.Argument(..., help="ID da skill"),
    full: bool = typer.Option(False, "--full", help="Mostrar manifest completo")
):
    """Mostra detalhes de uma skill."""
    skill = find_skill(skill_id)
    if not skill:
        console.print(f"[red]Skill '{skill_id}' não encontrada[/red]")
        raise typer.Exit(code=1)

    console.print(f"\n[bold cyan]{skill['name']}[/bold cyan]")
    console.print(f"  ID: {skill['id']}")
    console.print(f"  Tier: {skill['tier']}")
    console.print(f"  Description: {skill['description']}")

    if full:
        console.print(f"\n[bold]Manifest:[/bold]")
        console.print_json(json.dumps(skill, indent=2, ensure_ascii=False))

@skills_app.command("create")
def create_skill(
    name: str = typer.Argument(..., help="Nome da skill"),
    tier: str = typer.Option(..., "--tier", help="fundamental/agente/master/elite"),
    template: str = typer.Option("basic", "--template", "-t", help="Template: basic, rag, agent, voice")
):
    """Cria nova skill a partir de template."""
    template_path = Path(f"templates/skill-{template}.json")
    if not template_path.exists():
        console.print(f"[red]Template '{template}' não encontrado[/red]")
        raise typer.Exit(code=1)

    manifest = json.loads(template_path.read_text())
    manifest['name'] = name
    manifest['tier'] = tier
    manifest['id'] = generate_id(name)
    manifest['created_at'] = datetime.utcnow().isoformat()

    output = Path(f"skills/{manifest['id']}.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))

    console.print(f"[green]✓ Skill criada: {output}[/green]")
    console.print(f"  ID: {manifest['id']}")
    console.print(f"  Próximo: implementar lógica em skills/{manifest['id']}.py")
```

## 📋 Passo 4: Auto-complete

```bash
# Gerar script de auto-complete
python nexus_cli.py --install-completion

# Resultado (adicione ao ~/.bashrc):
# source ~/.bash_completions/nexus_cli.py-completion.bash

# Agora:
nexus_cli.py <TAB>          # Mostra sub-comandos
nexus_cli.py hello <TAB>    # Mostra opções
```

## 📋 Passo 5: Transformar em Executável

```python
# setup.py ou pyproject.toml
# pyproject.toml:
[project.scripts]
nexus = "nexus_cli:app"
skill = "skills_cli:app"
```

```bash
# Instalar em modo editável
pip install -e .

# Agora pode usar diretamente:
nexus hello Maria
skill list --tier master
```

## 📋 Passo 6: Adicionar Cores e UX

```python
from rich.table import Table
from rich.progress import track
import time

@app.command()
def deploy(
    env: str = typer.Argument(..., help="Ambiente: dev, staging, prod"),
    skip_tests: bool = typer.Option(False, "--skip-tests", help="Pular testes")
):
    """Deploy com progresso visual."""
    console.print(f"\n[bold]Deploying to {env}...[/bold]\n")

    if not skip_tests:
        for step in track(["Running tests", "Building", "Pushing", "Rolling out"], description="Deploying..."):
            time.sleep(1)  # simula trabalho
    else:
        console.print("[yellow]⚠️ Tests skipped[/yellow]")

    table = Table(title="Deploy Summary")
    table.add_column("Environment", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Version")

    table.add_row(env, "✅ Success", "v1.2.3")
    console.print(table)
```

## 🎓 Próximo Passo

- **Tutoriais relacionados**:
  - `tutoriais/14-ler-skill-manifest.md` (manipular skills)
  - `tutoriais/22-criar-playbook-do-zero.md`
- **Curso**: `cursos/agente/` (automações)
- **Ferramentas**: Adicionar ao `Lab-Nexus/tools/automation/`

---

**Tutorial criado em 2026-07-27** · Mavis Agent
**Versão 1.0** · Mantido em `tutoriais/27-criar-cli-python-typer.md`
