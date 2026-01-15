"""Apple Notes service using AppleScript"""

import subprocess
from typing import Optional


class NotesService:
    """AppleScript wrapper for Apple Notes operations

    All operations are hardcoded to work ONLY with the 'Claude Diary' folder.
    This prevents accidental modification of other notes.
    """

    FOLDER = "Claude Diary"  # Hardcoded - NOT configurable

    def create_note(self, title: str, body: str) -> str:
        """Create a new note in Claude Diary folder

        Args:
            title: Note title
            body: Note body content

        Returns:
            Note ID (x-coredata:// URL)

        Raises:
            Exception: If AppleScript execution fails
        """
        # Escape quotes, backslashes, and convert newlines to HTML breaks
        title = title.replace("\\", "\\\\").replace('"', '\\"')
        body = body.replace("\\", "\\\\").replace('"', '\\"').replace('\n', '<br>')

        script = f'''
        tell application "Notes"
            tell folder "{self.FOLDER}"
                set newNote to make new note with properties {{name:"{title}", body:"{body}"}}
                return id of newNote
            end tell
        end tell
        '''

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)

        if result.returncode != 0:
            raise Exception(f"Failed to create note: {result.stderr}")

        return result.stdout.strip()

    def get_note(self, note_id: str) -> dict:
        """Get note details by ID

        Args:
            note_id: Note ID (x-coredata:// URL)

        Returns:
            dict with keys: id, name, body, creation_date, modification_date

        Raises:
            Exception: If note not found or AppleScript fails
        """
        note_id = note_id.replace("\\", "\\\\").replace('"', '\\"')

        script = f'''
        tell application "Notes"
            set theNote to note id "{note_id}"
            set noteData to {{}}
            set end of noteData to id of theNote
            set end of noteData to name of theNote
            set end of noteData to body of theNote
            set end of noteData to creation date of theNote as string
            set end of noteData to modification date of theNote as string

            set AppleScript's text item delimiters to "|~|"
            return noteData as text
        end tell
        '''

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)

        if result.returncode != 0:
            raise Exception(f"Failed to get note: {result.stderr}")

        parts = result.stdout.strip().split("|~|")
        if len(parts) < 5:
            raise Exception("Invalid response from AppleScript")

        return {
            "id": parts[0],
            "name": parts[1],
            "body": parts[2],
            "creation_date": parts[3],
            "modification_date": parts[4],
        }

    def append_to_note(self, note_id: str, content: str) -> None:
        """Append content to existing note (APPEND ONLY - no overwrite/delete)

        Args:
            note_id: Note ID
            content: Content to append

        Raises:
            Exception: If note not found or append fails
        """
        note_id = note_id.replace("\\", "\\\\").replace('"', '\\"')
        content = content.replace("\\", "\\\\").replace('"', '\\"').replace('\n', '<br>')

        script = f'''
        tell application "Notes"
            set theNote to note id "{note_id}"
            set body of theNote to (body of theNote) & "<br><br>{content}"
        end tell
        '''

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)

        if result.returncode != 0:
            raise Exception(f"Failed to append to note: {result.stderr}")

    def get_notes_list(self, start_date: Optional[str] = None, end_date: Optional[str] = None) -> list[dict]:
        """Get list of notes from Claude Diary folder, optionally filtered by date range

        Args:
            start_date: ISO format date string (YYYY-MM-DD) - currently not implemented
            end_date: ISO format date string (YYYY-MM-DD) - currently not implemented

        Returns:
            List of note dicts with id, name, creation_date, modification_date

        Note:
            Date filtering is not yet implemented - returns all notes from Claude Diary folder
        """
        script = f'''
        tell application "Notes"
            set allNotes to notes of folder "{self.FOLDER}"
            set notesList to {{}}
            repeat with theNote in allNotes
                set noteInfo to {{}}
                set end of noteInfo to id of theNote
                set end of noteInfo to name of theNote
                set end of noteInfo to creation date of theNote as string
                set end of noteInfo to modification date of theNote as string
                set end of notesList to noteInfo
            end repeat

            set AppleScript's text item delimiters to "|~|"
            set output to {{}}
            repeat with noteInfo in notesList
                set end of output to noteInfo as text
            end repeat
            set AppleScript's text item delimiters to "||"
            return output as text
        end tell
        '''

        result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True, check=False)

        if result.returncode != 0:
            raise Exception(f"Failed to get notes: {result.stderr}")

        output = result.stdout.strip()
        if not output:
            return []

        notes = []
        for note_str in output.split("||"):
            if not note_str:
                continue
            parts = note_str.split("|~|")
            if len(parts) >= 4:
                notes.append(
                    {"id": parts[0], "name": parts[1], "creation_date": parts[2], "modification_date": parts[3]}
                )

        # TODO: Implement date filtering if start_date/end_date provided
        # For now, return all notes
        return notes
