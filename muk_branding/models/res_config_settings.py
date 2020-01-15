###################################################################################
#
#    Copyright (c) 2017-2019 MuK IT GmbH.
#
#    This file is part of MuK Branding 
#    (see https://mukit.at).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program. If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

from odoo import api, fields, models

class ResConfigSettings(models.TransientModel):

    _inherit = 'res.config.settings'

    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    module_muk_web_branding = fields.Boolean(
        string="Web Branding",
        help="Customize the backend according to your needs.")
    
    module_muk_mail_branding = fields.Boolean(
        string="Mail Branding",
        help="Brand your outgoing mails with your own style.")
    
    module_muk_website_branding = fields.Boolean(
        string="Website Branding",
        help="Brand the website according to your needs.")
    
    module_muk_pos_branding = fields.Boolean(
        string="PoS Branding",
        help="Brand the PoS panel according to your needs.")
    
    branding_system_name = fields.Char(
        string='System Name')
    
    branding_publisher = fields.Char(
        string='Publisher')
    
    branding_website = fields.Char(
        string='Website URL')
    
    branding_documentation = fields.Char(
        string='Documentation URL')
    
    branding_support = fields.Char(
        string='Support URL')
    
    branding_store = fields.Char(
        string='Store URL')
    
    branding_share = fields.Char(
        string='Share URL')
    
    branding_company_name = fields.Char(
        string='Company Name',
        related='company_id.name',
        readonly=False)
    
    branding_company_logo = fields.Binary(
        string='Company Logo',
        related='company_id.logo',
        readonly=False)
    
    branding_company_favicon = fields.Binary(
        string='Company Favicon',
        related='company_id.favicon',
        readonly=False)
    
    #----------------------------------------------------------
    # Helper
    #----------------------------------------------------------
    
    @api.model
    def _delete_translations(self, value):
        self.env['ir.translation'].sudo().search([
            ('value', 'ilike', value)
        ]).unlink()
    
    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(params.get_branding_settings_params())
        return res
    
    @api.multi 
    def set_values(self):
        translation_changed = False
        res = super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        values = params.get_branding_settings_params()
        if self.branding_system_name != values.get('branding_system_name'):
            self._delete_translations(values.get('branding_system_name'))
            translation_changed = True
        if self.branding_publisher != values.get('branding_publisher'):
            self._delete_translations(values.get('branding_publisher'))
            translation_changed = True
        if self.branding_website != values.get('branding_website'):
            self._delete_translations(values.get('branding_website'))
            translation_changed = True
        if self.branding_documentation != values.get('branding_documentation'):
            self._delete_translations(values.get('branding_documentation'))
            translation_changed = True
        if self.branding_support != values.get('branding_support'):
            self._delete_translations(values.get('branding_support'))
            translation_changed = True
        if self.branding_store != values.get('branding_store'):
            self._delete_translations(values.get('branding_store'))
            translation_changed = True
        if self.branding_share != values.get('branding_share'):
            self._delete_translations(values.get('branding_share'))
            translation_changed = True
        if translation_changed:
            self.env['ir.config_parameter'].set_params({
                'muk_branding.system_name': self.branding_system_name or '',
                'muk_branding.publisher': self.branding_publisher or '',
                'muk_branding.website': self.branding_website or '',
                'muk_branding.documentation': self.branding_documentation or '',
                'muk_branding.support': self.branding_support or '',
                'muk_branding.store': self.branding_store or '',
                'muk_branding.share': self.branding_share or '',
            })
            self.translations_reload()
        return res
    
    def translations_reload(self):
        for lang in self.env['res.lang'].sudo().search([('active','=',True)]).mapped('code'):
            self.env['base.language.install'].sudo().create({
                'lang': lang, 
                'overwrite': True
            }).lang_install()
            self.env['base.update.translations'].sudo().create({
                'lang': lang
            }).act_update()
        self.env['ir.translation'].sudo().clear_caches
