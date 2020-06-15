from odoo import api, fields, models


class CreateProjectFromTmpl(models.TransientModel):
    _name = 'create.project.from.tmpl'

    task_date = fields.Date('Task Date')
    tmpl_proj_id = fields.Many2one('project.project', 'Proj Template')

    @api.model
    def default_get(self, fields):
        result = super(CreateProjectFromTmpl, self).default_get(fields)

        active_id = self._context.get('active_id')
        if active_id:
            result['tmpl_proj_id'] = active_id
        return result

    def create_proj(self):
        self.ensure_one()
        res = self.tmpl_proj_id.create_project_from_template()
        project_id  = res.get('res_id')
        project = self.env['project.project'].browse(project_id)
        for task in project.task_ids:
            task.write({'task_date': self.task_date})
        return res
