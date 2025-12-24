"""FastMCP server for Apple Notes integration"""

import logging
from functools import lru_cache
from fastmcp import FastMCP
from .notes_service import NotesService

# Setup FastMCP server
mcp = FastMCP("iNotes")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Lazy initialization - only create service when first tool is called
@lru_cache(maxsize=None)
def get_notes_service() -> NotesService:
    """Get or initialize the notes service"""
    logger.info("Initializing NotesService...")
    return NotesService()


@mcp.tool
def create_note(title: str, body: str) -> str:
    """Create a new note in Claude Diary folder

    Args:
        title: The title of the note
        body: The content/body of the note

    Returns:
        Success message with note ID
    """
    try:
        service = get_notes_service()
        note_id = service.create_note(title, body)
        return f"""Created note: "{title}"
ID: {note_id}
Folder: Claude Diary (hardcoded)"""
    except Exception as e:
        logger.error("Failed to create note: %s", e)
        return f"Error creating note: {str(e)}"


@mcp.tool
def append_to_note(note_id: str, content: str) -> str:
    """Append content to an existing note (APPEND ONLY - no overwrite)

    Args:
        note_id: The ID of the note to append to (x-coredata:// URL)
        content: The content to append

    Returns:
        Success message

    Note:
        This operation only APPENDS content. It cannot overwrite or delete existing content.
        This is a safety feature to prevent data loss.
    """
    try:
        service = get_notes_service()
        service.append_to_note(note_id, content)
        return f"Successfully appended content to note\nID: {note_id}"
    except Exception as e:
        logger.error("Failed to append to note: %s", e)
        return f"Error appending to note: {str(e)}"


@mcp.tool
def get_note(note_id: str) -> str:
    """Get full content of a specific note by ID

    Args:
        note_id: The note ID (x-coredata:// URL)

    Returns:
        Formatted note content with metadata
    """
    try:
        service = get_notes_service()
        note = service.get_note(note_id)

        output = [
            f'Note: "{note["name"]}"',
            f"ID: {note['id']}",
            f"Created: {note['creation_date']}",
            f"Modified: {note['modification_date']}",
            "",
            "Content:",
            "---",
            note["body"],
        ]

        return "\n".join(output)
    except Exception as e:
        logger.error("Failed to get note: %s", e)
        return f"Error getting note: {str(e)}"


@mcp.tool
def get_notes_list(start_date: str | None = None, end_date: str | None = None) -> str:
    """Get list of notes from Claude Diary folder

    Args:
        start_date: Start date in ISO format (YYYY-MM-DD) - not yet implemented
        end_date: End date in ISO format (YYYY-MM-DD) - not yet implemented

    Returns:
        Formatted list of notes with metadata

    Note:
        Currently returns all notes from Claude Diary folder.
        Date filtering is not yet implemented.
    """
    try:
        service = get_notes_service()
        notes = service.get_notes_list(start_date, end_date)

        if not notes:
            return "No notes found in Claude Diary folder"

        # Limit to 50 notes
        notes = notes[:50]

        # Format output
        output = [f"Found {len(notes)} note(s) in Claude Diary:\n"]

        for i, note in enumerate(notes, 1):
            name = note.get("name", "Untitled")
            note_id = note.get("id", "")
            creation_date = note.get("creation_date", "")
            modification_date = note.get("modification_date", "")

            output.append(f'{i}. "{name}"')
            output.append(f"   ID: {note_id}")
            output.append(f"   Created: {creation_date}")
            output.append(f"   Modified: {modification_date}")
            output.append("")

        return "\n".join(output)
    except Exception as e:
        logger.error("Failed to get notes list: %s", e)
        return f"Error getting notes: {str(e)}"


def run():
    """Run the MCP server"""
    logger.info("Starting mcp-inotes server...")
    mcp.run()  # Defaults to stdio transport
