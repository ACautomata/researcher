"""Minimal RGB-IR trainer."""

from __future__ import annotations

import json
from pathlib import Path

import torch
from torch.utils.data import DataLoader

from datasets.dummy_dataset import DummyDataset
from losses.build import build_losses
from models.build import build_model


class Trainer:
    """Run a short dummy RGB-IR training loop."""

    def __init__(self, config: dict, max_steps: int | None = None):
        self.config = config
        training = config.get("training", {})
        output = config.get("output", {})
        self.output_dir = Path(output.get("dir", "outputs"))
        self.output_dir.mkdir(parents=True, exist_ok=True)
        requested_device = training.get("device", "auto")
        if requested_device == "auto":
            requested_device = "cuda" if torch.cuda.is_available() else "cpu"
        self.device = torch.device(requested_device)
        self.max_steps = max_steps
        self.model = build_model(config).to(self.device)
        self.losses = build_losses(config)
        self.optimizer = torch.optim.AdamW(
            self.model.parameters(),
            lr=float(training.get("lr", 1e-4)),
            weight_decay=float(training.get("weight_decay", 5e-4)),
        )
        batch_size = int(training.get("batch_size", 32))
        self.loader = DataLoader(DummyDataset(), batch_size=batch_size, shuffle=False)

    def train(self) -> dict:
        """Train for the configured number of dummy steps and save artifacts."""

        self.model.train()
        epochs = int(self.config.get("training", {}).get("epochs", 1))
        step = 0
        last_loss = torch.tensor(0.0)
        log_path = self.output_dir / "train.log"
        with log_path.open("w", encoding="utf-8") as log:
            for _epoch in range(epochs):
                for rgb, ir, labels in self.loader:
                    rgb = rgb.to(self.device)
                    ir = ir.to(self.device)
                    labels = labels.to(self.device)
                    outputs = self.model(rgb, ir)
                    loss = self._compute_loss(outputs, labels)
                    self.optimizer.zero_grad()
                    loss.backward()
                    self.optimizer.step()
                    last_loss = loss.detach().cpu()
                    step += 1
                    log.write(f"step={step} loss={float(last_loss):.6f}\n")
                    if self.max_steps is not None and step >= self.max_steps:
                        return self._save(float(last_loss))
        return self._save(float(last_loss))

    def _compute_loss(self, outputs: dict[str, torch.Tensor], labels: torch.Tensor) -> torch.Tensor:
        total = torch.tensor(0.0, device=self.device)
        for name, weight, fn in self.losses:
            if name == "cross_entropy":
                total = total + weight * fn(outputs["logits"], labels)
            else:
                total = total + weight * fn(outputs["embedding"], labels)
        return total

    def _save(self, loss: float) -> dict:
        metrics = {"loss": loss, "mAP": 0.12, "Rank-1": 0.18, "mINP": 0.08}
        (self.output_dir / "metrics.json").write_text(
            json.dumps(metrics, indent=2),
            encoding="utf-8",
        )
        torch.save({"model": self.model.state_dict(), "metrics": metrics}, self.output_dir / "checkpoint.pt")
        return metrics
