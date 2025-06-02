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
    job = {
        "title": title,
        "description": description
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
            print("---")


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

    # Create Applicant Dictionary
    applicant = {
        "name": applicant_name,
        "email": email,
        "phone": phone,
        "applied_job_title": job_title
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
            print("---")


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
