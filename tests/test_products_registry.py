"""제품 레지스트리(config/products.json) 가드레일.

수익 제품 단일 인덱스가 구조적으로 일관되고, 가리키는 위치가 실재하며,
교육 플랜 id 가 product_knowledge_layers.json 과 맞는지 강제한다.
"""
from __future__ import annotations

import json

from backend.core.paths import CONFIG_DIR, PROJECT_ROOT

_PRODUCTS = json.loads((CONFIG_DIR / "products.json").read_text(encoding="utf-8"))
_PLANS = {
    p["id"]
    for p in json.loads((CONFIG_DIR / "product_knowledge_layers.json").read_text(encoding="utf-8"))["plans"]
}

_REQUIRED = {"id", "name", "type", "revenue_path", "status"}


def test_product_ids_unique():
    ids = [p["id"] for p in _PRODUCTS["products"]]
    assert len(ids) == len(set(ids)), f"중복 제품 id: {ids}"


def test_required_fields_and_revenue_path():
    paths = set(_PRODUCTS["revenue_paths"])
    for p in _PRODUCTS["products"]:
        assert _REQUIRED <= set(p), f"필수 필드 누락: {p.get('id')}"
        assert p["revenue_path"] in paths, f"알 수 없는 revenue_path: {p['revenue_path']} ({p['id']})"


def test_knowledge_plan_refs_exist():
    for p in _PRODUCTS["products"]:
        plan = p.get("knowledge_plan")
        if plan is not None:
            assert plan in _PLANS, f"미존재 교육 플랜 참조: {plan} ({p['id']})"


def test_referenced_dirs_exist():
    for p in _PRODUCTS["products"]:
        for key in ("products_dir", "docs_dir", "commercial_dir", "store_docs_dir", "obsidian_vault"):
            rel = p.get(key)
            if rel:
                assert (PROJECT_ROOT / rel).is_dir(), f"{key} 경로 없음: {rel} ({p['id']})"
