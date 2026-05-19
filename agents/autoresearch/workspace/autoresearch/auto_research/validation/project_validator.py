"""Validate generated projects before handoff to the training framework."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys
from typing import Any

from auto_research.validation.command_runner import CommandResult, CommandRunner

_REQUIRED_PATHS = [
    "train.py",
    "test.py",
    "configs/config.yaml",
    "models",
    "losses",
    "datasets",
    "trainers",
    "evaluators",
]


class ProjectValidator:
    """Run validation checks for a generated project."""

    def __init__(self, timeout: int = 300):
        """Initialize the validator with a command timeout in seconds."""

        self.timeout = timeout
        self.runner = CommandRunner()

    def validate(
        self,
        project_dir: str | Path,
        config_path: str | Path | None = None,
    ) -> dict[str, Any]:
        """Validate a generated project and write validation artifacts."""

        root = Path(project_dir)
        if config_path is None:
            config = root / "configs" / "config.yaml"
        else:
            config = Path(config_path)
            if not config.is_absolute() and not config.exists():
                config = root / config

        checks: list[dict[str, Any]] = []
        errors: list[str] = []
        warnings: list[str] = []

        checks.append(self._check_required_files(root))
        checks.append(self._check_config_exists(config))

        train_exists = (root / "train.py").exists()
        test_exists = (root / "test.py").exists()
        config_exists = config.exists()

        if train_exists and test_exists:
            checks.append(
                self._command_check(
                    "py_compile",
                    [sys.executable, "-m", "py_compile", "train.py", "test.py"],
                    root,
                )
            )
        else:
            checks.append(self._skipped_check("py_compile", "train.py or test.py is missing."))

        checks.append(
            self._command_check(
                "import_check",
                [
                    sys.executable,
                    "-c",
                    "import models; import losses; import datasets; import trainers; import evaluators",
                ],
                root,
            )
        )

        if train_exists and config_exists:
            checks.append(
                self._command_check(
                    "config_load",
                    [
                        sys.executable,
                        "train.py",
                        "--config",
                        self._relative_config_arg(root, config),
                        "--dry-run",
                    ],
                    root,
                )
            )
        else:
            checks.append(self._skipped_check("config_load", "train.py or config file is missing."))

        if test_exists and config_exists:
            checks.append(
                self._command_check(
                    "dummy_forward",
                    [
                        sys.executable,
                        "test.py",
                        "--config",
                        self._relative_config_arg(root, config),
                        "--mode",
                        "dummy-forward",
                    ],
                    root,
                )
            )
        else:
            checks.append(self._skipped_check("dummy_forward", "test.py or config file is missing."))

        if train_exists and config_exists:
            checks.append(
                self._command_check(
                    "one_batch_train",
                    [
                        sys.executable,
                        "train.py",
                        "--config",
                        self._relative_config_arg(root, config),
                        "--max-steps",
                        "1",
                    ],
                    root,
                )
            )
        else:
            checks.append(self._skipped_check("one_batch_train", "train.py or config file is missing."))

        checks.append(self._check_file_exists("checkpoint_exists", root / "outputs" / "checkpoint.pt"))
        checks.append(self._check_file_exists("metrics_json_exists", root / "outputs" / "metrics.json"))
        checks.append(self._check_metrics_json(root / "outputs" / "metrics.json", root / "configs" / "config.yaml"))

        for check in checks:
            if not check["passed"] and check["name"] != "import_check":
                errors.append(f"{check['name']}: {check['details']}")
            elif not check["passed"]:
                errors.append(f"{check['name']}: {check['details']}")

        result_path = root / "validation_result.json"
        report_path = root / "validation_report.md"
        result = {
            "passed": not errors,
            "project_dir": str(root),
            "config_path": str(config),
            "checks": checks,
            "errors": errors,
            "warnings": warnings,
            "validation_result_path": str(result_path),
            "validation_report_path": str(report_path),
        }
        self._save_json(result, result_path)
        report_path.write_text(self._render_report(result), encoding="utf-8")
        return result

    def _check_required_files(self, root: Path) -> dict[str, Any]:
        missing = [item for item in _REQUIRED_PATHS if not (root / item).exists()]
        return {
            "name": "required_files_exist",
            "passed": not missing,
            "details": "All required files exist." if not missing else f"Missing: {', '.join(missing)}",
        }

    def _check_config_exists(self, config: Path) -> dict[str, Any]:
        return {
            "name": "config_exists",
            "passed": config.exists(),
            "details": f"Config exists: {config}" if config.exists() else f"Missing config: {config}",
        }

    def _command_check(self, name: str, command: list[str], cwd: Path) -> dict[str, Any]:
        result = self.runner.run(command, cwd=cwd, timeout=self.timeout)
        return {
            "name": name,
            "passed": result.returncode == 0,
            "command": result.command,
            "returncode": result.returncode,
            "stdout": self._summary(result.stdout),
            "stderr": self._summary(result.stderr),
            "duration": result.duration,
            "timed_out": result.timed_out,
            "details": self._command_details(result),
        }

    def _skipped_check(self, name: str, details: str) -> dict[str, Any]:
        return {
            "name": name,
            "passed": False,
            "skipped": True,
            "details": details,
        }

    def _check_file_exists(self, name: str, path: Path) -> dict[str, Any]:
        return {
            "name": name,
            "passed": path.exists(),
            "details": f"File exists: {path}" if path.exists() else f"Missing file: {path}",
        }

    def _check_metrics_json(self, metrics_path: Path, config_path: Path) -> dict[str, Any]:
        if not metrics_path.exists():
            return {
                "name": "metrics_json_valid",
                "passed": False,
                "details": f"Missing metrics JSON: {metrics_path}",
            }
        try:
            data = json.loads(metrics_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return {
                "name": "metrics_json_valid",
                "passed": False,
                "details": f"Invalid JSON: {exc}",
            }
        if not isinstance(data, dict):
            return {
                "name": "metrics_json_valid",
                "passed": False,
                "details": "metrics.json must contain an object.",
            }
        required = ["loss"]
        if self._looks_like_rgb_ir_reid(config_path):
            required.extend(["mAP", "Rank-1", "mINP"])
        missing = [key for key in required if key not in data]
        return {
            "name": "metrics_json_valid",
            "passed": not missing,
            "details": "metrics.json is valid." if not missing else f"Missing metrics: {', '.join(missing)}",
        }

    def _looks_like_rgb_ir_reid(self, config_path: Path) -> bool:
        if not config_path.exists():
            return False
        text = config_path.read_text(encoding="utf-8")
        return "rgb_ir_reid" in text

    def _relative_config_arg(self, root: Path, config: Path) -> str:
        try:
            return str(config.relative_to(root))
        except ValueError:
            return str(config)

    def _command_details(self, result: CommandResult) -> str:
        if result.returncode == 0:
            return "Command completed successfully."
        if result.timed_out:
            return "Command timed out."
        return f"Command failed with return code {result.returncode}."

    def _summary(self, text: str, limit: int = 1200) -> str:
        if len(text) <= limit:
            return text
        return text[:limit] + "\n...<truncated>..."

    def _save_json(self, result: dict[str, Any], path: Path) -> None:
        serializable = json.loads(json.dumps(result, default=asdict))
        path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    def _render_report(self, result: dict[str, Any]) -> str:
        lines = [
            "# Validation Report",
            "",
            "## Project",
            "",
            f"- project_dir: {result['project_dir']}",
            f"- config_path: {result['config_path']}",
            "",
            "## Summary",
            "",
            f"- passed: {result['passed']}",
            f"- total_checks: {len(result['checks'])}",
            "",
            "## Checks",
            "",
        ]
        for check in result["checks"]:
            lines.extend(
                [
                    f"### {check['name']}",
                    "",
                    f"- passed: {check['passed']}",
                    f"- details: {check.get('details', '')}",
                ]
            )
            if "command" in check:
                lines.extend(
                    [
                        f"- command: `{' '.join(check['command'])}`",
                        f"- returncode: {check.get('returncode')}",
                        f"- stdout: {check.get('stdout', '').strip() or 'None'}",
                        f"- stderr: {check.get('stderr', '').strip() or 'None'}",
                    ]
                )
            lines.append("")

        lines.extend(
            [
                "## Errors",
                "",
                self._list_or_none(result["errors"]),
                "",
                "## Warnings",
                "",
                self._list_or_none(result["warnings"]),
                "",
                "## Next Steps",
                "",
                "- If validation passed, the project is ready for task card generation.",
                "- If validation failed, inspect errors and command stderr before handoff.",
                "",
            ]
        )
        return "\n".join(lines)

    def _list_or_none(self, items: list[str]) -> str:
        if not items:
            return "- None"
        return "\n".join(f"- {item}" for item in items)
