"""Read free-form research ideas from text or markdown files."""

from __future__ import annotations

from pathlib import Path


class IdeaReader:
    """Read idea text from direct input or local files."""

    def read_from_text(self, idea_text: str) -> str:
        """Return normalized idea text from a user-provided string."""

        if not isinstance(idea_text, str) or not idea_text.strip():
            raise ValueError("idea_text must be a non-empty string.")
        return idea_text.strip()

    def read_from_file(self, idea_file: str | Path) -> str:
        """Read idea text from a .txt or .md file."""

        path = Path(idea_file)
        if not path.exists() or not path.is_file():
            raise FileNotFoundError(f"Idea file does not exist: '{path}'.")
        if path.suffix.lower() not in {".txt", ".md"}:
            raise ValueError("IdeaReader only supports .txt and .md files.")
        return self.read_from_text(path.read_text(encoding="utf-8"))
