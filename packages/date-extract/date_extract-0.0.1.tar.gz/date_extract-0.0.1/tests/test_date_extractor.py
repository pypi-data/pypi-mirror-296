import pytest
from src.date_extractor import DateExtractor


@pytest.fixture
def checker():
    # Initialize the DateSuggestionChecker
    return DateExtractor()


def test_check_for_date_suggestion_with_specific_date(checker):
    message = "Let's meet on October 15th."
    assert checker.check_for_date_suggestion(message) is True


def test_check_for_date_suggestion_with_relative_date(checker):
    message = "How about tomorrow?"
    assert checker.check_for_date_suggestion(message) is True


def test_check_for_date_suggestion_without_date(checker):
    message = "I don't think I can make it."
    assert checker.check_for_date_suggestion(message) is False


def test_check_for_date_suggestion_with_time(checker):
    message = "The meeting is scheduled for 3:00 PM."
    assert checker.check_for_date_suggestion(message) is True


def test_check_for_date_suggestion_with_keywords(checker):
    message = "Let's meet next week."
    assert checker.check_for_date_suggestion(message) is True

###
# NOT WORRYING ABOUT ADJUSTING DATES YET - JUST DEAL WITH DETECTING DATES FOR NOW
###

# def test_extract_date_with_specific_date(checker):
#     message = "Let's meet on October 15th."
#     extracted_date = checker.adjust_date(message, "2024-01-01", "08:15:00")
#     assert extracted_date["date"] is "2024-10-15"
#     assert extracted_date["time"] is "08:15:00"


# def test_extract_date_with_relative_date(checker):
#     message = "How about tomorrow at 5 pm?"
#     extracted_date = checker.adjust_date(message)
#     assert "tomorrow" in extracted_date
#     assert "5 pm" in extracted_date


# def test_extract_date_without_date(checker):
#     message = "I don't think I can make it."
#     extracted_date = checker.adjust_date(message)
#     assert extracted_date is None


# def test_extract_date_with_multiple_dates(checker):
#     message = "We can either meet on October 15th or next Friday."
#     extracted_date = checker.adjust_date(message)
#     assert "October 15th" in extracted_date
#     assert "next Friday" in extracted_date


def test_check_for_date_suggestion_with_noisy_text(checker):
    message = "I'm not sure, but how about meeting tomorrow, maybe?"
    assert checker.check_for_date_suggestion(message) is True


# def test_extract_date_with_noisy_text(checker):
#     message = "I'm not sure, but how about meeting tomorrow, maybe?"
#     extracted_date = checker.adjust_date(message)
#     assert "tomorrow" in extracted_date