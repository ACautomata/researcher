"""Tests for RTS to requirement.md generation."""

from __future__ import annotations

from auto_research.cli import build_rgb_ir_reid_example
from auto_research.planning.requirement_generator import RequirementGenerator


def test_generate_requirement_from_valid_rts() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    assert isinstance(markdown, str)
    assert markdown.startswith("# Requirement Document")


def test_requirement_contains_pipeline_role() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    assert "Document Role in the Auto-Research Pipeline" in markdown


def test_requirement_contains_auto_training_interface() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    assert "Interface with Existing Auto-Training Module" in markdown


def test_requirement_contains_validation_criteria() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    assert "Validation Criteria" in markdown


def test_requirement_contains_search_space() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    assert "Hyperparameter Search Space" in markdown
    assert "center_loss_weight" in markdown


def test_loss_role_center_constraint() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    assert "feature compactness constraint" in markdown


def test_baseline_fallback() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.baseline.template = None

    markdown = RequirementGenerator().generate(rts)

    assert "general_pytorch" in markdown
    assert "No explicit baseline template is provided" in markdown


def test_adapter_fallback() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")
    rts.adapter.type = ""

    markdown = RequirementGenerator().generate(rts)

    assert "pytorch_yaml" in markdown


def test_requirement_contains_all_required_headings() -> None:
    rts = build_rgb_ir_reid_example("rgb_ir_attention_test")

    markdown = RequirementGenerator().generate(rts)

    headings = [
        "# Requirement Document",
        "## 1. Document Role in the Auto-Research Pipeline",
        "## 2. Project Overview",
        "## 3. Research Problem and Goal",
        "## 4. Task Definition",
        "## 5. Input and Output Specification",
        "## 6. Baseline Template Requirement",
        "## 7. Model Requirements",
        "## 8. Loss Function Requirements",
        "## 9. Dataset Requirements",
        "## 10. Training Requirements",
        "## 11. Evaluation Metrics",
        "## 12. Hyperparameter Search Space",
        "## 13. Ablation Study Design",
        "## 14. Generated Project Requirements",
        "## 15. Validation Criteria",
        "## 16. Interface with Existing Auto-Training Module",
        "## 17. Risks and Manual Confirmation Items",
        "## 18. Summary for Next Stage",
    ]
    for heading in headings:
        assert heading in markdown
