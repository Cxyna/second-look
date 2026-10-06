import pytest

from ui.theme import THEMES, contrast, on_color


def test_contrast_known_values() -> None:
    assert contrast("#000000", "#ffffff") == pytest.approx(21)


@pytest.mark.parametrize("name", THEMES)
def test_primary_button_text_readable(name: str) -> None:
    iris = THEMES[name]["iris"]
    assert contrast(on_color(iris), iris) >= 4.5


@pytest.mark.parametrize("name", THEMES)
def test_button_and_pill_text_readable(name: str) -> None:
    t = THEMES[name]
    assert contrast(t["text"], t["overlay"]) >= 4.5


@pytest.mark.parametrize("name", THEMES)
def test_checkbox_radio_progress_fill_visible(name: str) -> None:
    # All three controls are filled with --accent (= iris) on the page background (base).
    t = THEMES[name]
    assert contrast(t["iris"], t["base"]) >= 3
