# Odoo Development Documentation

## Table of Contents

1. [Shell Configuration](#shell-configuration)
2. [Dependency Check](#dependency-check)
3. [Testing and Reports](#testing-and-reports)
4. [Chrome Configuration](#chrome-configuration)
5. [Regular Expressions](#regular-expressions)
6. [Python Conventions](#python-conventions)
7. [Process Management](#process-management)
8. [Git Operations](#git-operations)
9. [Odoo Commands](#odoo-commands)
10. [View Development](#view-development)
11. [Field Types and Widgets](#field-types-and-widgets)
12. [Actions and Context](#actions-and-context)
13. [Chatter Integration](#chatter-integration)
14. [Smart Buttons](#smart-buttons)
15. [Compute Functions](#compute-functions)
16. [VS Code Debugger](#vs-code-debugger)
17. [Database Operations](#database-operations)
18. [Many2many Relationships](#many2many-relationships)

---

## Shell Configuration

### Git Branch in Prompt

```bash
parse_git_branch() {
    git branch 2>/dev/null | grep '^\*' | colrm 1 2
}

# Add branch info to your prompt
export PS1="$PS1[$(parse_git_branch)] "
```

---

## Dependency Check

### Odoo Analysis Commands

```bash
# Check dependencies with path
odoo_analyse --path /opt/odoo17/odoo17/epm-betaegypt/metrics_enterprise/ --show-dependency --skip-assets --skip-data --skip-language --skip-readme

# Check dependencies with config
odoo_analyse -c /etc/odoo_17_beta.conf --show-dependency --skip-all
```

---

## Testing and Reports

### Test Report Format

```python
'["/report/pdf/multi_product_select.tb_invoice/554704","qweb-pdf"]'
```

---

## Chrome Configuration

### Disable CORS

```bash
google-chrome --disable-web-security --user-data-dir="/tmp/chrome_dev"
```

---

## Regular Expressions

### Common Regex Patterns

```regex
# HTML anchor tags
\{\{<a.*?\}\}

# One2many field with domain
One2many\(['"]([\w.]+)['"].*?domain
```

**References:**
- [OpenAI Regex Chat](https://chat.openai.com/share/238ab334-2d67-445b-b477-d78c9a2347e5)

---

## Python Conventions

### Underscore Naming Conventions

- `_` leading method name: private, not imported when `from xxx import *`
- `__` leading method name: adds class name to it
  - Example: `play()` in class `football` becomes `_football__play()`

**References:**
- [Python Engineer - Underscore](https://www.python-engineer.com/posts/double-single-leading-underscore/)
- [TutorialsTeacher - Modifiers](https://www.tutorialsteacher.com/python/public-private-protected-modifiers)

---

## Process Management

### Kill Odoo Process

```bash
# Test SSH connection
ssh -T git@github.com

# Find Odoo processes
ps aux | grep odoo

# Kill processes
sudo kill 12345
sudo kill -9 118115
```

---

## Git Operations

### Submodules

#### Add Submodule

```bash
git submodule add --force -b 15.0 git@github.com:Metrics-eg/odoo-paymob.git metrics_enterprise/wt_payment_paymob

# Update submodules
git submodule update
```

#### Clone with Submodules

```bash
# Clone with submodules
git clone --recurse-submodules https://github.com/chaconinc/MainProject

# Or clone then initialize submodules
git submodule init
git submodule update
```

### Branch Management

```bash
# Delete remote branch
git push origin :branch_name

# Delete local branch
git branch -d branch_name

# List remote branches
git branch -r
```

### Git Ignore

```bash
# Ignore .pyc files
*.pyc

# Remove from repository but keep locally
git rm --cached '*.pyc'
```

---

## Odoo Commands

### Running Odoo

```bash
# Odoo 16
/opt/odoo16/odoo16-venv/bin/python3 /opt/odoo16/odoo16/odoo-bin -c /etc/odoo16.conf --dev all --log-level=debug --logfile= -d stage -u wallet

# Odoo 17
/opt/odoo17/beta_17_env/bin/python3 /opt/odoo17/odoo17/odoo-bin -c /etc/odoo_17_beta.conf --logfile= -d osama -p 8027

# Odoo 15
/opt/odoo15/beta_env/bin/python3 /opt/odoo15/odoo15/odoo-bin -c /etc/odoo_15_beta.conf --logfile= -d -p 8025
```

---

## View Development

### Domain Rules

> **Note:** Domain and other attributes must have `" "` except only in `<attribute>`

### Image Widget

```xml
<field name="image" string="Image" widget="image" options="{'size': [150, 150]}"/>
```

### Status Bar

```xml
<!-- Before sheet -->
<header>
    <field name="status" widget="statusbar" options="{'clickable':'1'}" nolabel='1'/>
</header>

<!-- Remove field -->
<field name="status"/>
```

### Editable Tree View

```xml
<tree string="invoice_product" editable='bottom'>
    <field name="invoice_id"/>
    <field name="product_id"/>
    <field name="price"/>
    <field name="count"/>
    <field name="total_price"/>
</tree>
```

---

## Field Types and Widgets

### Monetary Field

```python
# Model definition
currency_id = fields.Many2one('res.currency', string="Currency")
currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)
price = fields.Monetary(string='Price', required=True, currency_field='currency_id', tracking=True)
```

```xml
<!-- View definition -->
<field name="total_cheques_amount" widget="monetary"/>
```

---

## Actions and Context

### Using Context for Default Values

#### XML Action

```xml
<record id="create_quotation_action" model="ir.actions.act_window">
    <field name="name">Create Quotation</field>
    <field name="res_model">workshop.quotation</field>
    <field name="view_mode">form</field>
</record>

<header>
    <button string="Create Quotation" 
            name="%(automotive_workshop.create_quotation_action)d" 
            type="action" 
            context="{'default_inspection_order_id':active_id}" 
            view_mode="form"/>
</header>
```

#### Python Context

```python
def action_quotation_send(self, cr, uid, ids, context=None):
    # ...
    ctx.update({
        'default_model': 'sale.order',
        'default_res_id': ids[0],
        'default_use_template': bool(template_id),
        'default_template_id': template_id,
        'default_composition_mode': 'comment',
        'mark_so_as_sent': True
    })
    return {
        'type': 'ir.actions.act_window',
        'view_type': 'form',
        'view_mode': 'form',
        'res_model': 'mail.compose.message',
        'views': [(compose_form_id, 'form')],
        'view_id': compose_form_id,
        'target': 'new',
        'context': ctx,
    }
```

### Return View from Python

```python
def action_view_quotation(self):
    self.ensure_one()
    quotations = self.env['workshop.quotation'].search([
        ('inspection_order_id', '=', self.id)]).ids
    return {
        'name': _('Quotations'),
        'type': 'ir.actions.act_window',
        'view_mode': 'tree,form',
        'res_model': 'workshop.quotation',
        'domain': [('id', 'in', quotations)],
        'target': 'new'
    }

def action_create_quotation(self):
    self.ensure_one()
    return {
        'name': _('Quotation'),
        'type': 'ir.actions.act_window',
        'view_mode': 'form',
        'res_model': 'workshop.quotation',
        'context': {'default_inspection_order_id': self.id}
    }
```

### Hide Elements Based on Context

```xml
<button string="Create repair order" 
        invisible="context.get('hide_repair_order_button')" 
        name="%(automotive_workshop.create_repair_order_action)d" 
        type="action" 
        context="{'default_quotation_id':active_id}" 
        view_mode="form"/>
```

---

## Chatter Integration

### Model Configuration

```python
# In model
_inherit = ['mail.thread', 'mail.activity.mixin']
# Add tracking=True to fields
```

### View Configuration

```xml
<!-- In view after sheet -->
<!-- Chatter -->
<div class="oe_chatter">
    <field name="message_follower_ids" groups="base.group_user"/>
    <field name="activity_ids"/>
    <field name="message_ids"/>
</div>
```

---

## Smart Buttons

### Model Definition

```python
quotation_count = fields.Integer('Quotation Count', compute="_compute_quotation_count", default=0)

def _compute_quotation_count(self):
    for rec in self:
        rec.quotation_count = self.env['workshop.quotation'].search_count([
            ('inspection_order_id', '=', rec.id)
        ])

def action_view_quotation(self):
    self.ensure_one()
    quotations = self.env['workshop.quotation'].search([
        ('inspection_order_id', '=', self.id)]).ids
    return {
        'name': _('Quotations'),
        'type': 'ir.actions.act_window',
        'view_mode': 'tree,form',
        'res_model': 'workshop.quotation',
        'domain': [('id', 'in', quotations)],
    }
```

### View Definition

#### Odoo 15

```xml
<sheet>
    <div class="oe_button_box" name="button_box">
        <button name="action_view_quotation" 
                type="object" 
                class="oe_stat_button" 
                icon="fa-pencil-square-o" 
                attrs="{'invisible': [('quotation_count', '=', 0)]}">
            <field name="quotation_count" widget="statinfo" string="Quotations"/>
        </button>
    </div>
</sheet>
```

#### Odoo 17

```xml
<div class="oe_button_box" name="button_box">
    <button name="action_view_invoices" 
            type="object" 
            class="oe_stat_button" 
            icon="fa-pencil-square-o" 
            invisible="invoice_count == 0">
        <field name="invoice_count" widget="statinfo" string="Invoices"/>
    </button>
</div>
```

### Smart Button Without Count

```xml
<button name="action_open_original" 
        type="object" 
        class="oe_stat_button"
        icon="fa-pencil-square-o" 
        invisible="not original_structure_id">
    <div class="o_stat_info">
        <span class="o_stat_text">Original Structure</span>
    </div>
</button>
```

---

## Compute Functions

```python
car_id = fields.Many2one('workshop.car', string='Car', compute="_compute_car_id", tracking=True)

@api.depends('inspection_order_id')
def _compute_car_id(self):
    for rec in self:
        if rec.inspection_order_id:
            rec.car_id = rec.inspection_order_id.car_id
        else:
            rec.car_id = False
```

---

## VS Code Debugger

### Configuration

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Odoo",
            "type": "python",
            "request": "launch",
            "program": "/opt/odoo16/odoo16/odoo-bin",
            "pythonPath": "/opt/odoo16/odoo16-venv/bin/python3",
            "args": [
                "-c", "/etc/odoo16.conf",
                "--dev", "all",
                "--log-level=debug",
                "--logfile=",
                "-d", "stage",
                "-u", "wallet"
            ],
            "cwd": "${workspaceFolder}",
            "env": {},
            "envFile": "${workspaceFolder}/.env",
            "debugOptions": [
                "WaitOnAbnormalExit",
                "WaitOnNormalExit",
                "RedirectOutput"
            ]
        },
        {
            "name": "Python: Current File",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        }
    ]
}
```

### Ordering

```python
_order = 'sequence'
sequence = fields.Integer(string='Sequence', default=0)
```

---

## Database Operations

### PostgreSQL Commands

```sql
-- List all users
\du
```

---

## Many2many Relationships

### Basic Many2many with Attributes

```python
from odoo import models, fields

class Course(models.Model):
    _name = 'your_module.course'
    _description = 'Course Model'

    name = fields.Char(string='Course Name', required=True)
    students = fields.Many2many(
        'your_module.student',
        'course_student_rel',
        'course_id',
        'student_id',
        string='Students',
        relation='your_module.course_student_relation'
    )

class Student(models.Model):
    _name = 'your_module.student'
    _description = 'Student Model'

    name = fields.Char(string='Student Name', required=True)
    courses = fields.Many2many(
        'your_module.course',
        'course_student_rel',
        'student_id',
        'course_id',
        string='Courses',
        relation='your_module.course_student_relation'
    )

class CourseStudentRelation(models.Model):
    _name = 'your_module.course_student_relation'
    _description = 'Course-Student Relation'

    course_id = fields.Many2one('your_module.course', string='Course')
    student_id = fields.Many2one('your_module.student', string='Student')
    attendance = fields.Float(string='Attendance Percentage')
```

**Key Points:**
1. The `CourseStudentRelation` model represents the many-to-many relationship between `Course` and `Student`
2. This model contains an additional field called `attendance` to store the attendance percentage for each student in a course
3. In the `Course` and `Student` models, set the `relation` parameter in the `Many2many` field to specify the name of the model that defines the relationship

### Usage Example

```python
# Create a student
student = self.env['your_module.student'].create({'name': 'John Doe'})

# Create a course
course = self.env['your_module.course'].create({'name': 'Mathematics'})

# Add the student to the course with attendance information
course.students = [(4, student.id, {'attendance': 90.0})]

# Retrieve the attendance information for a student in a course
attendance_percentage = student.courses.filtered(lambda c: c.id == course.id).attendance
```

---

## Widgets and Special Fields

### Avatar Widget

```xml
<field name="user_id" widget="many2one_avatar_user"/>
```

### Search View Filters

```xml
<!-- Group by filter -->
<filter name="group_by_stage_id" string="stage_id" context="{'group_by': 'stage_id'}"/>

<!-- Default search filter -->
<field name="context">{'search_default_group_by_stage_id':1}</field>

<!-- User-specific filter -->
<filter name="filter_my_contracts" string="My Contracts" domain="[('user_id', '=', uid)]"/>
```

---

## Sequences

### Model Implementation

```python
contract_code = fields.Char(string='Contact Code', readonly=True)

@api.model
def create(self, vals):
    vals['contract_code'] = self.env['ir.sequence'].next_by_code('contract.contract')
    return super(ContractContract, self).create(vals)
```

### XML Configuration

```xml
<record id="contract_contract_seq" model="ir.sequence">
    <field name="name">Contract Sequence</field>
    <field name="code">contract.contract</field>
    <field name="prefix">CT</field>
    <field name="padding">5</field>
    <field name="company_id" eval="False"/>
</record>
```

---

## Default Values

### Simple Defaults

```python
booking_date = fields.Date('Booking Date', default=lambda self: fields.Date.today())
default_booking_date = fields.Date(default=lambda self: fields.Date.today() + timedelta(days=7))
```

### Complex Default Functions

```python
def _get_default_stage(self):
    default_stage_id = self.env['contract.stage'].search([], limit=1)
    return default_stage_id

stage_id = fields.Many2one('contract.stage', string='Stage', default=_get_default_stage)
```

---

## Advanced Search Views

```xml
<record id="view_account_move_filter" model="ir.ui.view">
    <field name="name">account.move.select</field>
    <field name="model">account.move</field>
    <field name="arch" type="xml">
        <search string="Search Move">
            <field name="name" string="Journal Entry" 
                   filter_domain="['|', '|', ('name', 'ilike', self), ('ref', 'ilike', self), ('partner_id', 'ilike', self)]"/>
            <field name="date"/>
            <field name="partner_id"/>
            <field name="journal_id"/>
            
            <!-- Filters -->
            <filter string="Unposted" name="unposted" domain="[('state', '=', 'draft')]"/>
            <filter string="Posted" name="posted" domain="[('state', '=', 'posted')]"/>
            <separator/>
            <filter string="Reversed" name="reversed" domain="[('payment_state', '=', 'reversed')]"/>
            
            <!-- Date filter -->
            <filter string="Date" name="date" date="date"/>
            
            <!-- Group by -->
            <group expand="0" string="Group By">
                <filter string="Partner" name="partner" domain="[]" context="{'group_by': 'partner_id'}"/>
                <filter string="Journal" name="journal" domain="[]" context="{'group_by': 'journal_id'}"/>
                <filter string="Status" name="status" domain="[]" context="{'group_by': 'state'}"/>
                <filter string="Date" name="by_date" domain="[]" context="{'group_by': 'date'}"/>
            </group>
        </search>
    </field>
</record>
```

---

## One2many Field Filtering

```python
step_ids = fields.One2many('contract.step', inverse_name="contract_id", string="Contract Step", store=True)
stage_step_ids = fields.One2many('contract.step', inverse_name="contract_id", string="Contract Step", compute="_compute_stage_steps_ids")

@api.depends('step_ids')
def _compute_stage_steps_ids(self):
    for rec in self:
        rec.stage_step_ids = rec.step_ids.filtered_domain([('stage_id', '=', rec.stage_id.id)])
```

---

## Error Handling and Notifications

### Exceptions

```python
from odoo.exceptions import ValidationError, UserError

# User error
raise UserError('Requests Created Successfully')

# Validation error
raise ValidationError(_("You can't associate a contract with an active related sale order."))
```

### Notifications

```python
def showwarning(self):
    return {
        'type': 'ir.actions.client',
        'tag': 'display_notification',
        'params': {
            'type': 'info',  # 'warning', 'success', 'info'
            'title': "Success",
            'message': _("Two-factor authentication disabled for the following user(s)"),
            'next': {'type': 'ir.actions.act_window_close'},
        }
    }
```

---

## API Constraints

```python
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class YourModel(models.Model):
    _name = 'your.model'

    field1 = fields.Char(string='Field 1')
    field2 = fields.Char(string='Field 2')

    @api.constrains('field1', 'field2')
    def _check_at_least_one_field_has_value(self):
        for record in self:
            if not (record.field1 or record.field2):
                raise ValidationError("At least one of Field 1 or Field 2 must have a value.")
```

---

## Form View Enhancements

### Title Section

```xml
<div class="oe_title">
    <h1>
        <field name="name" readonly="1"/>
    </h1>
</div>
```

### SQL Constraints

```python
_sql_constraints = [
    ('Unique_Contract_Partner', 'UNIQUE(contract_id,partner_id)', 
     'this partner already exists for this contract')
]
```

---

## Python Utilities

### Inline If Statement

```python
value_if_true if condition else value_if_false
```

### Complex Computed Fields

```python
@api.depends('stage_step_ids.step_status')
def _compute_stage_complete(self):
    self.stage_complete = True if len(self.stage_step_ids.filtered_domain([('step_status', '!=', 'accepted')])) == 0 else False

stage_complete = fields.Boolean('Stage Complete', compute="_compute_stage_complete", default=False)
```

---

## Scheduled Actions (Cron Jobs)

```xml
<record id="ir_cron_scheduler_recurring_action" model="ir.cron">
    <field name="name">Update Missing Duration</field>
    <field name="model_id" ref="model_contract_contract"/>
    <field name="state">code</field>
    <field name="code">model.comput_stage_missing()</field>
    <field name="interval_number">1</field>
    <field name="interval_type">days</field>
    <field name="numbercall">-1</field>
    <field name="doall">False</field>
    <field name="nextcall" eval="(DateTime.now().replace(hour=22,minute=1,second=0)).strftime('%Y-%m-%d %H:%M:%S')"/>
</record>
```

---

## Ribbon Widget

```xml
<!-- Basic ribbon -->
<widget name="web_ribbon" title="illegal" bg_color="bg-danger" 
        attrs="{'invisible': [('illegal', '=', False)]}"/>

<!-- Available colors -->
<!-- .bg-primary, .bg-secondary, .bg-success, .bg-danger, .bg-warning, .bg-info, .bg-light, .bg-dark -->

<!-- Advanced ribbon with tooltip -->
<widget name="web_ribbon" text="Invoicing App Legacy" bg_color="bg-info"
        attrs="{'invisible': [('payment_state', '!=', 'invoicing_legacy')]}"
        tooltip="This entry has been generated through the Invoicing app"/>
```

---

## Layout and Styling

### Group Width

```xml
<group style="width:30%">
    <!-- fields here -->
</group>
```

### Button States

```python
stage = fields.Selection([
    ('draft', 'Draft'),
    ('confirmed', 'Confirmed'),
    ('pending', 'Pending'),
    ('approved', 'Approved'),
], string='Stage', default='draft')

def confirm_payment_plan(self):
    for rec in self:
        rec.stage = 'confirmed'
```

```xml
<button name="confirm_payment_plan" type="object" string="Confirm"
        class="btn-secondary" attrs="{'invisible': [('stage', '!=', 'draft')]}"/>
<button name="generate_plan_requests" type="object" string="Generate Requests"
        class="btn-secondary" attrs="{'invisible': [('stage', '!=', 'confirmed')]}"/>
```

---

## Advanced Python Techniques

### Calling Specific Parent Methods

```python
from odoo import models, fields, api

class Base1(models.Model):
    _name = 'your_module.base1'

    def some_method(self):
        print("Base1 method")
        return True

class Base2(models.Model):
    _name = 'your_module.base2'

    def some_method(self):
        print("Base2 method")
        return True

class Derived(models.Model):
    _name = 'your_module.derived'
    _inherit = ['your_module.base1', 'your_module.base2']

    def call_base1_method(self):
        # Call the specific method of Base1 using the class name
        Base1.some_method(self)
```

---

## Tree View Decorations

```xml
<tree string="Approvals"
      decoration-success="state == 'Approved'"
      decoration-danger="state == 'Refused'"
      decoration-info="state == 'Submitted'"
      decoration-warning="state == 'Cancel'">
    <field name="priority" widget="priority"/>
    <field name="code"/>
    <field name="name"/>
    <field name="user_id"/>
    <field name="request_date"/>
    <field name="pic_id"/>
    <field name="deadline"/>
    <field name="state" widget="badge"
           decoration-success="state == 'Approved'"
           decoration-danger="state == 'Refused'"
           decoration-info="state == 'Submitted'"
           decoration-warning="state == 'Cancel'"/>
</tree>
```

---

## Dynamic Actions

```python
def create_action(self):
    ActWindow = self.env['ir.actions.act_window']
    view = self.env.ref('mail.email_compose_message_wizard_form')

    for template in self:
        button_name = _('Send Mail (%s)', template.name)
        action = ActWindow.create({
            'name': button_name,
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'context': "{'default_composition_mode': 'mass_mail', 'default_template_id' : %d, 'default_use_template': True}" % (template.id),
            'view_mode': 'form,tree',
            'view_id': view.id,
            'target': 'new',
            'binding_model_id': template.model_id.id,
        })
        template.write({'ref_ir_act_window': action.id})
    return True
```

---

## Database Backup

**Reference:** [Odoo Forum - Database Backup](https://www.odoo.com/ar/forum/lms-d-1/how-can-i-take-back-of-database-by-terminal-101505)

---

## Tree View Controls

```xml
<!-- Disable editing and creation -->
<tree edit="0" create="0">
    <!-- tree content -->
</tree>
```

---

## Kanban Views

### Advanced Kanban with Images and Progress

```xml
<field name="unit_ids" string="Units"
       domain="[('is_real_estate','=', True),('state','=','available')]">
    <kanban sample="1">
        <field name="id"/>
        <field name="product_variant_count"/>
        <field name="currency_id"/>
        <field name="activity_state"/>
        <progressbar field="activity_state"
                     colors="{&quot;planned&quot;: &quot;success&quot;, &quot;today&quot;: &quot;warning&quot;, &quot;overdue&quot;: &quot;danger&quot;}"/>
        <templates>
            <t t-name="kanban-box">
                <div class="oe_kanban_card oe_kanban_global_click">
                    <div class="o_kanban_image mr-1">
                        <img t-att-src="kanban_image('product.template', 'image_128', record.id.raw_value)"
                             alt="Product" class="o_image_64_contain"/>
                    </div>
                    <div class="oe_kanban_details">
                        <div class="o_kanban_record_top mb-0">
                            <div class="oe_kanban_top_right">
                                <strong class="o_kanban_record_title">
                                    <field name="name"/>
                                </strong>
                            </div>
                            <div class="oe_kanban_top_left">
                                <field name="state" widget="label_selection"
                                       options="{'classes': {'registered': 'default', 'available': 'primary','booked': 'warning','contracted':'success','delivered':'success'}}"/>
                            </div>
                        </div>
                        <div name="product_lst_price" class="mt-1">
                            Price: <field name="list_price" widget="monetary"
                                         options="{'currency_field': 'currency_id', 'field_digits': True}"/>
                        </div>
                    </div>
                </div>
            </t>
        </templates>
    </kanban>
</field>
```

---

## Date and Time Operations

### Date Manipulation

```python
from datetime import datetime, time

# End of day
end_of_the_day = datetime.combine(rec.day_date, datetime.max.time())

# Begin of day (commented examples)
# begin_of_the_day = rec.day_date.replace(hour=0, minute=0, second=0, microsecond=0).strftime('%Y-%m-%d %H:%M:%S')

# Combine date and time
date = datetime.now().date()
specific_time = time(hour=16)
datetime_obj = datetime.combine(date, specific_time)
print("Datetime from:", datetime_obj)
```

### Weekday Calculation

```python
import datetime

# Create a datetime object for a specific date
date = datetime.date(2024, 4, 1)
datet = datetime.datetime(2024, 4, 1)

# Get the day of the week (0 = Monday, 1 = Tuesday, ..., 6 = Sunday)
day_of_week = datet.weekday()

print(f"The day of the week for {date} is {day_of_week}.")
```

---

## Tree View Headers

> **Note:** Must select records to show header buttons

```xml
<record id="stock_valuation_layer_tree_inherit" model="ir.ui.view">
    <field name="name">stock.valuation.layer.tree.inherit</field>
    <field name="model">stock.valuation.layer</field>
    <field name="inherit_id" ref="stock_account.stock_valuation_layer_tree"/>
    <field name="arch" type="xml">
        <xpath expr="//tree[1]" position="inside">
            <header>
                <button string="compensate" name="compensate_selected" type="object"
                        class="oe_highlight"/>
            </header>
        </xpath>
    </field>
</record>
```

---

## Currency Fields

```python
company_id = fields.Many2one(
    'res.company', 'Company',
    default=lambda self: self.env.company, index=1)
currency_id = fields.Many2one(
    'res.currency', 'Currency',
    default=lambda self: self.env.company.currency_id)
```

---

## Wizard Forms

```xml
</sheet>
<footer>
    <button name="action_validate_revaluation" string="Revalue" type="object"
            class="btn-primary" data-hotkey="q"/>
    <button string="Cancel" class="btn-secondary" special="cancel" data-hotkey="z"/>
</footer>
```

---

## Odoo 17 Configuration

### VS Code Debug Configuration

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Odoo_beta_17",
            "type": "python",
            "request": "launch",
            "program": "/opt/odoo17/odoo17/odoo-bin",
            "python": "/opt/odoo17/beta_17_env/bin/python3",
            "args": [
                "-c", "/etc/odoo_17_beta.conf",
                "--dev", "all",
                "--log-level=debug",
                "--logfile=",
                "-d", "osama",
                "-u", "attendance_advanced"
            ],
            "console": "internalConsole",
            "redirectOutput": true,
            "cwd": "${workspaceFolder}",
            "env": {},
            "envFile": "${workspaceFolder}/.env"
        }
    ]
}
```

### Odoo 17 Configuration File

```ini
[options]
addons_path = /opt/odoo17/addons,/opt/odoo17/enterprise_addons,/opt/odoo17/mybroker_addons
admin_passwd = admin
csv_internal_sep = ,
data_dir = /home/shahin/.local/share/Odoo
db_host = False
db_name = 
db_password = False
db_port = False
db_sslmode = prefer
db_template = template0
db_user = False
dbfilter = 
demo = {}
email_from = False
from_filter = False
http_port = 8017
limit_memory_hard = 26843545600000
limit_memory_soft = 21474836480000
limit_request = 655360000
limit_time_cpu = 600000
limit_time_real = 120000
limit_time_real_cron = -1
proxy_mode = False
websocket_keep_alive_timeout = 360000
websocket_rate_limit_burst = 10
websocket_rate_limit_delay = 0.2
without_demo = False
workers = 0
x_sendfile = False
```

---

## Advanced Field Features

### Computed Fields with Onchange

> **Note:** You can make onchange on computed fields

### Readonly Fields with Group Exceptions

```xml
<field name="employee_id" readonly="1"/>
<field name="employee_id" groups="hr_payroll_community.group_hr_payroll_community_user"/>
```

### Instance Type Checking

```python
import datetime

attendance_date = attendance if isinstance(attendance, datetime.date) else attendance.check_in.date()
```

---

## View Inheritance and XPath

### Button Replacement

```xml
<xpath expr="//button[@name='%(hr_payroll_community.action_hr_payslip_by_employees)d']"
       position="before">
    <button string="Generate Payslips"
            name="%(action_hr_payslip_by_employees_with_exclusions)d" type="action"
            class="oe_highlight"/>
</xpath>
<xpath expr="//button[@name='%(hr_payroll_community.action_hr_payslip_by_employees)d']"
       position="attributes">
    <attribute name="invisible">1</attribute>
</xpath>
```

---

## Group-Based Visibility

```xml
<xpath expr="//widget[@name='hr_leave_stats']" position="before">
    <group string="Appears only to assistants" groups="time_off_assistant.group_hr_holidays_assistant">
        <field name="employee_id" 
               invisible="holiday_type != 'employee' or employee_id == False" 
               widget="many2one_avatar_employee" 
               domain="['|',('time_off_assistant_id', '=', uid),('user_id','=',uid)]"/>
        <field name="employee_ids"  
               invisible="holiday_type != 'employee' or (state == 'validate' and employee_id)" 
               readonly="state in ['cancel', 'refuse', 'validate', 'validate1']" 
               required="holiday_type == 'employee' and state in ('draft', 'cancel', 'refuse')" 
               widget="many2many_tags_avatar" 
               domain="['|',('time_off_assistant_id', '=', uid),('user_id','=',uid)]"/>
    </group>
</xpath>
```

---

## Computed Domains

### New Method (Odoo 17+)

```xml
<field name="parent_id" domain="[('id', 'in', context.get('task_ids', []))]"/>
```

### Old Method

```python
from odoo import models, fields, api

class YourModelName(models.Model):
    _name = 'your.model.name'

    field_to_compute_domain = fields.Many2one('related.model.name', 
                                              domain=lambda self: self._compute_field_domain())
    
    @api.model
    def _compute_field_domain(self):
        context = self.env.context
        some_value_from_context = context.get('some_key', 'default_value_if_not_present')
        domain = [('some_field', '=', some_value_from_context)]
        return domain
```

---

## Age Calculation

```python
from dateutil.relativedelta import relativedelta
from datetime import datetime

birthdate = fields.Date(string="Birthdate", required=True)
age_years = fields.Integer(string="Age (Years)", compute="_compute_age")
age_months = fields.Integer(string="Age (Months)", compute="_compute_age")
age_days = fields.Integer(string="Age (Days)", compute="_compute_age")

@api.depends('birthdate')
def _compute_age(self):
    today = datetime.now().date()
    for record in self:
        birthdate = record.birthdate
        age = relativedelta(today, birthdate)
        record.age_years = age.years
        record.age_months = age.months
        record.age_days = age.days
```

---

## Group Users Retrieval

```python
def get_all_sales_persons(self):
    group_id = self.env.ref('sales_team.group_sale_salesman').id
    # Retrieve the group record
    users = self.env['res.groups'].browse(group_id).users
```

**Reference:** [Python Expansion and Destruction](https://chat.openai.com/c/677856cf-2ba2-432f-a60e-72278f0a6958)

---

## JavaScript RPC Calls

```javascript
async onClickDownloadXSD() {
    await this.rpc("/web/dataset/call_kw/ir.attachment/action_download_xsd_files", {
        model: 'ir.attachment',
        method: 'action_download_xsd_files',
        args: [],
        kwargs: {}
    })
}
```

---

## Type Checking and Conversion

```python
if not (isinstance(res_model, int)): 
    res_model = res_model.id
if not (isinstance(res_id, int)): 
    res_id = res_id.id
```

**Reference:** [POST vs GET](https://chat.openai.com/share/b6547023-8dcc-4300-a46f-b5e979059a41)

---

## XPath Widget Modifications

```xml
<xpath expr="//field[@name='contract_partner_id_or_ids']" position="attributes">
    <attribute name="widget">many2many_tags</attribute>
</xpath>
```

---

## Search View Inheritance

```xml
<record id="cm_contract_view_search" model="ir.ui.view">
    <field name="name">cm.contract.view.search</field>
    <field name="model">cm.contract</field>
    <field name="inherit_id" ref="generic_contract.contract_contract_view_search"/>
    <field name="mode">primary</field>
    <field name="arch" type="xml">
        <search string="Contract">
            <field name="dependant_ids"/>
        </search>
    </field>
</record>
```

---

## Default Get Override

```python
class MyModel(models.Model):
    _name = 'my.model'

    def default_get(self, fields_list):
        defaults = super(MyModel, self).default_get(fields_list)
        if 'field1' in fields_list:
            defaults['field1'] = self.env.user.name  # Set default value based on current user
        if 'field2' in fields_list:
            defaults['field2'] = fields.Datetime.now()  # Set default value to current date and time
        return defaults
```

---

## Window Reload from Code

```python
return {
    'type': 'ir.actions.client',
    'tag': 'reload'
}
```

---

## Email Templates and Sending

### Email Template Definition

```xml
<record id="email_template_unit_booked_email_template" model="mail.template">
    <field name="name">Unit Booked Email Template To All Sales Persons</field>
    <field name="model_id" ref="real_estate_inventory.model_crm_lead"/>
    <field name="subject">Unit {{ object.proposed_unit.display_name }} is BOOKED</field>
    <field name="description">Sent to all sales persons when unit is booked</field>
    <field name="body_html" type="html">
        <div style="margin: 0; padding: 0; font-family: Arial, sans-serif; font-size: 14px; color: #333;">
            <p style="margin: 0; padding: 0;">
                Please note that unit
                <t t-if="object.proposed_unit">
                    <strong>
                        <t t-out="object.proposed_unit.display_name or ''"/>
                    </strong>
                </t>
                has been booked by
                <t t-if="object.user_id.name">
                    <strong>
                        <t t-out="object.user_id.name or ''"/>
                    </strong>
                </t>
            </p>
        </div>
    </field>
    <field name="lang">{{ object.partner_id.lang }}</field>
    <field name="auto_delete" eval="True"/>
</record>
```

### Send Email from Code

```python
def send_unit_booked_email_to_sales_persons(self):
    email_to = ','.join(self.get_emails_of_all_sales_persons())
    
    template_id = self.env.ref('real_estate_inventory.email_template_unit_booked_email_template')
    email_values = {"email_to": email_to}
    mail_id = template_id.send_mail(self.id, email_values=email_values)
    self.env['mail.mail'].browse(mail_id).send()
```

---

## One2many Field Operations

### Writing to One2many Fields

```python
def post_review_additional_fees(self, review):
    create_dict = {
        "move_id": self.invoice_id.id,
        "name": f"Additional Fees of {review.invoice_line_id.name}",
        "account_id": review.invoice_line_id.account_id.id,
        "analytic_account_id": review.invoice_line_id.analytic_account_id.id,
        "tax_ids": review.invoice_line_id.tax_ids.ids,
        "quantity": review.invoice_line_id.quantity,
        'price_unit': review.unit_added_value
    }
    self.invoice_id.with_context(check_move_validity=False).write({
        'invoice_line_ids': [[0, 0, create_dict]]
    })
```

---

## Tree View Headers with Buttons

```xml
<record id="cm_membership_view_tree" model="ir.ui.view">
    <field name="name">cm.membership.view.tree</field>
    <field name="model">cm.membership</field>
    <field name="arch" type="xml">
        <tree string="Membership" 
              decoration-success="membership_status == 'active'" 
              decoration-info="membership_status == 'pending'" 
              decoration-warning="is_suspended == True">
            <header>
                <button string="Activate" name="action_activate_membership" type="object" 
                        class="bg-success" 
                        attrs="{'invisible': ['|',('membership_status', 'not in', ('pending')),('is_suspended', '=', True)]}"/>
            </header>
            <field name="code"/>
            <field name="is_suspended" invisible="1"/>
            <field name="active" invisible="1"/>
            <field name="membership_type"/>
            <field name="dependant_type"/>
            <field name="partner_id"/>
            <field name="cm_contract_id"/>
            <field name="parent_membership_id"/>
            <field name="membership_status" widget="badge" 
                   decoration-success="membership_status == 'active'" 
                   decoration-info="membership_status == 'pending'" 
                   decoration-warning="is_suspended == True"/>
            <button string="Activate" name="action_activate_membership" type="object" 
                    class="bg-success" 
                    attrs="{'invisible': ['|',('membership_status', 'not in', ('pending')),('is_suspended', '=', True)]}"/>
        </tree>
    </field>
</record>
```

---

## Module Manifest Examples

### Basic Module

```python
{
    'name': 'OCA Bank Reconciliation Cosmetics',
    'version': '17.0.1.0.0',
    'description': 'Hide Any Menu Item User Wise, Hide Menu Items, Hide Menu',
    'category': 'Extra Tools',
    'author': 'Cybrosys Techno Solutions',
    'company': 'Cybrosys Techno Solutions',
    'maintainer': 'Cybrosys Techno Solutions',
    'website': "https://www.cybrosys.com",
    'depends': ['base'],
    'data': [
        'views/res_users.xml',
        'security/security.xml'
    ],
    'license': 'LGPL-3',
    'images': ['static/description/banner.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
}
```

### Advanced Payroll Module

```python
{
    'name': 'Payroll Advanced attendance calculation',
    'version': '1.0',
    'depends': ['hr_attendance', "hr_payroll_community", 'hr_holidays', 'hr_raw_zte_attendance'],
    'author': 'Metrics',
    'category': 'Uncategorized',
    'description': '''
    Integrating hr attendance with payroll to calculate:
    - missing check in/check out
    - late check in / checkout 
    - early check in / checkout
    - matching this with expected working days and hours
    ''',
    'data': [
        'security/ir.model.access.csv',
        'views/payslip.xml',
        'views/aa_payslip_exclusion_views.xml',
        'views/absent.xml',
    ],
    'demo': [],
}
```

---

## Field Options and Constraints

### No Create/Edit Options

```xml
<field name="spouse_id" 
       attrs="{'invisible': [('dependant_type', '=', 'child')],'required':[('dependant_type', '=', 'spouse')]}" 
       options="{'no_create': True, 'no_create_edit':True}"/>
```

### Computed Main Partner

```python
main_contract_partner = fields.Many2one('contract.partner', string='Main Partner', 
                                        compute="_compute_main_partner", store=True)

@api.depends('contract_partner_id_or_ids')
def _compute_main_partner(self):
    for rec in self:
        if rec.contract_partner_id_or_ids:
            rec.main_contract_partner = rec.contract_partner_id_or_ids[0].id
        else:
            rec.main_contract_partner = False
```

---

## Activity Creation

```python
self.env["mail.activity"].sudo().create({
    "activity_type_id": self.activity3.id,
    "note": "Partner activity 3.",
    "res_id": self.partner_client.id,
    "res_model_id": partner_model_id,
    "user_id": self.employee.id,
})
```

---

## One2many and Many2many Operations

### Command Operations

**References:**
- [Cybrosys - Special Command Operations](https://www.cybrosys.com/blog/what-are-the-special-command-operation-for-one2many-and-many2many-fields)
- [Cybrosys - Pass Values to Child Lines](https://www.cybrosys.com/blog/how-to-pass-values-to-the-child-lines-of-one2many-fields)

```python
# Command operations for One2many and Many2many fields:

# (0, 0, {values}) - link to a new record that needs to be created with the given values dictionary
# (1, ID, {values}) - update the linked record with id = ID (write values on it)
# (2, ID) - remove and delete the linked record with id = ID (calls unlink on ID)
# (3, ID) - cut the link to the linked record with id = ID (delete the relationship)
# (4, ID) - link to existing record with id = ID (adds a relationship)
# (5) - unlink all (like using (3,ID) for all linked records)
# (6, 0, [IDs]) - replace the list of linked IDs

# Example:
[(6, 0, [8, 5, 6, 4])]  # sets the many2many to ids [8, 5, 6, 4]
```

---

## Invoice Creation from Code

```python
def create_request_invoice(self):
    invoice = self.env['account.move'].create({
        'move_type': 'out_invoice',
        'partner_id': self.customer_id.id,
        'partner_shipping_id': self.customer_id.id,
        'booking_request_id': self.id,
        'invoice_date': datetime.now(),
        'invoice_line_ids': [(0, 0, {
            'product_id': self.unit_id.product_variant_id.id,
            'price_unit': 54545,
        })],
    })
```

---

## Reference Usage in Views

```xml
<button name="action_book_unit" string="Booked" type="object" 
        invisible="stage_id == %(stage_booked)d or is_won == True"/>
```

---

## XPath Replacements

```xml
<xpath expr="//button[@name='action_configure_bank_journal']" position="replace">
    <button name="%(account_reconcile_oca.action_bank_statement_line_reconcile_all)s" 
            type="action" class="btn btn-primary" groups="account.group_account_invoice">
        New Transaction
    </button>
</xpath>

<xpath expr="//t[@t-name='JournalBodyBankCash']//a[@name='action_new_transaction']" position="replace">
    <a role="menuitem" type="object" name="open_action_with_context" 
       context="{'action_name': 'action_bank_statement_tree', 'search_default_journal': True}">
        Statements
    </a>
</xpath>
```

---

## Action Window Views

```xml
<record id="crm_all_leads_action" model="ir.actions.act_window">
    <field name="name">All Leads</field>
    <field name="res_model">crm.lead</field>
    <field name="view_mode">tree,kanban,graph,pivot,calendar,form,activity</field>
    <field name="domain">['|',("active","=",True),("active","=",False)]</field>
    <field name="view_ids" eval="[Command.clear(),
        Command.create({'sequence': '1', 'view_mode': 'form', 'view_id': ref('real_estate_inventory.crm_sales_person_lead_view_form_inheritt')}),
        Command.create({'sequence': '0', 'view_mode': 'tree', 'view_id': ref('crm.crm_lead_view_list_activities')})]"/>
    <field name="search_view_id" ref="crm.view_crm_case_leads_filter"/>
    <field name="context">{}</field>
</record>
```

---

## Advanced Search Filters

### Date Filters

```xml
<filter string="Creation Date" name="creation_date" date="create_date"/>
```

### Advanced Time-based Filters

```xml
<filter name="today_activities" string="Today Activities" 
        domain="[('date', '&gt;=', (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d 00:00:00')), ('date', '&lt;=', (datetime.datetime.now()).strftime('%Y-%m-%d 23:59:59'))]"/>
<filter name="this_week_activities" string="This Week Activities" 
        domain="[('date', '&gt;=',(datetime.datetime.now() + relativedelta( days=-7,weekday=5)).strftime('%Y-%m-%d 00:00:00'))]"/>
```

---

## Configuration Settings

### XML Configuration

```xml
<record id="res_config_settings_view_form_inherit" model="ir.ui.view">
    <field name="name">res.config.settings.view.form.inherit</field>
    <field name="model">res.config.settings</field>
    <field name="inherit_id" ref="base.res_config_settings_view_form"/>
    <field name="arch" type="xml">
        <xpath expr="//form" position="inside">
            <app data-string="Real estate Inventory" string="Real estate Inventory" name="real_estate_inventory">
                <block title="Accounting">
                    <setting company_dependent="1" string="Booking Payment Journal" 
                             help="Payment method allowed for expenses paid by company.">
                        <field name="booking_request_payment_journal_id" 
                               placeholder="All payment methods allowed"/>
                    </setting>
                    <setting company_dependent="1" string="Booking Payment Method" 
                             help="Payment method allowed for expenses paid by company.">
                        <field name="booking_request_payment_method_id" 
                               placeholder="All payment methods allowed"/>
                    </setting>
                </block>
            </app>
        </xpath>
    </field>
</record>
```

### Python Configuration

```python
from odoo import fields, models

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    booking_request_invoicing_product_id = fields.Many2one(
        'product.template',
        string="Booking Request Invoicing Product", 
        config_parameter='booking_request_invoicing.booking_request_invoicing_product_id_param', 
        help='This is the product that is added to the invoice when you create booking request invoice'
    )
    
    # Get config parameter
    unit_change_approval_type_id = self.env['ir.config_parameter'].get_param('contract_management.unit_change_approval_type_id')
```

---

## Archived Records in One2many

```python
archived_plan_structure_approval_ids = fields.One2many(
    comodel_name='fa.multi_approval',
    inverse_name='plan_structure_id', 
    string='Archived Approvals',
    compute="_compute_archived_plan_structure_approval_ids",
    context={'active_test': False}
)
```

---

## Menu Configuration

```xml
<menuitem id="contract_menu" name="Contracts Configuration" parent="base.menu_custom" sequence="10"/>
<menuitem id="contract_reporting_menu" name="Reporting" parent="contract_menu" sequence="10"/>
```

---

## Field Attributes

### Readonly with Reference

```xml
<field name="partner_ids" readonly="stage_id == %(stage_booked)d"/>
```

### No Label (Odoo 17)

```xml
<field name="unit_expected_revenue_ids" 
       readonly="stage_id == %(stage_booked)d or is_won == True" 
       nolabel="1" colspan="2"/>
```

### XPath Attribute Modification

```xml
<xpath expr="//field[@name='partner_id']" position="attributes">
    <attribute name="readonly">stage_id == %(stage_booked)d or is_won == True</attribute>
</xpath>
```

---

## Update Methods

```python
def update_owners_when_customer_change(self, values):
    x = self.env.ref('real_estate_inventory.stage_booked')
    if (self.stage_id.id != self.env.ref('real_estate_inventory.stage_booked').id 
        and not(self.is_won) and 'owner_ids' not in values.keys()):
        
        if values.get('partner_id', False) and values['partner_id'] not in self.owner_ids.ids:
            self.owner_ids = self.owner_ids + self.env['res.partner'].browse(values['partner_id'])
        else:
            self.owner_ids = self.owner_ids + self.partner_id
```

---

## SMS Sending

```python
self.env['sms.sms'].create({
    'partner_id': my_otp.res_id,
    'number': my_otp.phone_number,
    'body': f"Your OTP for verification is: {my_otp.otp}"
})._send()
```

---

## Search Domain Reference

### Domain Operators

A domain is a list of criteria, each criterion being a triple `(field_name, operator, value)`:

- `=` - equals to
- `!=` - not equals to
- `>` - greater than
- `>=` - greater than or equal to
- `<` - less than
- `<=` - less than or equal to
- `=?` - unset or equals to
- `=like` - matches field_name against the value pattern
- `like` - matches field_name against the %value% pattern
- `not like` - doesn't match against the %value% pattern
- `ilike` - case insensitive like
- `not ilike` - case insensitive not like
- `=ilike` - case insensitive =like
- `in` - is equal to any of the items from value
- `not in` - is unequal to all of the items from value
- `child_of` - is a child (descendant) of a value record
- `parent_of` - is a parent (ascendant) of a value record
- `any` - matches if any record in the relationship satisfies the domain
- `not any` - matches if no record in the relationship satisfies the domain

### Logical Operators

- `'&'` - logical AND (default, arity 2)
- `'|'` - logical OR (arity 2)
- `'!'` - logical NOT (arity 1)

---

## Date Range Widget

```xml
<label for="date_from" string="Dates"/>
<div class="o_row">
    <field name="date_from" widget="date"/>
    <i class="fa fa-long-arrow-right" title="to"/>
    <field name="date_to" widget="date"/>
</div>
```

---

## Status Bar Visibility

```xml
<field name="state" widget="statusbar" statusbar_visible="draft,submitted,approved" 
       options="{'clickable':'1'}"/>
```

---

## Date Calculations

```python
from dateutil.relativedelta import relativedelta

def cron_separation_status(self):
    birthdate_of_25_years_old = fields.Date.today() - relativedelta(years=25)
    warning_date = birthdate_of_25_years_old + relativedelta(months=12 - self._separation_warning_month)
    
    records = self.search([
        ('membership_status', '=', 'active'),
        ('parent_membership_id', '!=', False),
        ('birthdate', '<=', warning_date)
    ])
    
    records._compute_separtion_status(birthdate_of_25_years_old, warning_date)

# First and last day of month
first_day = fields.Date.today().replace(day=1)
last_day = first_day + relativedelta(months=1) - relativedelta(days=1)
```

---

## Image Display in Templates

```xml
<!-- Base64 image -->
<img t-attf-src="data:image;base64,{{workflow.image}}" class="menu-img img-fluid"/>

<!-- Field widget -->
<field name="image" widget="image" class="rounded" options="{'size': [90, 90]}"/>

<!-- Kanban image -->
<img t-att-src="kanban_image('workflow.workflow', 'image', record.id.raw_value)" 
     class="w-100 rounded" alt="Icon"/>
```

---

## User and Group Creation

```xml
<record id="user_client_admin" model="res.users">
    <field name="name">Client Admin</field>
    <field name="login">client_admin</field>
    <field name="password">client_admin</field>
</record>

<record id="group_client_admin" model="res.groups">
    <field name="name">Client Admin Group</field>
    <field name="implied_ids" eval="[Command.link(ref('base.group_user'))]"/>
    <field name="users" eval="[(4, ref('workflow_users.user_client_admin'))]"/>
</record>
```

---

## Abstract Models

```python
from odoo import _, api, fields, models

class PaymentPlanPayment(models.AbstractModel):
    _name = 'finance.payment'
    _description = 'Payment plan payment'
    _order = 'sequence asc'

class PolicyBulkPayments(models.AbstractModel):
    _name = 'finance.payment_plan_structure_bulk_payments'
    _description = "Payment Plan Bulk Payments"
    _order = 'sequence asc'

class PaymentPlan(models.AbstractModel):
    _name = 'finance.payment_plan'
    _description = 'Real Estate Payment Plans'
```

---

## Kanban View Ribbon

```xml
<kanban string="Automation Rules" class="o_base_automation_kanban_view"
        records_draggable="false" groups_draggable="false"
        quick_create="false" group_create="false" 
        group_edit="false" group_delete="false">
    <templates>
        <t t-name="kanban-box">
            <div class="oe_kanban_global_click">
                <field name="active" invisible="1"/>
                <field name="model_name" invisible="1"/>
                <widget name="web_ribbon" title="Archived" bg_color="text-bg-danger" invisible="active"/>
                <div class="d-flex flex-column flex-md-row gap-3 flex-grow-1">
                    <!-- kanban content -->
                </div>
            </div>
        </t>
    </templates>
</kanban>
```

---

## Kanban View in Form View

```xml
<field name="contract_partner_ids" mode="kanban" readonly="1"/>
```

---

This comprehensive Odoo development documentation covers essential concepts, patterns, and examples for building robust Odoo applications. Each section provides practical code examples and explanations to help developers implement features effectively.

