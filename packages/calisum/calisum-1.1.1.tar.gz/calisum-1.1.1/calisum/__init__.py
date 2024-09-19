"""Caliap Activity Summarizer package."""

__app_name__ = "calisum"
__version__ = "1.1.1"

(
    SUCCESS,
    ERROR,
    SCRAPING_ERROR,
    PARSING_ERROR,
    SUMMARIZING_ERROR,
) = range(5)

ERROR_MESSAGES = {
    SUCCESS: "Success",
    ERROR: "Error",
    SCRAPING_ERROR: "Error while scraping",
    PARSING_ERROR: "Error while parsing",
    SUMMARIZING_ERROR: "Error while summarizing",
}