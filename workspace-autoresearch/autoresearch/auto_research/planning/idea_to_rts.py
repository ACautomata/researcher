"""Heuristic conversion from natural-language research ideas to RTS."""

from __future__ import annotations

from typing import Any

from auto_research.rts.schema import (
    RTSAdapter,
    RTSBaseline,
    RTSGoal,
    RTSImplementation,
    RTSInput,
    RTSMeta,
    RTSModel,
    RTSOutput,
    RTSTask,
    RTSTraining,
    ResearchTaskSpecification,
)


class IdeaToRTSConverter:
    """Convert idea text into a first-draft RTS with offline heuristics."""

    def convert(self, idea_text: str, project_name: str) -> ResearchTaskSpecification:
        """Convert natural-language idea text into ResearchTaskSpecification."""

        if not isinstance(idea_text, str) or not idea_text.strip():
            raise ValueError("idea_text must be a non-empty string.")
        if not isinstance(project_name, str) or not project_name.strip():
            raise ValueError("project_name must be a non-empty string.")

        normalized = self._normalize(idea_text)
        task_type = self._detect_task_type(normalized)
        spec = self._task_defaults(task_type)
        components = self._detect_components(normalized, task_type)
        losses = self._detect_losses(normalized, spec["losses"])

        return ResearchTaskSpecification(
            meta=RTSMeta(
                project_name=project_name.strip(),
                source_type="idea",
                description=idea_text.strip(),
            ),
            task=RTSTask(
                type=task_type,
                research_problem=idea_text.strip(),
                learning_paradigm=spec["learning_paradigm"],
            ),
            goal=RTSGoal(
                primary_metric=spec["primary_metric"],
                optimization_direction=spec["optimization_direction"],
                secondary_metrics=list(spec["secondary_metrics"]),
            ),
            input=RTSInput(
                modalities=list(spec["modalities"]),
                data_format=spec["data_format"],
                input_shape=spec["input_shape"],
            ),
            output=RTSOutput(
                type=spec["output_type"],
                dimension=spec["output_dimension"],
                description=spec["output_description"],
            ),
            baseline=RTSBaseline(
                template=spec["baseline_template"],
                name=f"{spec['baseline_template']} baseline",
                description="Heuristic baseline selected from idea text.",
            ),
            model=RTSModel(
                backbone=spec["backbone"],
                components=components,
                heads=spec["heads"],
            ),
            losses=losses,
            training=RTSTraining(
                optimizer="AdamW",
                scheduler="cosine",
                batch_size=32,
                epochs=1,
                lr=1e-4,
                weight_decay=5e-4,
                mixed_precision=False,
            ),
            datasets=[],
            metrics=self._unique(
                [spec["primary_metric"], *spec["secondary_metrics"], "loss"]
            ),
            search_space=self._default_search_space(task_type),
            objective_policy={
                "type": "single_metric",
                "primary_metric": spec["primary_metric"],
                "direction": spec["optimization_direction"],
                "metrics": {},
                "constraints": {},
            },
            implementation=RTSImplementation(
                required_files=["train.py", "configs/config.yaml"],
                expected_modules=["models", "datasets", "losses", "trainers", "evaluators"],
                notes="Generated from idea text using heuristic rules.",
            ),
            adapter=RTSAdapter(
                type="pytorch_yaml",
                train_entry="train.py",
                config_path="configs/config.yaml",
                fixed_args=[],
                param_arg_map={},
            ),
            extra={
                "idea_text": idea_text.strip(),
                "conversion_method": "heuristic",
            },
        )

    def build_prompt(self, idea_text: str) -> str:
        """Build a future LLM prompt for idea-to-RTS conversion."""

        return (
            "Convert the following research idea into an AutoResearch RTS YAML. "
            "Return structured fields only.\n\n"
            f"{idea_text.strip()}"
        )

    def parse_llm_output(self, output_text: str) -> dict[str, Any]:
        """Placeholder parser for future LLM output."""

        raise NotImplementedError("LLM output parsing is not implemented in the heuristic version.")

    def convert_with_llm(
        self,
        idea_text: str,
        project_name: str,
    ) -> ResearchTaskSpecification:
        """Placeholder for future LLM-backed conversion."""

        raise NotImplementedError("LLM-backed idea conversion is not implemented yet.")

    def _detect_task_type(self, text: str) -> str:
        if self._contains_any(text, ["rgb-ir", "rgb ir", "rgb/ir", "跨模态行人重识别", "红外", "可见光"]):
            return "rgb_ir_reid"
        if self._contains_any(text, ["行人重识别", "reid", "person re-identification", "person reid"]):
            return "person_reid"
        if self._contains_any(text, ["姿态估计", "pose", "keypoint", "heatmap"]):
            return "pose_estimation"
        if self._contains_any(text, ["阴影去除", "shadow removal", "shadow-removal"]):
            return "shadow_removal"
        if self._contains_any(text, ["扩散", "diffusion", "restoration", "修复"]):
            return "diffusion_restoration"
        if self._contains_any(text, ["分类", "classification"]):
            return "image_classification"
        return "general_pytorch"

    def _task_defaults(self, task_type: str) -> dict[str, Any]:
        defaults: dict[str, dict[str, Any]] = {
            "rgb_ir_reid": {
                "modalities": ["RGB", "IR"],
                "data_format": "paired_image_folders",
                "input_shape": [3, 256, 128],
                "output_type": "embedding",
                "output_dimension": 512,
                "output_description": "Cross-modal person embedding.",
                "primary_metric": "mAP",
                "secondary_metrics": ["Rank-1", "mINP"],
                "optimization_direction": "maximize",
                "baseline_template": "rgb_ir_reid",
                "losses": ["cross_entropy", "triplet"],
                "learning_paradigm": "supervised",
                "backbone": {"name": "resnet50", "pretrained": True},
                "heads": [{"name": "identity_classifier", "type": "linear"}],
            },
            "person_reid": {
                "modalities": ["RGB"],
                "data_format": "image_folders",
                "input_shape": [3, 256, 128],
                "output_type": "embedding",
                "output_dimension": 512,
                "output_description": "Person identity embedding.",
                "primary_metric": "mAP",
                "secondary_metrics": ["Rank-1"],
                "optimization_direction": "maximize",
                "baseline_template": "person_reid",
                "losses": ["cross_entropy", "triplet"],
                "learning_paradigm": "supervised",
                "backbone": {"name": "resnet50", "pretrained": True},
                "heads": [{"name": "identity_classifier", "type": "linear"}],
            },
            "pose_estimation": {
                "modalities": ["RGB"],
                "data_format": "keypoint_annotations",
                "input_shape": [3, 256, 192],
                "output_type": "heatmap",
                "output_dimension": None,
                "output_description": "Keypoint heatmaps.",
                "primary_metric": "AP",
                "secondary_metrics": ["PCK"],
                "optimization_direction": "maximize",
                "baseline_template": "pose_estimation",
                "losses": ["mse"],
                "learning_paradigm": "supervised",
                "backbone": {"name": "hrnet_or_resnet", "pretrained": True},
                "heads": [{"name": "heatmap_head", "type": "conv"}],
            },
            "shadow_removal": {
                "modalities": ["RGB"],
                "data_format": "image_pairs",
                "input_shape": [3, 256, 256],
                "output_type": "image",
                "output_dimension": None,
                "output_description": "Shadow-free restored image.",
                "primary_metric": "PSNR",
                "secondary_metrics": ["SSIM"],
                "optimization_direction": "maximize",
                "baseline_template": "shadow_removal",
                "losses": ["l1"],
                "learning_paradigm": "supervised",
                "backbone": {"name": "unet", "pretrained": False},
                "heads": [{"name": "restoration_head", "type": "conv"}],
            },
            "diffusion_restoration": {
                "modalities": ["RGB"],
                "data_format": "image_pairs",
                "input_shape": [3, 256, 256],
                "output_type": "image",
                "output_dimension": None,
                "output_description": "Restored image.",
                "primary_metric": "PSNR",
                "secondary_metrics": ["SSIM"],
                "optimization_direction": "maximize",
                "baseline_template": "diffusion_restoration",
                "losses": ["l1", "mse"],
                "learning_paradigm": "generative",
                "backbone": {"name": "diffusion_unet", "pretrained": False},
                "heads": [{"name": "denoising_head", "type": "diffusion"}],
            },
            "image_classification": {
                "modalities": ["RGB"],
                "data_format": "image_folders",
                "input_shape": [3, 224, 224],
                "output_type": "class_logits",
                "output_dimension": None,
                "output_description": "Class logits.",
                "primary_metric": "accuracy",
                "secondary_metrics": ["loss"],
                "optimization_direction": "maximize",
                "baseline_template": "image_classification",
                "losses": ["cross_entropy"],
                "learning_paradigm": "supervised",
                "backbone": {"name": "resnet18", "pretrained": True},
                "heads": [{"name": "classification_head", "type": "linear"}],
            },
        }
        return defaults.get(
            task_type,
            {
                "modalities": ["Tensor"],
                "data_format": "dummy_tensor",
                "input_shape": [32],
                "output_type": "class_logits",
                "output_dimension": None,
                "output_description": "Generic model output.",
                "primary_metric": "loss",
                "secondary_metrics": [],
                "optimization_direction": "minimize",
                "baseline_template": "general_pytorch",
                "losses": ["cross_entropy"],
                "learning_paradigm": "unknown",
                "backbone": {"name": "mlp", "pretrained": False},
                "heads": [{"name": "classification_head", "type": "linear"}],
            },
        )

    def _detect_components(self, text: str, task_type: str) -> list[dict[str, Any]]:
        components: list[dict[str, Any]] = []
        if self._contains_any(text, ["attention", "注意力"]):
            name = "cross_modal_attention" if task_type == "rgb_ir_reid" else "attention_module"
            components.append(
                {
                    "name": name,
                    "type": "attention",
                    "purpose": "Fuse or refine features based on idea text.",
                    "input": "features",
                    "output": "refined_features",
                }
            )
        if self._contains_any(text, ["fusion", "融合"]):
            components.append(
                {
                    "name": "feature_fusion",
                    "type": "fusion",
                    "purpose": "Fuse multi-source features.",
                    "input": "multi_modal_features",
                    "output": "fused_features",
                }
            )
        return components

    def _detect_losses(self, text: str, default_losses: list[str]) -> list[dict[str, Any]]:
        names = list(default_losses)
        if self._contains_any(text, ["center", "中心约束", "center constraint", "center loss"]):
            names.append("center_constraint")
        if self._contains_any(text, ["contrastive", "对比学习", "对比损失"]):
            names.append("contrastive")
        return [
            {"name": name, "weight": 1.0 if name != "center_constraint" else 0.01, "params": {}}
            for name in self._unique(names)
        ]

    def _default_search_space(self, task_type: str) -> dict[str, Any]:
        space: dict[str, Any] = {
            "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
            "batch_size": {"type": "categorical", "choices": [32, 64]},
        }
        if task_type in {"rgb_ir_reid", "person_reid"}:
            space["weight_decay"] = {"type": "float", "low": 1e-6, "high": 1e-3, "log": True}
        return space

    def _contains_any(self, text: str, keywords: list[str]) -> bool:
        return any(keyword.lower() in text for keyword in keywords)

    def _normalize(self, text: str) -> str:
        return text.lower().replace("－", "-").replace("—", "-")

    def _unique(self, values: list[Any]) -> list[Any]:
        result: list[Any] = []
        for value in values:
            if value not in result:
                result.append(value)
        return result
