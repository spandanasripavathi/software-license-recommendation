# Project Documentation

## Title
Software License Recommendation System

## Problem statement
Developers may not understand the permissions, restrictions and obligations attached to software licenses. This application helps compare four common licenses and provides an explainable rule-based recommendation.

## Objectives
1. Recommend a license using project requirements.
2. Explain MIT, GNU GPL, Apache 2.0 and BSD.
3. Compare copying, modification, distribution and commercial-use conditions.
4. Promote copyright awareness and respect for intellectual property.
5. Encourage ethical software development and notice preservation.

## Architecture
- Presentation layer: Jinja2 HTML templates, CSS, JavaScript and Bootstrap.
- Application layer: Flask routes and recommendation rules.
- Data layer: SQLite tables for license references, recommendation history and contact messages.

## Database tables
- `licenses`: license key, name and official reference URL.
- `recommendations`: project name, submitted answers, selected license, explanation, alternatives and date.
- `contact_messages`: sender name, email, message and date.

## Recommendation approach
The engine uses weighted rules rather than selecting a license from one answer. Copyleft preference strongly increases the GPL score. A request for an express patent grant strongly increases Apache 2.0. A permissive preference increases MIT, BSD and Apache. The system flags requirements that cannot be met by the four licenses, such as prohibiting commercial use or modification.

## Testing checklist
- Open each navigation link.
- Submit the recommendation form with all answers.
- Try submitting without a project name or a required answer.
- Test copyleft preference and patent-grant preference separately.
- Test a conflicting combination (copyleft + permissive).
- Confirm records appear in History and can be viewed/deleted.
- Submit the contact form and verify the success message.
- Resize the browser to mobile width and verify responsive navigation and tables.

## Limitations
This is a teaching prototype. License compatibility can depend on exact versions, project architecture, distribution method, dependencies and jurisdiction. The application does not replace legal review.
