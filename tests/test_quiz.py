import quiz_data


def test_quiz_scenarios_exist():
    assert len(quiz_data.SCENARIOS) >= 5


def test_quiz_scenarios_have_required_fields():
    for sc in quiz_data.SCENARIOS:
        assert sc.title
        assert sc.scenario_type
        assert sc.sender
        assert sc.message
        assert isinstance(sc.is_scam, bool)
        assert sc.difficulty in ("Beginner", "Intermediate", "Advanced", "Expert")
        assert sc.correct_explanation
        assert len(sc.tell_signs) >= 2
