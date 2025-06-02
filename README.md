# Simple Command-Line Applicant Tracking System (ATS)

This is a basic command-line application for managing job postings and applicant CVs.

## Features

*   Add new job postings (title, description, and comma-separated required skills).
*   View a list of all job postings, including their required skills.
*   Submit an applicant's CV (plain text file) for a specific job.
    *   The system attempts to parse the applicant's name from the CV filename.
    *   It extracts email and phone number from the CV content using regular expressions.
    *   Extracts unique words from the CV as 'keywords'.
    *   Attempts to extract snippets of text indicating years of experience using pattern matching.
*   View a list of all applicants, including their extracted details, CV keywords, skill match results against the job (score, matched/missing skills), and experience snippets.
*   Performs basic skills matching between applicant's CV keywords and job's required skills, providing a match score and identifying matched/missing skills.
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

## CV Analysis and Parsing Notes

*   **CV Format:** Expects plain text (`.txt`) files for CVs.
*   **Name Parsing:** The applicant's name is derived from the CV filename (e.g., `john_doe_cv.txt` becomes "John Doe Cv").
*   **Email and Phone Extraction:** Uses basic regular expressions. It will find the first occurrence of an email and a common phone number pattern. More complex CV structures or formats might not be parsed correctly.
*   **Keyword Extraction:** Unique words are extracted from the CV text by splitting the content by non-alphanumeric characters and converting to lowercase. These keywords form the basis for skill matching.
*   **Skill Matching:** Skill matching is based on comparing the unique words (keywords) extracted from the CV against the comma-separated 'required skills' defined for a job. A percentage score is calculated based on the number of matched skills relative to the total required skills.
*   **Experience Extraction:** Experience extraction uses a predefined set of regular expressions to find common phrases related to years of experience (e.g., "5 years", "3-5 yrs", "experience: 2 years"). It's a basic implementation and may not capture all variations or accurately interpret the context.
*   **Data Persistence:** All job and applicant data is stored in memory and will be lost when the application closes.
