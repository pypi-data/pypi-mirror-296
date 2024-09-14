# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

class Task_update(models.Model):

    _name="project.task.update"

    task_id = fields.Many2one(
        comodel_name="project.task", 
        string="Task", 
        ondelete="cascade",
    )
    date = fields.Date(
        string="Date", 
        required=True,
        default=lambda self: fields.Date.today()
    )
    execution_pcnt = fields.Float(
       string="Execution percent",
       help="Execution percent of the task",       
    ) 
    description = fields.Char(
       string="Description"
    ) 

