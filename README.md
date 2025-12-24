# mcp-inotes

Lightweight MCP server for Apple Notes. 

## Constrains
Works exclusively with "Claude Diary" folder for safe diary management. No delete tool, just create / append only.

## Install

```bash
git clone <your-repo-url> mcp-inotes
cd mcp-inotes
uv sync
```

## Configuration

Add to `~/.mcp.json` or `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-inotes": {
      "command": "uv",
      "args": [
        "--directory",
        "/absolute/path/to/mcp-inotes",
        "run",
        "python",
        "main.py"
      ]
    }
  }
}
```

**Required:** Create a "Claude Diary" folder in Apple Notes before use.

## Tools

- `create_note(title, body)` - Create new note
- `get_note(note_id)` - Read full content
- `append_to_note(note_id, content)` - Add content (append only)
- `get_notes_list()` - List all notes

## Safety Features

✅ Hardcoded to "Claude Diary" folder - cannot modify other notes
✅ Append-only - no overwrite or delete
✅ No folder selection - prevents data loss

## Requirements

- macOS
- Python 3.12+
- Apple Notes.app

## License

MIT
