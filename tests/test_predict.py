# tests/test_predict.py
from __future__ import annotations
import pytest
from unittest.mock import patch, MagicMock
from predict import (
    predict_best_point,
    ModelNotReadyError,
    POINT_DETAILS,
    DEFAULT_BY_SYMPTOM,
    DEFAULT_BY_REGION,
)


class TestPredictBestPoint:
    """Tests for the predict_best_point function."""

    def test_returns_dict_with_required_keys(self):
        """Every prediction must return all five required keys."""
        result = predict_best_point(
            symptom="headache", region="all", duration_minutes=2
        )
        assert isinstance(result, dict)
        for key in ["point_code", "who_point_code", "point_name",
                    "location", "technique"]:
            assert key in result, f"Missing key: {key}"

    def test_symptom_only_uses_keyword_lookup(self):
        """When region is 'all', should use DEFAULT_BY_SYMPTOM lookup."""
        # pick a symptom we know exists in the catalog
        if not DEFAULT_BY_SYMPTOM:
            pytest.skip("No symptoms in catalog")
        symptom = next(iter(DEFAULT_BY_SYMPTOM))
        result = predict_best_point(
            symptom=symptom, region="all", duration_minutes=1
        )
        assert result["point_code"] == DEFAULT_BY_SYMPTOM[symptom]

    def test_region_only_uses_region_lookup(self):
        """When symptom is 'all', should use DEFAULT_BY_REGION lookup."""
        if not DEFAULT_BY_REGION:
            pytest.skip("No regions in catalog")
        region = next(iter(DEFAULT_BY_REGION))
        result = predict_best_point(
            symptom="all", region=region, duration_minutes=1
        )
        assert result["point_code"] == DEFAULT_BY_REGION[region]

    def test_raises_value_error_when_both_all(self):
        """Should raise ValueError when both symptom and region are 'all'."""
        with pytest.raises(ValueError, match="at least one"):
            predict_best_point(symptom="all", region="all", duration_minutes=1)

    def test_input_normalisation_lowercase(self):
        """Uppercase input should produce same result as lowercase."""
        result_lower = predict_best_point(
            symptom="headache", region="all", duration_minutes=1
        )
        result_upper = predict_best_point(
            symptom="HEADACHE", region="all", duration_minutes=1
        )
        assert result_lower["point_code"] == result_upper["point_code"]

    def test_input_normalisation_whitespace(self):
        """Input with extra whitespace should produce same result."""
        result_clean = predict_best_point(
            symptom="headache", region="all", duration_minutes=1
        )
        result_spaces = predict_best_point(
            symptom="  headache  ", region="all", duration_minutes=1
        )
        assert result_clean["point_code"] == result_spaces["point_code"]

    def test_unknown_symptom_falls_back_to_li4(self):
        """Unknown symptom should fall back to LI4 default."""
        result = predict_best_point(
            symptom="zzz_unknown_symptom_xyz",
            region="all",
            duration_minutes=1
        )
        assert result["point_code"] == "LI4"

    def test_model_not_ready_error_when_model_missing(self):
        """Should raise ModelNotReadyError when model file does not exist."""
        with patch("predict.MODEL_PATH") as mock_path:
            mock_path.exists.return_value = False
            with pytest.raises(ModelNotReadyError):
                predict_best_point(
                    symptom="headache",
                    region="head",
                    duration_minutes=2
                )

    def test_duration_minutes_accepted_range(self):
        """Valid duration values 1-10 should all work without error."""
        for duration in [1, 5, 10]:
            result = predict_best_point(
                symptom="headache", region="all", duration_minutes=duration
            )
            assert "point_code" in result

    def test_point_details_populated(self):
        """POINT_DETAILS should have entries from catalog."""
        assert len(POINT_DETAILS) > 0

    def test_result_location_not_empty(self):
        """Location should never be empty for known points."""
        if not DEFAULT_BY_SYMPTOM:
            pytest.skip("No symptoms in catalog")
        symptom = next(iter(DEFAULT_BY_SYMPTOM))
        result = predict_best_point(
            symptom=symptom, region="all", duration_minutes=1
        )
        assert result["location"] != ""