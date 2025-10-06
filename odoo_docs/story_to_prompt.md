As a Project Administrator,

I want to create and manage Developers as master data and assign Projects to the  Developer,

So that I can organize projects by developer, track ownership, and view all projects belonging to each developer.



# Acceptance Criteria
## Developer Entity (model: realestate.developer)
- A new entity Developers is created with its own menu under Projects.
- Developers have Tree View and Form View.
- Developers can be created, edited, archived/unarchived.
## Developer Profile (Form View) Fields
- name → Developer Name (Char, required).
- logo → Developer Logo (Binary, image).
- description → Description (Text/HTML).
- website → Website (Char, URL).
- email → Email (Char, email).
- phone → Phone Number (Char).
- street / city / country_id → Address fields.
- year_established → Year Established (Integer/Date).
- status → Status (Selection: Active/Inactive).
- notes → Internal Notes (Text).
- project_ids → Projects (One2many → realestate.project, field: developer_id).
## Developer Tree View (List View) Fields
* name (Developer Name).
* logo.
* phone.
* email.
* website.
* project_count (Computed Integer: number of related projects).
## Projects Integration (model: realestate.project)
- New field developer_id → Developer (Many2one → realestate.developer).
- The field is required when creating a project.
- Once the project is created, developer_id is readonly (uneditable).
- Clicking on Developer opens the Developer Profile.
## Developer → Projects Relationship
- Developer form view contains a Projects tab (One2many list of projects).
- Alternatively, add a smart button on Developer profile showing project count → clicking it opens the list of related projects.
## Technical Notes
* Models:
    * realestate.developer (new model).
    * realestate.project (existing, add field developer_id).
- Security: only Project Administrators can create/edit Developers.
- Views:
    - Menu: Projects → Developers.
    - Tree view, Form view, Search view.
    - Add Developer field to Project form & list view.