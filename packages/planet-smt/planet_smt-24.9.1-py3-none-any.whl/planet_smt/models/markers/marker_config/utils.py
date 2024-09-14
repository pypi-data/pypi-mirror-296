"""Common utilities when resolving marker-configs."""

from datetime import date


def validate_start_and_end_date_consistency(start_date: str | date, end_date: str | date) -> None:
    """Validate that the end date is strictly greater than the start date."""

    if isinstance(start_date, str):
        start_date = date.fromisoformat(start_date)

    if isinstance(end_date, str):
        end_date = date.fromisoformat(end_date)

    if end_date <= start_date:
        raise ValueError("End date must be stricly greater than start date")
