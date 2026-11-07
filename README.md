# Software License Recommendation System

A B.Tech Computing Ethics project built with Python, Flask, SQLite, HTML, CSS, JavaScript and Bootstrap 5.

## Features
- Responsive home, about, license library, comparison and contact pages.
- License summaries for MIT, GNU GPL, Apache License 2.0 and BSD 3-Clause.
- Rule-based recommendation questionnaire with explanations and warnings for conflicting requirements.
- SQLite storage for recommendation history and contact messages.
- View and delete previous recommendations.

## Requirements
- Python 3.9 or newer
- Visual Studio Code (recommended)
- Internet connection for Bootstrap CDN assets (the Flask application itself runs locally)

## Run in VS Code (Windows)
1. Extract the ZIP file.
2. Open the `software-license-recommendation` folder in VS Code.
3. Open Terminal > New Terminal.
4. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

5. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use Command Prompt and run:

   ```cmd
   venv\Scripts\activate.bat
   ```

6. Install dependencies:

   ```powershell
   pip install -r requirements.txt
   ```

7. Start the application:

   ```powershell
   python app.py
   ```

8. Open this address in your browser:

   `http://127.0.0.1:5000`

The SQLite database is created automatically at `database/licenses.db` the first time the application starts.

## Project structure

```text
software-license-recommendation/
├── app.py
├── recommendation.py
├── database.py
├── requirements.txt
├── README.md
├── database/
│   └── licenses.db        # generated automatically
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── about.html
│   ├── licenses.html
│   ├── license_detail.html
│   ├── recommendation.html
│   ├── result.html
│   ├── comparison.html
│   ├── history.html
│   ├── contact.html
│   └── 404.html
└── static/
    ├── css/style.css
    └── js/script.js
```

## Recommendation logic notes
- GPL is prioritized when the developer asks for covered distributed derivatives to remain under the same license.
- Apache 2.0 is prioritized when an express contributor patent grant is requested.
- MIT and BSD are permissive options for projects that do not require copyleft.
- All four licenses permit commercial use, modification and redistribution subject to their terms. Therefore, selecting “No” for one of these permissions creates a warning: none of these four licenses meets that restriction.
- Attribution is not an optional switch. All four licenses require preservation of certain copyright/license notices, although the exact conditions differ.

This is an educational rule-based aid, not legal advice. The project does not perform a legal compatibility analysis of all dependencies or jurisdictions. Read the complete license texts before adopting a license.

## Official references
- MIT: https://opensource.org/license/mit
- GNU GPLv3: https://www.gnu.org/licenses/gpl-3.0.en.html
- Apache 2.0: https://www.apache.org/licenses/LICENSE-2.0
- BSD 3-Clause: https://opensource.org/license/bsd-3-clause

## Production note
Before deployment, set a strong random Flask `SECRET_KEY`, turn off Flask debug mode, add CSRF protection, and use a production WSGI server. The included contact form stores messages locally; it does not send email.
