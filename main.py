import click
from rich.console import Console
from rich.table import Table

import storage
from assistant import summarize_notes

console = Console()


@click.group()
def cli():
    """AI Note Assistant — manage and summarize your notes from the terminal."""
    storage.init_db()


@cli.command()
@click.argument("content")
@click.option("--tags", "-t", default="", help="Comma-separated tags")
def add(content: str, tags: str):
    """Add a new note."""
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
    """Search notes by content."""
    notes = storage.search_notes(query)
    if not notes:
        console.print("[yellow]No matching notes.[/yellow]")
        return

    for note in notes:
        console.print(
            f"[cyan]#{note['id']}[/cyan] [{note['created_at'][:10]}] "
            f"{note['content']} [green]{note['tags']}[/green]"
        )


@cli.command()
@click.option("--tag", "-t", default=None, help="Summarize notes with this tag")
def summarize(tag: str):
    """Get an AI summary of your notes."""
    notes = storage.get_all_notes(tag)
    console.print("[dim]Generating summary...[/dim]")
    result = summarize_notes(notes)
    console.print(f"\n[bold]Summary:[/bold]\n{result}")


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
            f.write(f"## Note #{note['id']} — {note['created_at'][:10]}\n\n")
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


if __name__ == "__main__":
    cli()
