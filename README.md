# mcp-inotes

![Python](https://img.shields.io/badge/python-3.12+-blue) ![License](https://img.shields.io/badge/license-MIT-green)

A lightweight [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that enables Claude and other LLMs to interact with Apple Notes.

## About

This MCP server gives Claude the ability to create, read, and append to notes in Apple Notes. It's designed with a safety-first approach: all operations are restricted to a single designated folder, and the server only supports append operations (no overwrites or deletions).

Perfect for using Claude as your AI journaling assistant, note-taking companion, or personal knowledge base manager.

## Features

- Create new notes with title and body
- Read existing notes by ID
- Append content to notes (no overwrites)
- List all notes with metadata
- Safety-first: Operations restricted to "Claude Diary" folder only
- Append-only design prevents accidental data loss
- Built with [FastMCP](https://github.com/jlowin/fastmcp)

## Prerequisites

- **macOS** - Uses AppleScript to interact with Notes.app
- **Python 3.12+**
- **Apple Notes.app**
- **Claude Desktop** or another MCP-compatible client
- Basic familiarity with [MCP servers](https://modelcontextprotocol.io/)

## Installation

```bash
git clone https://github.com/pongsapakl/mcp-inotes.git
cd mcp-inotes
uv sync
```

## Configuration

Add to your MCP settings file. For Claude Desktop, edit:
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Alternative: `~/.mcp.json`

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

**Important**: Replace `/absolute/path/to/mcp-inotes` with the actual path where you cloned this repository.

## Required Setup

Before using the server, **create a folder named "Claude Diary"** in Apple Notes:

1. Open Apple Notes
2. Right-click in the sidebar
3. Select "New Folder"
4. Name it exactly: `Claude Diary`

This folder is where all notes will be created and managed.

## Available Tools

- `create_note(title, body)` - Create new note in Claude Diary folder
- `get_note(note_id)` - Read full note content and metadata
- `append_to_note(note_id, content)` - Append content to existing note (append-only)
- `get_notes_list()` - List all notes with IDs and timestamps

## Usage Examples

Here's how Claude can use these tools in practice:

**Creating a daily journal entry:**
```
User: "Create a journal entry for today about my morning routine"
Claude: [Uses create_note("Daily Journal - 2026-01-15", "Woke up at 7am...")]
```

**Building on previous notes:**
```
User: "Add my evening reflections to today's journal"
Claude: [Uses get_notes_list() to find today's note, then append_to_note()]
```

**Searching through your notes:**
```
User: "What did I write about my project last week?"
Claude: [Uses get_notes_list(), then get_note() to read relevant entries]
```

## Safety & Constraints

This server is designed with deliberate limitations for safety:

**Folder Restriction**
- All operations are hardcoded to work **only** with the "Claude Diary" folder
- Cannot access, modify, or delete notes in other folders
- Prevents accidental changes to important notes elsewhere in your Apple Notes

**Append-Only Operations**
- No delete functionality
- No overwrite functionality
- Only supports creating new notes and appending to existing ones
- Protects against accidental data loss

**Why "Claude Diary"?**
The folder name is intentionally hardcoded rather than configurable. This constraint ensures you always know exactly where the MCP server can operate, reducing the risk of unintended modifications to other notes.

## Limitations

- **Date filtering not implemented**: The `start_date` and `end_date` parameters in `get_notes_list()` are accepted but not yet functional. Currently returns all notes from the Claude Diary folder.
- **macOS only**: Relies on AppleScript, which is macOS-specific
- **Single folder**: Cannot manage notes across multiple folders
- **No delete operations**: By design, but means you'll need to manually clean up unwanted notes in Apple Notes

## Troubleshooting

**"Folder not found" error**
- Make sure you've created a folder named exactly "Claude Diary" in Apple Notes
- The name is case-sensitive

**Server not connecting**
- Verify the absolute path in your MCP config file is correct
- Try running `uv sync` again to ensure dependencies are installed
- Check Claude Desktop logs: `~/Library/Logs/Claude/`

**AppleScript permission denied**
- macOS may prompt you to grant permissions the first time
- Check System Settings → Privacy & Security → Automation
- Ensure Claude/your MCP client can control Apple Notes

**Notes not appearing**
- Make sure you're looking in the "Claude Diary" folder in Apple Notes
- Try refreshing the Notes app
- Check that the note IDs being used are valid

## Contributing

Contributions are welcome! Feel free to:
- Report issues on [GitHub](https://github.com/pongsapakl/mcp-inotes/issues)
- Submit pull requests for bug fixes or improvements
- Suggest new features (while respecting the safety-first design philosophy)

## License

MIT

---

Built with [FastMCP](https://github.com/jlowin/fastmcp) | Learn more about [Model Context Protocol](https://modelcontextprotocol.io/)
