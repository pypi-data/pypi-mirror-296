# See README.rst file on addon root folder for license details

from odoo import api, fields, models


class ProjectRecalculateWizard(models.TransientModel):
    _name = "project.recalculate.execution.wizard"
    _description = "Project recalculate execution wizard"

    project_ids = fields.Many2one(
        comodel_name="project.project", readonly=True, string="Projects"
    )
    date = fields.Date(string="Close Date")

    @api.model
    def default_get(self, fields_list):
        active_model = self._context.get('active_model', '')
        active_id = self._context.get('active_id', False)
        if active_model == 'project.collaborator':
            active_model = 'project.project'
            active_id = self._context.get('default_project_id', False)
        result = super(ProjectRecalculateWizard, self.with_context(active_model=active_model, active_id=active_id)).default_get(fields)
        if not result.get('access_mode'):
            result.update(
                access_mode='read',
                display_access_mode=True,
            )
        return result



    def confirm_button(self):
        return self.project_ids.project_recalculate_execution(self.date)