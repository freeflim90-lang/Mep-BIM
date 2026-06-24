"""Starter Plan 레퍼런스 카드 언어별 라우팅 회귀 테스트.

배경(2026-06-24): 카드 PDF가 전 언어 영어 단일본이라 ko/ja/zh 구독자가
영어 카드를 받던 공백을 해소. 발송기(send_starter·send_daily)에 get_card_path()를
추가해 reference_cards/<lang>/ 우선 → 영어 폴백으로 라우팅한다.
이 테스트는 그 라우팅과 _lang_fallbacks 폴백 순서가 깨지지 않도록 고정한다.
"""

import importlib

import pytest

send_starter = importlib.import_module("scripts.bim_education.send_starter")
send_daily = importlib.import_module("scripts.bim_education.send_daily")

SENDERS = [send_starter, send_daily]
SAMPLE_CARD = "card_01_roles_lod.pdf"


@pytest.mark.parametrize("mod", SENDERS)
def test_lang_fallbacks_order(mod):
    # 비영어는 [자기언어, en], 영어는 [en] 만.
    assert mod._lang_fallbacks("ko") == ["ko", "en"]
    assert mod._lang_fallbacks("ja") == ["ja", "en"]
    assert mod._lang_fallbacks("en") == ["en"]


@pytest.mark.parametrize("mod", SENDERS)
@pytest.mark.parametrize("lang", ["ko", "ja", "zh"])
def test_localized_card_when_present(mod, lang):
    # 현지화 PDF가 실제로 존재하면 그 경로를 돌려준다.
    localized = mod.STARTER_CARDS_DIR / lang / SAMPLE_CARD
    if not localized.exists():
        pytest.skip(f"{lang} 카드 미생성 — make starter-localize 필요")
    path = mod.get_card_path(SAMPLE_CARD, lang)
    assert path == localized
    assert path.exists()


@pytest.mark.parametrize("mod", SENDERS)
def test_english_and_unknown_fall_back_to_root(mod):
    # 영어/미지원 언어(ar 등)는 reference_cards 루트의 영어 원본으로 폴백.
    root = mod.STARTER_CARDS_DIR / SAMPLE_CARD
    assert mod.get_card_path(SAMPLE_CARD, "en") == root
    assert mod.get_card_path(SAMPLE_CARD, "ar") == root  # ar 카드는 미지원(RTL)


@pytest.mark.parametrize("mod", SENDERS)
def test_card_path_never_returns_missing_for_known_days(mod):
    # REFERENCE_CARDS에 등록된 모든 카드는 최소한 영어 원본이 존재해야 한다.
    for _day, (_num, filename, _title) in mod.REFERENCE_CARDS.items():
        assert mod.get_card_path(filename, "en").exists(), filename
