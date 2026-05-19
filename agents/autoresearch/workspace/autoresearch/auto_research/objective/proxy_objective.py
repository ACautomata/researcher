"""Proxy and weighted objective score calculation."""

from __future__ import annotations

from typing import Any


class ProxyObjectiveCalculator:
    """Compute scalar proxy scores from one or more metrics."""

    def compute(self, metrics: dict[str, Any], policy: dict[str, Any]) -> dict[str, Any]:
        """Compute an objective score and constraint status from metrics and policy."""

        effective_policy = dict(policy or {})
        policy_type = effective_policy.get("type", "single_metric")
        direction = effective_policy.get("direction", "maximize")
        warnings: list[str] = []
        details: dict[str, Any] = {"warnings": warnings, "contributions": {}}

        if policy_type == "weighted_sum":
            score = self._weighted_sum(metrics, effective_policy, details, warnings)
        else:
            score = self._single_metric(metrics, effective_policy, warnings)
            policy_type = "single_metric"

        if direction == "minimize":
            score = -score

        violated = self._violated_constraints(metrics, effective_policy.get("constraints", {}))

        return {
            "score": score,
            "passed_constraints": not violated,
            "violated_constraints": violated,
            "details": {
                **details,
                "policy_type": policy_type,
                "direction": direction,
            },
        }

    def _single_metric(
        self,
        metrics: dict[str, Any],
        policy: dict[str, Any],
        warnings: list[str],
    ) -> float:
        metric_name = str(policy.get("primary_metric") or policy.get("metric") or "")
        value = self._metric_value(metrics, metric_name)
        if value is None:
            warnings.append(f"Metric '{metric_name}' is missing; contribution defaults to 0.")
            return 0.0
        return value

    def _weighted_sum(
        self,
        metrics: dict[str, Any],
        policy: dict[str, Any],
        details: dict[str, Any],
        warnings: list[str],
    ) -> float:
        weights = policy.get("metrics", {})
        if not isinstance(weights, dict) or not weights:
            warnings.append("weighted_sum policy has no metric weights; score defaults to 0.")
            return 0.0

        total = 0.0
        contributions: dict[str, float] = {}
        for metric_name, raw_weight in weights.items():
            weight = self._float(raw_weight, default=0.0)
            value = self._metric_value(metrics, str(metric_name))
            if value is None:
                warnings.append(f"Metric '{metric_name}' is missing; contribution defaults to 0.")
                contributions[str(metric_name)] = 0.0
                continue
            contribution = weight * value
            contributions[str(metric_name)] = contribution
            total += contribution
        details["contributions"] = contributions
        return total

    def _violated_constraints(
        self,
        metrics: dict[str, Any],
        constraints: dict[str, Any],
    ) -> list[str]:
        if not isinstance(constraints, dict) or not constraints:
            return []

        violated: list[str] = []
        min_metrics = constraints.get("min_metrics", {})
        if isinstance(min_metrics, dict):
            for name, threshold in min_metrics.items():
                value = self._metric_value(metrics, str(name))
                if value is None or value < self._float(threshold):
                    violated.append(f"min_metrics.{name}")

        max_metrics = constraints.get("max_metrics", {})
        if isinstance(max_metrics, dict):
            for name, threshold in max_metrics.items():
                value = self._metric_value(metrics, str(name))
                if value is None or value > self._float(threshold):
                    violated.append(f"max_metrics.{name}")

        max_time = constraints.get("max_training_time_hours")
        if max_time is not None:
            value = self._metric_value(metrics, "training_time_hours")
            if value is not None and value > self._float(max_time):
                violated.append("max_training_time_hours")

        max_memory = constraints.get("max_gpu_memory_gb")
        if max_memory is not None:
            value = self._metric_value(metrics, "gpu_memory_gb")
            if value is not None and value > self._float(max_memory):
                violated.append("max_gpu_memory_gb")

        return violated

    def _metric_value(self, metrics: dict[str, Any], name: str) -> float | None:
        if not name:
            return None
        if name in metrics:
            return self._float(metrics[name], default=None)
        lower_lookup = {str(key).lower(): value for key, value in metrics.items()}
        if name.lower() in lower_lookup:
            return self._float(lower_lookup[name.lower()], default=None)
        return None

    def _float(self, value: Any, default: float | None = 0.0) -> float | None:
        if isinstance(value, bool):
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
