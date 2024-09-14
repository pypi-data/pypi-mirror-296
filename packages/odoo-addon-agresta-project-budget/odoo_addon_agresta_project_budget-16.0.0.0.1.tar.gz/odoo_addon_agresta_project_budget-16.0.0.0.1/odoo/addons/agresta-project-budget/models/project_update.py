# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class ProjectUpdate(models.Model):

    _inherit = "project.update"

    auto= fields.Boolean("Is authomatic",default=False)
    

