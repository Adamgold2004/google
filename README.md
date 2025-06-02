# Simple Command-Line Applicant Tracking System (ATS)

This is a basic command-line application for managing job postings and applicant CVs.

## Features

*   Add new job postings (title and description).
*   View a list of all job postings.
*   Submit an applicant's CV (plain text file) for a specific job.
    *   The system attempts to parse the applicant's name from the CV filename.
    *   It extracts email and phone number from the CV content using regular expressions.
*   View a list of all applicants, including their extracted details and the job they applied for.
*   Data is stored in memory and is not persisted between sessions in this version.

## How to Run

1.  Ensure you have Python 3 installed.
2.  Save the `ats.py` script to your local machine.
3.  Open a terminal or command prompt.
4.  Navigate to the directory where you saved `ats.py`.
5.  Run the script using the command:
    ```bash
    python ats.py
    ```
6.  Follow the on-screen menu prompts to use the application.

## CV Parsing Notes

*   **CV Format:** Expects plain text (`.txt`) files for CVs.
*   **Name Parsing:** The applicant's name is derived from the CV filename (e.g., `john_doe_cv.txt` becomes "John Doe Cv").
*   **Email and Phone Extraction:** Uses basic regular expressions. It will find the first occurrence of an email and a common phone number pattern. More complex CV structures or formats might not be parsed correctly.
