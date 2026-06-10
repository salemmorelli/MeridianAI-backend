# tests/test_catalog.py
from __future__ import annotations
import pytest
from catalog import load_catalog


class TestLoadCatalog:
    """Tests for the catalog data loading."""

    def test_catalog_loads_without_error(self):
        """Catalog should load without raising any exception."""
        catalog = load_catalog()
        assert catalog is not None

    def test_catalog_has_points_key(self):
        """Catalog must contain a points key."""
        catalog = load_catalog()
        assert "points" in catalog

    def test_catalog_points_is_list(self):
        """Points must be a list."""
        catalog = load_catalog()
        assert isinstance(catalog["points"], list)

    def test_catalog_has_at_least_one_point(self):
        """Catalog must have at least one acupressure point."""
        catalog = load_catalog()
        assert len(catalog["points"]) > 0

    def test_every_point_has_id(self):
        """Every point must have an id field."""
        for point in load_catalog()["points"]:
            assert "id" in point, f"Point missing id: {point}"

    def test_every_point_has_name(self):
        """Every point must have a name field."""
        for point in load_catalog()["points"]:
            assert "name" in point, f"Point missing name: {point}"

    def test_every_point_has_location(self):
        """Every point must have a location field."""
        for point in load_catalog()["points"]:
            assert "location" in point, f"Point missing location: {point}"

    def test_every_point_has_how_to(self):
        """Every point must have a howTo field."""
        for point in load_catalog()["points"]:
            assert "howTo" in point, f"Point missing howTo: {point}"

    def test_point_ids_are_unique(self):
        """All point IDs must be unique — no duplicates."""
        ids = [p["id"] for p in load_catalog()["points"]]
        assert len(ids) == len(set(ids)), "Duplicate point IDs found"

    def test_point_ids_are_strings(self):
        """All point IDs must be strings."""
        for point in load_catalog()["points"]:
            assert isinstance(point["id"], str), f"Non-string id: {point['id']}"

    def test_catalog_is_cached(self):
        """load_catalog should return the same object on repeated calls (lru_cache)."""
        catalog1 = load_catalog()
        catalog2 = load_catalog()
        assert catalog1 is catalog2