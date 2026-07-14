from tplink.catalog import TAPO_DETECTIONS, catalog_rows


def test_catalog_rows_marks_supported_keys():
    rows = catalog_rows({"motion", "person"})
    by_key = {row["key"]: row for row in rows}
    assert by_key["motion"]["supported"] is True
    assert by_key["person"]["supported"] is True
    assert by_key["vehicle"]["supported"] is False


def test_catalog_rows_cover_all_definitions():
    rows = catalog_rows(set())
    assert len(rows) == len(TAPO_DETECTIONS)
    assert {row["key"] for row in rows} == {definition.key for definition in TAPO_DETECTIONS}


def test_catalog_rows_use_tplink_source_tag():
    rows = catalog_rows(set())
    assert all(row["source"] == "tp-link/onvif" for row in rows)
    assert all(row["raw_value"] is None for row in rows)
