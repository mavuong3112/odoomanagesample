# -*- coding: utf-8 -*-
from odoo import api, fields, models, _


class Language(models.Model):
    _name = 'language.center.language'
    _description = 'Language'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char('Tên ngôn ngữ', required=True, tracking=True)
    code = fields.Char('Mã ngôn ngữ', required=True, tracking=True)
    description = fields.Text('Mô tả')
    course_ids = fields.One2many('language.center.course', 'language_id', string='Khóa học')
    active = fields.Boolean('Active', default=True)
    image = fields.Binary('Hình ảnh')
    
    _sql_constraints = [
        ('code_uniq', 'unique (code)', 'Mã ngôn ngữ phải là duy nhất!')
    ]
    
    def name_get(self):
        result = []
        for language in self:
            name = f"{language.name} [{language.code}]"
            result.append((language.id, name))
        return result
    
    @api.model
    def create(self, vals):
        # Convert code to uppercase
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super(Language, self).create(vals)
    
    def write(self, vals):
        # Convert code to uppercase
        if vals.get('code'):
            vals['code'] = vals['code'].upper()
        return super(Language, self).write(vals)
    
    def unlink(self):
        # Check if language is used in courses
        for language in self:
            if language.course_ids:
                raise models.ValidationError(_('Không thể xóa ngôn ngữ này vì đã có khóa học sử dụng!'))
        return super(Language, self).unlink()