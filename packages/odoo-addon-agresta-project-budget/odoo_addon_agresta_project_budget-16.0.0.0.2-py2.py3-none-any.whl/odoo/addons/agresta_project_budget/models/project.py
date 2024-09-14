# Copyright 2024 - Coopdevs - Quim Rebull
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError
import datetime
import logging

_logger = logging.getLogger(__name__)

class Project(models.Model):

    _inherit = "project.project"

    execution_weight = fields.Selection([('budget',"Based on phase budget [new field on task]"),
                                       ('hours',"Based on calculated hours"),
                                       ("none","No autocalculation")
                                       ],
                                       string='How should we weight each task?',
                                       default='none'
                                       )

    def project_recalculate_execution(self,date):
        for project in self:
            if project.execution_weight == 'none':
                next

            executed=0
            total=0
            for task in project.task_ids:
                _logger.debug("Last update project weight type -%s- ",  project.execution_weight)
                if project.execution_weight == 'budget':
                    total=total + task.budget_amount
                    _logger.debug("Last update date %s ",  date)
                    last_update= task.task_update_ids.filtered(lambda l: l.date <= date).sorted(lambda m: m.date,reverse=True)
                    if last_update :
                        _logger.debug("Last update for task executed pcnt %s - %s", last_update.execution_pcnt, date)

                        executed = executed + (task.budget_amount*last_update.execution_pcnt/100)
                elif project.execution_weight == 'hours':
                    total=total+task.planned_hours
                    executed= executed + task.effective_hours
                _logger.debug("Last update for task executed %s - total %s", executed, total)
            if total>0:
                project_total_pcnt= 100*executed/total
            else:
                project_total_pcnt=0
            if project.update_ids or project_total_pcnt>0:
                existing_update= self.env['project.update'].search([('project_id','=',project.id),('date','=',date),('auto','=',True) ])
                if existing_update:
                    existing_update.write({
                        'progress': project_total_pcnt,
                        'progress_percentage': project_total_pcnt,

                        })
                else: 
                    self.env['project.update'].create({
                        "status": 'on_track',
                        'project_id': project.id,
                        'name': f'Authomatic update for {date:%d/%m/%Y}',
                        'auto': True,
                        'progress': project_total_pcnt,
                        'progress_percentage': project_total_pcnt,
                        'date':date
                        })

    @api.model
    def recalc_execution_active_projects(self):
        projects= self.env['project.project'].search([])
        last_month_date = datetime.date.today().replace(day=1) - datetime.timedelta(days=1)  

        for project in projects:
            project.project_recalculate_execution(last_month_date)