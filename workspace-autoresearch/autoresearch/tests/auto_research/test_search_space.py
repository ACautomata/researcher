"""Focused tests for search-space parsing and sampling."""

from __future__ import annotations

from auto_research.search_space.base import (
    hash_search_space,
    sample_from_search_space,
    validate_search_space,
)


class _TrialStub:
    def suggest_float(self, name: str, low: float, high: float, *, log: bool = False) -> float:
        assert isinstance(name, str)
        assert low < high
        return high if log else low

    def suggest_int(self, name: str, low: int, high: int, *, step: int = 1) -> int:
        assert isinstance(name, str)
        assert low <= high
        assert step > 0
        return low

    def suggest_categorical(self, name: str, choices: list[object]) -> object:
        assert isinstance(name, str)
        return choices[-1]


def test_validate_search_space_accepts_supported_types() -> None:
    search_space = {
        "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        "epochs": {"type": "int", "low": 5, "high": 20, "step": 5},
        "batch_size": {"type": "categorical", "choices": [32, 64]},
        "use_warmup": {"type": "bool"},
    }

    assert validate_search_space(search_space) == (True, "Search space is valid.")


def test_sample_from_search_space_returns_trial_config() -> None:
    search_space = {
        "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        "epochs": {"type": "int", "low": 5, "high": 20},
        "batch_size": {"type": "categorical", "choices": [32, 64]},
        "use_warmup": {"type": "bool"},
    }

    sampled = sample_from_search_space(_TrialStub(), search_space)

    assert sampled == {
        "lr": 1e-3,
        "epochs": 5,
        "batch_size": 64,
        "use_warmup": True,
    }


def test_validate_search_space_rejects_invalid_categorical_choice() -> None:
    is_valid, message = validate_search_space(
        {
            "optimizer": {
                "type": "categorical",
                "choices": ["adam", {"name": "sgd"}],
            }
        }
    )

    assert is_valid is False
    assert "must be a number, string, or boolean" in message


def test_hash_search_space_is_stable_across_key_order() -> None:
    left = {
        "lr": {"type": "float", "low": 1e-5, "high": 1e-3, "log": True},
        "batch_size": {"type": "categorical", "choices": [32, 64]},
    }
    right = {
        "batch_size": {"choices": [32, 64], "type": "categorical"},
        "lr": {"high": 1e-3, "log": True, "low": 1e-5, "type": "float"},
    }

    assert hash_search_space(left) == hash_search_space(right)
