"""Generate config.yaml files for generated projects."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from auto_research.rts.schema import ResearchTaskSpecification


class ConfigGenerator:
    """Build generated-project configuration dictionaries from RTS and plans."""

    def generate(
        self,
        rts: ResearchTaskSpecification,
        plan: dict[str, Any],
        project_dir: str | Path,
    ) -> dict[str, Any]:
        """Generate a config dictionary for a generated project."""

        adapter = plan.get("adapter_requirements", {})
        return {
            "project": {
                "name": rts.meta.project_name,
                "task_type": rts.task.type,
            },
            "dataset": {
                "use_dummy": True,
                "modalities": list(rts.input.modalities),
            },
            "model": {
                "backbone": dict(rts.model.backbone),
                "components": list(rts.model.components),
                "heads": list(rts.model.heads),
            },
            "losses": list(rts.losses),
            "training": {
                "optimizer": rts.training.optimizer or "AdamW",
                "scheduler": rts.training.scheduler or "cosine",
                "batch_size": rts.training.batch_size or 32,
                "epochs": rts.training.epochs or 1,
                "lr": rts.training.lr or 1e-4,
                "weight_decay": rts.training.weight_decay or 5e-4,
                "mixed_precision": (
                    rts.training.mixed_precision
                    if rts.training.mixed_precision is not None
                    else False
                ),
                "device": "auto",
            },
            "evaluation": {
                "primary_metric": rts.goal.primary_metric,
                "secondary_metrics": list(rts.goal.secondary_metrics),
            },
            "output": {
                "dir": "outputs",
            },
            "search_space": dict(rts.search_space),
            "adapter": {
                "type": adapter.get("adapter_type", rts.adapter.type or "pytorch_yaml"),
                "train_entry": adapter.get("train_entry", rts.adapter.train_entry or "train.py"),
                "config_path": adapter.get(
                    "config_path",
                    rts.adapter.config_path or "configs/config.yaml",
                ),
            },
            "generation": {
                "project_dir": str(Path(project_dir)),
            },
        }

    def save(self, config: dict[str, Any], output_path: str | Path) -> None:
        """Save a generated config dictionary to YAML."""

        path = Path(output_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("w", encoding="utf-8") as handle:
            yaml.safe_dump(config, handle, sort_keys=False, allow_unicode=True)
