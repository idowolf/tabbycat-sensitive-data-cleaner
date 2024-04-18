# Tabbycat Admin Automation

This project automates several administrative tasks on a Tabbycat Django-admin interface using Selenium. The automation scripts provided handle tasks such as updating adjudicator scores, deleting adjudicator conflicts, and deactivating users.

## Setup and Configuration

Before running the automation scripts, you need to set up your environment and install the necessary dependencies.

### Dependencies

- Python 3.6 or higher
- Selenium WebDriver
- ChromeDriver (or any compatible driver for your browser)

You can install the required Python packages using pip:

```bash
pip install selenium
```

### Environment Variables

You need to set the following environment variables before running the scripts:

- `TABBYCAT_URL`: The base URL of your Tabbycat site (e.g., `https://example.com/`).
- `TABBYCAT_ADMIN_USERNAME`: Your admin username for logging into the Django-admin dashboard.
- `TABBYCAT_ADMIN_PASSWORD`: Your admin password for logging into the Django-admin dashboard.

You can set these variables in your environment like this:

#### On Linux/Mac:

```bash
export TABBYCAT_URL='https://example.com/'
export TABBYCAT_ADMIN_USERNAME='your_username'
export TABBYCAT_ADMIN_PASSWORD='your_password'
```

#### On Windows:

```bash
set TABBYCAT_URL=https://example.com/
set TABBYCAT_ADMIN_USERNAME=your_username
set TABBYCAT_ADMIN_PASSWORD=your_password
```

### Running the Script

Once you have set up the environment variables and installed the dependencies, you can run the scripts from your command line:

```bash
python main.py
```

## Features

The automation scripts include functions to:

- Update adjudicator base scores to 10 unless they are already set to 10.
- Delete all adjudicator feedbacks.
- Delete all preformed panels.
- Delete all base score histories.
- Delete all adjudicator-adjudicator and adjudicator-team conflicts.
- Deactivate all users except the administrator currently logged in.

## Contributions

Contributions to this project are welcome. Please ensure that you test the scripts in a safe environment before pushing changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
