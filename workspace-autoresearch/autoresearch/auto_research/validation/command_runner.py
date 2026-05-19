"""Structured subprocess command execution for validation."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import subprocess
import time


@dataclass
class CommandResult:
    """Result of a command executed during validation."""

    command: list[str]
    cwd: str | None
    returncode: int
    stdout: str
    stderr: str
    duration: float
    timed_out: bool = False


class CommandRunner:
    """Run commands safely without shell=True and return structured results."""

    def run(
        self,
        command: list[str],
        cwd: str | Path | None = None,
        timeout: int = 300,
    ) -> CommandResult:
        """Run a command and capture stdout, stderr, duration, and timeout status."""

        start = time.perf_counter()
        cwd_text = str(Path(cwd)) if cwd is not None else None
        try:
            completed = subprocess.run(
                command,
                cwd=cwd_text,
                timeout=timeout,
                shell=False,
                capture_output=True,
                text=True,
                check=False,
            )
            duration = time.perf_counter() - start
            return CommandResult(
                command=list(command),
                cwd=cwd_text,
                returncode=completed.returncode,
                stdout=completed.stdout,
                stderr=completed.stderr,
                duration=duration,
                timed_out=False,
            )
        except subprocess.TimeoutExpired as exc:
            duration = time.perf_counter() - start
            stdout = exc.stdout if isinstance(exc.stdout, str) else ""
            stderr = exc.stderr if isinstance(exc.stderr, str) else ""
            if stderr:
                stderr = stderr + "\n"
            stderr = stderr + f"Command timed out after {timeout} seconds."
            return CommandResult(
                command=list(command),
                cwd=cwd_text,
                returncode=124,
                stdout=stdout,
                stderr=stderr,
                duration=duration,
                timed_out=True,
            )
        except Exception as exc:
            duration = time.perf_counter() - start
            return CommandResult(
                command=list(command),
                cwd=cwd_text,
                returncode=1,
                stdout="",
                stderr=f"{type(exc).__name__}: {exc}",
                duration=duration,
                timed_out=False,
            )
