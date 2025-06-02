import re
import os

# Data structures for Job and Applicant

# A Job is represented as a dictionary with the following keys:
# - title: str, the title of the job
# - description: str, a description of the job
Job = {
    "title": "",
    "description": ""
}

# An Applicant is represented as a dictionary with the following keys:
# - name: str, the name of the applicant
# - email: str, the email address of the applicant
# - phone: str, the phone number of the applicant
# - applied_job_title: str, the title of the job the applicant applied for
Applicant = {
    "name": "",
    "email": "",
    "phone": "",
    "applied_job_title": ""
}

# Global lists to store Job and Applicant dictionaries
jobs = []  # List to store all available jobs
applicants = []  # List to store all applicants


def add_job(title: str, description: str):
    """
    Adds a new job to the jobs list.

    Args:
        title: The title of the job.
        description: A description of the job.
    """
    skills_input = input("Enter required skills (comma-separated, e.g., python,api,sql): ")
    if skills_input:
        required_skills = [skill.strip().lower() for skill in skills_input.split(',')]
    else:
        required_skills = []

    job = {
        "title": title,
        "description": description,
        "required_skills": required_skills
    }
    jobs.append(job)
    print(f"Job '{title}' added successfully.")


def view_jobs():
    """
    Prints all available jobs.

    If no jobs are available, it prints "No jobs available."
    Otherwise, it prints the title and description for each job.
    """
    if not jobs:
        print("No jobs available.")
    else:
        print("\nAvailable Jobs:")
        for job in jobs:
            print(f"Title: {job['title']}")
            print(f"Description: {job['description']}")
            skills_display = ", ".join(job['required_skills']) if job['required_skills'] else "None"
            print(f"Required Skills: {skills_display}")
            print("---")


def extract_keywords_from_cv(cv_text: str) -> list[str]:
    """
    Extracts unique keywords from a given text.

    Args:
        cv_text: The text content of the CV.

    Returns:
        A list of unique words (keywords) extracted from the text.
    """
    if not cv_text:
        return []
    words = re.split(r'\W+', cv_text.lower())
    # Filter out empty strings that can result from multiple delimiters
    keywords = [word for word in words if word]
    return list(set(keywords))


def parse_cv(cv_filepath: str, job_title: str):
    """
    Parses a CV file to extract applicant information and adds them to the applicants list.

    Args:
        cv_filepath: The path to the CV file.
        job_title: The title of the job the applicant is applying for.
    """
    try:
        # Extract Applicant Name
        filename = os.path.basename(cv_filepath)
        applicant_name_base = os.path.splitext(filename)[0]
        applicant_name = ' '.join(word.capitalize() for word in applicant_name_base.replace('_', ' ').replace('-', ' ').split())

        # Read CV Content
        with open(cv_filepath, 'r') as f:
            cv_content = f.read()

    except FileNotFoundError:
        print(f"Error: CV file '{cv_filepath}' not found.")
        return

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", cv_content)
    email = email_match.group(0) if email_match else "Not found"

    # Extract Phone Number
    phone_match = re.search(r"\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})", cv_content)
    phone = phone_match.group(0) if phone_match else "Not found"

    # Extract Email
    email_match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", cv_content)
    email = email_match.group(0) if email_match else "Not found"

    # Extract Phone Number
    phone_match = re.search(r"\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})", cv_content)
    phone = phone_match.group(0) if phone_match else "Not found"

    # Extract skills from CV content
    extracted_skills = extract_keywords_from_cv(cv_content)

    # Extract experience snippets
    experience_snippets = extract_experience(cv_content)

    # Create Applicant Dictionary
    applicant = {
        "name": applicant_name,
        "email": email,
        "phone": phone,
        "applied_job_title": job_title,
        "extracted_skills": extracted_skills,
        "experience_snippets": experience_snippets
    }

    # Add to Applicants List
    applicants.append(applicant)

    print(f"Applicant '{applicant_name}' processed for job '{job_title}'. Email: {email}, Phone: {phone}.")


def view_applicants():
    """
    Prints all processed applicants.

    If no applicants have been processed, it prints "No applicants processed yet."
    Otherwise, it prints the details for each applicant.
    """

    if not applicants:
        print("No applicants processed yet.")
    else:
        print("\nProcessed Applicants:")
        for applicant in applicants:
            print(f"Applicant: {applicant['name']}")
            print(f"Email: {applicant['email']}")
            print(f"Phone: {applicant['phone']}")
            print(f"Applied for: {applicant['applied_job_title']}")

            applicant_skills = applicant.get('extracted_skills', [])
            extracted_keywords_str = ", ".join(sorted(applicant_skills)) or "None" # Sort for consistent display
            print(f"Extracted Keywords: {extracted_keywords_str}")

            job_title_applied = applicant.get('applied_job_title')
            skill_match_info_str = "Skill Match: Not available (Job not found or no skills specified for job)"

            if job_title_applied:
                job_applied_for = None
                for j in jobs:  # Access global 'jobs' list
                    if j['title'] == job_title_applied:
                        job_applied_for = j
                        break

                if job_applied_for:
                    job_required_skills = job_applied_for.get('required_skills', [])
                    if job_required_skills:
                        match_results = match_skills(applicant_skills, job_required_skills)
                        score_percent = match_results['score'] * 100
                        matched_str = ", ".join(match_results['matched_skills']) or "None"
                        missing_str = ", ".join(match_results['missing_skills']) or "None"
                        skill_match_info_str = f"Skill Match Score: {score_percent:.2f}% | Matched: {matched_str} | Missing: {missing_str}"
                    else:
                        skill_match_info_str = "Skill Match Score: 100.00% (No specific skills required by job)"

            print(skill_match_info_str)

            experience_list = applicant.get('experience_snippets', [])
            if experience_list:
                print("Experience Snippets:")
                for snippet in experience_list:
                    print(f"  - {snippet}")
            else:
                print("Experience Snippets: None found")

            print("---")


def match_skills(applicant_skills: list[str], job_skills: list[str]) -> dict:
    """
    Compares applicant skills with job skills and calculates a match score.

    Args:
        applicant_skills: A list of skills extracted from the applicant's CV.
        job_skills: A list of required skills for the job.

    Returns:
        A dictionary containing:
            'score': Float, the match score (0.0 to 1.0).
            'matched_skills': List of skills present in both applicant and job requirements.
            'missing_skills': List of skills required by the job but missing from the applicant.
    """
    if not isinstance(applicant_skills, list) or not isinstance(job_skills, list):
        # Or raise an error, depending on desired strictness
        return {'score': 0.0, 'matched_skills': [], 'missing_skills': sorted(list(set(job_skills)))}

    set_applicant_skills = set(skill.lower() for skill in applicant_skills)
    set_job_skills = set(skill.lower() for skill in job_skills)

    if not set_job_skills:  # No skills required for the job
        return {'score': 1.0, 'matched_skills': [], 'missing_skills': []}

    matched_skills = list(set_applicant_skills & set_job_skills)
    missing_skills = list(set_job_skills - set_applicant_skills)

    score = len(matched_skills) / len(set_job_skills)

    return {
        'score': score,
        'matched_skills': sorted(matched_skills),
        'missing_skills': sorted(missing_skills)
    }


def extract_experience(cv_text: str) -> list[str]:
    """
    Extracts potential experience duration snippets from CV text.

    Args:
        cv_text: The text content of the CV.

    Returns:
        A list of unique experience-related snippets found in the text.
    """
    if not cv_text:
        return []

    found_experiences = []
    # Using corrected \b for word boundaries.
    # Pattern 4 is designed to capture only the "X years/yr" part as per findall behavior with one capture group.
    patterns = [
        r"\b\d+\s*(?:to|-)\s*\d+\s*years\b",         # e.g., "5 to 7 years", "5-7 years"
        r"\b\d+\+?\s*years(?: of experience)?\b",    # e.g., "5 years", "10+ years", "5 years of experience"
        r"\b\d+\s*yrs\b",                           # e.g., "3 yrs"
        r"(?:experience|exp)\s*[:\-]?\s*(\d+\s*years?)", # e.g., "Experience: 3 years" (captures "3 years")
    ]

    for p_str in patterns:
        try:
            matches = re.findall(p_str, cv_text, re.IGNORECASE)
            for match in matches:
                # If findall returns tuples (due to multiple capture groups in a pattern, though not the case here)
                # or a list of strings (if one capture group or no groups)
                if isinstance(match, tuple):
                    # This case would apply if a pattern had multiple capture groups, e.g., r"(\d+) to (\d+) years"
                    # For the current patterns, this branch is less likely to be hit for pattern 4 as it has one group.
                    # findall with one group returns a list of strings, not list of tuples.
                    found_experiences.append(" ".join(m for m in match if m).strip())
                else: # Match is a string (either full match or content of a single capture group)
                    found_experiences.append(match.strip())
        except re.error as e:
            # This should ideally not happen with pre-defined valid patterns
            print(f"Regex error with pattern '{p_str}': {e}")

    return list(set(found_experiences)) # Return unique snippets


def main():
    """Runs the main loop for the Simple Applicant Tracking System."""
    print("Simple Applicant Tracking System")

    while True:
        print("\nMenu:")
        print("1. Add Job")
        print("2. View Jobs")
        print("3. Add Applicant (Submit CV)")
        print("4. View Applicants")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            title = input("Enter job title: ")
            description = input("Enter job description: ")
            add_job(title, description)
        elif choice == '2':
            view_jobs()
        elif choice == '3':
            view_jobs()
            if not jobs:
                print("Please add a job first before adding an applicant.")
                print()
                continue
            cv_filepath = input("Enter path to CV file: ")
            job_title_applied = input("Enter the exact title of the job to apply for: ")

            job_exists = False
            for job in jobs:
                if job['title'] == job_title_applied:
                    job_exists = True
                    break

            if job_exists:
                parse_cv(cv_filepath, job_title_applied)
            else:
                print(f"Error: Job title '{job_title_applied}' not found. Please enter an existing job title.")
        elif choice == '4':
            view_applicants()
        elif choice == '5':
            print("Exiting application.")
            break
        else:
            print("Invalid choice. Please try again.")
        print()  # For better readability


if __name__ == "__main__":
    main()
