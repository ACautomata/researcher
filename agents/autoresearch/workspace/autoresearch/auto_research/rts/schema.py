"""Schema objects for the Research Task Specification protocol."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Optional


def _created_at_now() -> str:
    """Return a portable UTC timestamp for newly created RTS objects."""

    return datetime.now(timezone.utc).isoformat()


@dataclass
class RTSMeta:
    """Metadata describing where an RTS came from."""

    project_name: str = ""
    source_type: str = "manual"
    source_path: Optional[str] = None
    created_at: str = field(default_factory=_created_at_now)
    description: Optional[str] = None


@dataclass
class RTSTask:
    """High-level research task definition."""

    type: str = "general_pytorch"
    research_problem: str = ""
    learning_paradigm: Optional[str] = None


@dataclass
class RTSGoal:
    """Optimization target for automatic training and tuning."""

    primary_metric: str = ""
    optimization_direction: str = "maximize"
    secondary_metrics: list[str] = field(default_factory=list)


@dataclass
class RTSInput:
    """Expected model input shape and modalities."""

    modalities: list[str] = field(default_factory=list)
    data_format: Optional[str] = None
    input_shape: Optional[list[int]] = None


@dataclass
class RTSOutput:
    """Expected model output contract."""

    type: str = ""
    dimension: Optional[int] = None
    description: Optional[str] = None


@dataclass
class RTSBaseline:
    """Baseline implementation or template hints."""

    template: Optional[str] = None
    name: Optional[str] = None
    source: Optional[str] = None
    description: Optional[str] = None


@dataclass
class RTSModel:
    """Model architecture description."""

    backbone: dict[str, Any] = field(default_factory=dict)
    components: list[dict[str, Any]] = field(default_factory=list)
    heads: list[dict[str, Any]] = field(default_factory=list)


@dataclass
class RTSTraining:
    """Training hyperparameters and runtime preferences."""

    optimizer: Optional[str] = None
    scheduler: Optional[str] = None
    batch_size: Optional[int] = None
    epochs: Optional[int] = None
    lr: Optional[float] = None
    weight_decay: Optional[float] = None
    mixed_precision: Optional[bool] = None


@dataclass
class RTSImplementation:
    """Expected generated project structure."""

    required_files: list[str] = field(default_factory=list)
    expected_modules: list[str] = field(default_factory=list)
    notes: Optional[str] = None


@dataclass
class RTSValidation:
    """Validation checks expected before launching full experiments."""

    required_checks: list[str] = field(
        default_factory=lambda: [
            "import_check",
            "dummy_forward",
            "loss_backward",
            "one_batch_train",
            "config_load",
            "checkpoint_save_load",
        ]
    )


@dataclass
class RTSAdapter:
    """Adapter bridge to the existing auto_research training layer."""

    type: str = ""
    train_entry: Optional[str] = None
    config_path: Optional[str] = None
    output_dir_arg: Optional[str] = None
    fixed_args: list[str] = field(default_factory=list)
    param_arg_map: dict[str, str] = field(default_factory=dict)
    notes: Optional[str] = None


@dataclass
class ResearchTaskSpecification:
    """Intermediate representation between research ideas and runnable training tasks."""

    meta: RTSMeta = field(default_factory=RTSMeta)
    task: RTSTask = field(default_factory=RTSTask)
    goal: RTSGoal = field(default_factory=RTSGoal)
    input: RTSInput = field(default_factory=RTSInput)
    output: RTSOutput = field(default_factory=RTSOutput)
    baseline: RTSBaseline = field(default_factory=RTSBaseline)
    model: RTSModel = field(default_factory=RTSModel)
    losses: list[dict[str, Any]] = field(default_factory=list)
    training: RTSTraining = field(default_factory=RTSTraining)
    datasets: list[dict[str, Any]] = field(default_factory=list)
    metrics: list[str] = field(default_factory=list)
    search_space: dict[str, Any] = field(default_factory=dict)
    objective_policy: dict[str, Any] = field(default_factory=dict)
    ablation: list[dict[str, Any]] = field(default_factory=list)
    implementation: RTSImplementation = field(default_factory=RTSImplementation)
    validation: RTSValidation = field(default_factory=RTSValidation)
    adapter: RTSAdapter = field(default_factory=RTSAdapter)
    risks: list[str] = field(default_factory=list)
    extra: dict[str, Any] = field(default_factory=dict)
