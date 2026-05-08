import click
from rich.console import Console
from rich.table import Table

import storage
from assistant import summarize_notes, auto_tag, smart_search, categorize_notes, analyze_pipeline

console = Console()


@click.group()
def cli():
    """AI Note Assistant -- manage and summarize your notes from the terminal."""
    storage.init_db()


@cli.command()
@click.argument("content")
@click.option("--tags", "-t", default="", help="Comma-separated tags")
@click.option("--auto-tag", "use_auto_tag", is_flag=True, help="Let AI generate tags automatically")
def add(content: str, tags: str, use_auto_tag: bool):
    """Add a new note."""
    if use_auto_tag and not tags:
        console.print("[dim]Generating tags with AI...[/dim]")
        tags = auto_tag(content)
        if tags:
            console.print(f"[dim]Auto-tags: {tags}[/dim]")
    note_id = storage.add_note(content, tags)
    console.print(f"[green]Note #{note_id} saved.[/green]")


@cli.command("list")
@click.option("--tag", "-t", default=None, help="Filter by tag")
def list_notes(tag: str):
    """List all notes."""
    notes = storage.get_all_notes(tag)
    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return

    table = Table(title="Your Notes")
    table.add_column("ID", style="cyan", width=5)
    table.add_column("Date", style="magenta", width=12)
    table.add_column("Content", style="white")
    table.add_column("Tags", style="green", width=20)

    for note in notes:
        table.add_row(
            str(note["id"]),
            note["created_at"][:10],
            note["content"][:80],
            note["tags"],
        )

    console.print(table)


@cli.command()
@click.argument("query")
def search(query: str):
    """Search notes by content (keyword match)."""
    notes = storage.search_notes(query)
    if not notes:
        console.print("[yellow]No matching notes.[/yellow]")
        return

    for note in notes:
        console.print(
            f"[cyan]#{note['id']}[/cyan] [{note['created_at'][:10]}] "
            f"{note['content']} [green]{note['tags']}[/green]"
        )


@cli.command("ai-search")
@click.argument("query")
def ai_search(query: str):
    """Semantic AI-powered search -- finds notes by meaning, not just keywords."""
    all_notes = storage.get_all_notes()
    if not all_notes:
        console.print("[yellow]No notes found.[/yellow]")
        return

    console.print("[dim]Searching with AI...[/dim]")
    results = smart_search(query, all_notes)

    if not results:
        console.print("[yellow]No semantically matching notes found.[/yellow]")
        return

    console.print(f"[bold]Found {len(results)} relevant note(s):[/bold]\n")
    for note in results:
        console.print(
            f"[cyan]#{note['id']}[/cyan] [{note['created_at'][:10]}] "
            f"{note['content']} [green]{note['tags']}[/green]"
        )


@cli.command()
@click.option("--tag", "-t", default=None, help="Summarize notes with this tag")
def summarize(tag: str):
    """Get an AI summary of your notes."""
    notes = storage.get_all_notes(tag)
    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return
    console.print("[dim]Generating summary...[/dim]")
    result = summarize_notes(notes)
    console.print(f"\n[bold]Summary:[/bold]\n{result}")


@cli.command()
@click.option("--tag", "-t", default=None, help="Categorize notes with this tag")
def categorize(tag: str):
    """AI-powered categorization -- groups notes by theme and priority."""
    notes = storage.get_all_notes(tag)
    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return
    console.print("[dim]Categorizing with AI...[/dim]")
    result = categorize_notes(notes)
    console.print(f"\n[bold]Categories:[/bold]\n{result}")


@cli.command()
@click.option("--tag", "-t", default=None, help="Analyze notes with this tag")
def analyze(tag: str):
    """Multi-step AI analysis pipeline: themes -> actions -> executive summary."""
    notes = storage.get_all_notes(tag)
    if not notes:
        console.print("[yellow]No notes found.[/yellow]")
        return
    console.print("[dim]Running AI analysis pipeline (3 steps)...[/dim]")
    result = analyze_pipeline(notes)
    console.print(f"\n{result}")


@cli.command()
@click.argument("filepath")
@click.option("--tag", "-t", default=None, help="Export notes with this tag")
def export(filepath: str, tag: str):
    """Export notes to a markdown file."""
    notes = storage.get_all_notes(tag)
    if not notes:
        console.print("[yellow]No notes to export.[/yellow]")
        return

    with open(filepath, "w") as f:
        f.write("# Exported Notes\n\n")
        for note in notes:
            f.write(f"## Note #{note['id']} -- {note['created_at'][:10]}\n\n")
            f.write(f"{note['content']}\n\n")
            if note["tags"]:
                f.write(f"**Tags:** {note['tags']}\n\n")
            f.write("---\n\n")

    console.print(f"[green]Exported {len(notes)} notes to {filepath}[/green]")


@cli.command()
@click.argument("note_id", type=int)
def delete(note_id: int):
    """Delete a note by ID."""
    if storage.delete_note(note_id):
        console.print(f"[green]Note #{note_id} deleted.[/green]")
    else:
        console.print(f"[red]Note #{note_id} not found.[/red]")


@cli.command()
def stats():
    """Show note collection statistics."""
    all_notes = storage.get_all_notes()
    if not all_notes:
        console.print("[yellow]No notes yet.[/yellow]")
        return

    total = len(all_notes)
    all_tags = set()
    for n in all_notes:
        if n["tags"]:
            for t in n["tags"].split(","):
                all_tags.add(t.strip())

    console.print(f"[bold]Notes:[/bold] {total}")
    console.print(f"[bold]Unique tags:[/bold] {len(all_tags)}")
    if all_tags:
        console.print(f"[bold]Tags:[/bold] {', '.join(sorted(all_tags))}")
    console.print(f"[bold]Oldest:[/bold] {all_notes[-1]['created_at'][:10]}")
    console.print(f"[bold]Newest:[/bold] {all_notes[0]['created_at'][:10]}")


if __name__ == "__main__":
    cli()
