"""Test suite untuk modul questionnaire.py."""
import pandas as pd
import pytest
from src.questionnaire import compute_cronbach_alpha, analyze_questionnaire


def test_cronbach_alpha():
    df = pd.DataFrame({
        "item1": [4, 5, 3, 4, 5],
        "item2": [4, 4, 3, 5, 4],
        "item3": [5, 5, 4, 4, 5],
    })
    alpha = compute_cronbach_alpha(df)
    assert 0.0 <= alpha <= 1.0


def test_analyze_questionnaire():
    df = pd.DataFrame({
        "JAR_1": [4, 5, 3, 4, 5],
        "JAR_2": [4, 4, 3, 5, 4],
        "JAR_3": [5, 5, 4, 4, 5],
        "ADM_1": [2, 3, 2, 3, 2],
        "ADM_2": [2, 2, 3, 2, 2],
        "ADM_3": [3, 3, 2, 3, 3],
        "SUP_1": [4, 4, 4, 3, 4],
        "SUP_2": [3, 4, 3, 4, 3],
        "SUP_3": [4, 3, 4, 4, 4],
    })
    res = analyze_questionnaire(df)
    assert "minat_jaringan" in res
    assert "cronbach_alpha" in res["minat_jaringan"]
