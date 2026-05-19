"""Tests for task-card search space validation and sampling."""

from __future__ import annotations

from auto_research.search_space.base import (
    SearchSpaceDefinition,
    hash_search_space,
    sample_from_search_space,
    validate_search_space,
)


class _TrialStub:
    def suggest_float(self, name: str, low: float, high: float, *, log: bool = False) -> float:
        assert isinstance(name, str)
        assert low < high
        assert isinstance(log, bool)
        return low if not log else high

    def suggest_int(self, name: str, low: int, high: int, *, step: int = 1) -> int:
        assert isinstance(name, str)
        assert low <= high
        assert step > 0
        return low + step - 1 if low + step - 1 <= high else low

    def suggest_categorical(self, name: str, choices: list[object]) -> object:
        assert isinstance(name, str)
        return choices[0]


def test_validate_search_space_accepts_supported_types() -> None:
    search_space = {
        "lr": {"type": "float", "low": "1e-5", "high": "1e-3", "log": True},
        "weight_decay": {"type": "float", "low": 1e-6, "high": 1e-3, "log": True},
        "batch_size": {"type": "categorical", "choices": [32, 64]},
        "epochs": {"type": "int", "low": 5, "high": 20, "step": 5},
        "use_warmup": {"type": "bool"},
    }

    is_valid, message = validate_search_space(search_space)

    assert is_valid is True
    assert message == "Search space is valid."


def test_validate_search_space_rejects_bad_float_log_range() -> None:
    search_space = {
        "lr": {"type": "float", "low": 0.0, "high": 1e-3, "log": True},
    }

    is_valid, message = validate_search_space(search_space)

    assert is_valid is False
    assert "both low and high must be > 0" in message


def test_validate_search_space_rejects_invalid_categorical_choice_type() -> None:
    search_space = {
        "optimizer": {"type": "categorical", "choices": ["adam", {"name": "sgd"}]},
    }

    is_valid, message = validate_search_space(search_space)

    assert is_valid is False
    assert "must be a number, string, or boolean" in message


def test_sample_from_search_space_returns_sampled_config() -> None:
    search_space = {
        "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        "batch_size": {"type": "categorical", "choices": [32, 64]},
        "epochs": {"type": "int", "low": 5, "high": 20, "step": 5},
        "use_warmup": {"type": "bool"},
    }

    sampled = sample_from_search_space(_TrialStub(), search_space)

    assert sampled == {
        "lr": 1e-3,
        "batch_size": 32,
        "epochs": 9,
        "use_warmup": False,
    }


def test_hash_search_space_is_stable_for_equivalent_dict_order() -> None:
    left = {
        "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        "batch_size": {"type": "categorical", "choices": [32, 64]},
    }
    right = {
        "batch_size": {"choices": [32, 64], "type": "categorical"},
        "lr": {"high": 1e-3, "log": True, "low": 1e-5, "type": "float"},
    }

    assert hash_search_space(left) == hash_search_space(right)


def test_search_space_definition_wrapper_uses_helper_functions() -> None:
    definition = SearchSpaceDefinition(
        parameters={
            "epochs": {"type": "int", "low": 5, "high": 20},
        }
    )

    assert definition.validate() == (True, "Search space is valid.")
    assert definition.sample(_TrialStub()) == {"epochs": 5}
    assert isinstance(definition.hash(), str)
