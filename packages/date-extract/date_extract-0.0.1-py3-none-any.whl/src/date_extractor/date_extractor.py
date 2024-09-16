import spacy
from typing import Optional, Union, TypedDict
from datetime import datetime, timedelta
import re

class ExtractedInfo(TypedDict):
    date: Optional[str]
    time: Optional[str]

class DateExtractor:
    def __init__(self):
        # Load the small English model
        self.nlp = spacy.load("en_core_web_sm")
        # Common keywords that suggest a date change
        self.relative_date_patterns = {
            "today": 0,
            "tomorrow": 1,
            "yesterday": -1,
            "next week": 7,
            "next month": 30,
        }

    def check_for_date_suggestion(self, message: str) -> bool:
        """
        Analyzes a message to determine if it likely contains a new date suggestion.
        Returns True if a suggestion is likely, False otherwise.
        """
        # Process the message using spaCy
        doc = self.nlp(message.lower())

        # Look for date-related entities
        date_entities = [ent for ent in doc.ents if ent.label_ in {"DATE", "TIME"}]

        # Check if the message contains any keywords suggesting a date change
        keyword_present = any(keyword in message.lower() for keyword in self.relative_date_patterns)

        # Return True if there are date entities or keywords suggesting a new date
        if date_entities or keyword_present:
            return True
        return False

    def adjust_date(self, message: str, original_date: Union[str, None] = None, original_time: Union[str, None] = None) -> ExtractedInfo:
        """
        Attempts to extract a date and time from the message, and adjust it according to the original date/time
        Uses original_date and original_time to resolve relative date expressions.

        Parameters:
        - message (str): The chat message to analyze.
        - original_date (str): A reference date in 'YYYY-mm-dd' format. Can be None.
        - original_time (str): A reference time in 'hh:mm:ss' format. Can be None.

        Returns:
        - extracted_info (dict): Contains extracted 'date' and 'time' strings.
        """
        # Initialize extracted information
        extracted_info: ExtractedInfo = {"date": None, "time": None}

        # Parse the original date and time, if provided
        reference_date = datetime.strptime(original_date, '%Y-%m-%d') if original_date else datetime.now()
        reference_time = datetime.strptime(original_time, '%H:%M:%S').time() if original_time else None

        # Process the message using spaCy
        doc = self.nlp(message.lower())

        # Extract date and time entities
        for ent in doc.ents:
            if ent.label_ == "DATE":
                date_text = ent.text.lower()
                # Check for relative date keywords
                if date_text in self.relative_date_patterns:
                    days_offset = self.relative_date_patterns[date_text]
                    resolved_date = reference_date + timedelta(days=days_offset)
                    extracted_info["date"] = resolved_date.strftime('%Y-%m-%d')
                else:
                    # Use a simple regex to find specific dates (e.g., "October 15th")
                    match = re.search(r'(\d{4}-\d{2}-\d{2})', date_text)
                    if match:
                        extracted_info["date"] = match.group(0)
            elif ent.label_ == "TIME":
                extracted_info["time"] = ent.text

        # If no specific date was extracted, use the reference date as a fallback
        if not extracted_info["date"]:
            extracted_info["date"] = reference_date.strftime('%Y-%m-%d')

        # If no specific time was extracted, use the reference time as a fallback
        if not extracted_info["time"] and reference_time:
            extracted_info["time"] = reference_time.strftime('%H:%M:%S')

        return extracted_info


# Example usage
if __name__ == "__main__":
    checker = DateExtractor()
    test_message = "How about tomorrow at 5 pm?"

    if checker.check_for_date_suggestion(test_message):
        print("This message likely contains a new date suggestion.")
        extracted_date = checker.extract_date(test_message, None, None)
        if extracted_date:
            print(f"Extracted date/time: {extracted_date}")
    else:
        print("No date suggestion found.")