###################################################################################
# 
#    Copyright (C) 2017 MuK IT GmbH
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################

import logging

from odoo import models, api

_logger = logging.getLogger(__name__)

class BaseModelExtension(models.AbstractModel):
    
    _name = 'muk_utils.model'
    _description = 'MuK Base Model'

    #----------------------------------------------------------
    # Function
    #----------------------------------------------------------
    
    @api.multi
    def notify_change(self, values, *largs, **kwargs):
        pass
    
    @api.multi
    def trigger_computation(self, fields, *largs, **kwargs):
        pass
    
    @api.multi
    def check_existence(self):
        records = self.exists()
        if not (len(records) == 0 or (len(records) == 1 and records.id == False)):
            return records
        else:
            return False
    
    #----------------------------------------------------------
    # Read
    #----------------------------------------------------------
    
    @api.model
    def browse(self, arg=None, prefetch=None):
        arg = self._before_browse(arg)
        result = super(BaseModelExtension, self).browse(arg, prefetch)
        result = self._after_browse(result)
        return result
    
    @api.model
    def _before_browse(self, arg, *largs, **kwargs):
        return arg

    @api.model
    def _after_browse(self, result, *largs, **kwargs):
        return result
    
    @api.multi
    def read(self, fields=None, load='_classic_read'):
        fields = self._before_read(fields)
        result = super(BaseModelExtension, self).read(fields, load)
        for index, record in enumerate(self.exists()):
            try:
                result[index] = record._after_read_record(result[index])  
            except IndexError:
                _logger.exception("Something went wrong!")
        result = self._after_read(result)
        return result
    
    @api.multi
    def _before_read(self, fields, *largs, **kwargs):
        return fields

    @api.multi
    def _after_read_record(self, values, *largs, **kwargs):
        return values
    
    @api.multi
    def _after_read(self, result, *largs, **kwargs):
        return result
    
    @api.model
    @api.returns('self',
        upgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else self.browse(value),
        downgrade=lambda self, value, args, offset=0, limit=None, order=None, count=False: value if count else value.ids)
    def search(self, args, offset=0, limit=None, order=None, count=False):
        args, offset, limit, order, count = self._before_search(args, offset, limit, order, count)
        result = super(BaseModelExtension, self).search(args, offset, limit, order, count)
        result = self._after_search(result)
        return result
    
    @api.model
    def _before_search(self, args, offset, limit, order, count, *largs, **kwargs):
        return args, offset, limit, order, count
    
    @api.model
    def _after_search(self, result, *largs, **kwargs):
        return result
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        name, args, operator, limit = self._before_name_search(name, args, operator, limit)
        result = super(BaseModelExtension, self).name_search(name, args, operator, limit)
        result = self._after_name_search(result)
        return result
    
    @api.model
    def _before_name_search(self, name, args, operator, limit, *largs, **kwargs):
        return name, args, operator, limit

    @api.model
    def _after_name_search(self, result, *largs, **kwargs):
        return result
    
    @api.model
    def read_group(self, domain, fields, groupby, offset=0, limit=None, orderby=False, lazy=True):
        domain, fields, groupby, offset, limit, orderby, lazy = self._before_read_group(domain, fields, groupby, offset, limit, orderby, lazy)
        result = super(BaseModelExtension, self).read_group(domain, fields, groupby, offset, limit, orderby, lazy)
        result = self._after_read_group(result)
        return result
    
    @api.model
    def _before_read_group(self, domain, fields, groupby, offset, limit, orderby, lazy, *largs, **kwargs):
        return domain, fields, groupby, offset, limit, orderby, lazy

    @api.model
    def _after_read_group(self, result, *largs, **kwargs):
        return result
        
    #----------------------------------------------------------
    # Create, Update, Delete
    #----------------------------------------------------------
    
    @api.model
    def create(self, vals):
        vals = self._before_create(vals)
        result = super(BaseModelExtension, self).create(vals)
        result = result._after_create(vals)
        return result
    
    @api.model
    def _before_create(self, vals, *largs, **kwargs):
        return vals
        
    @api.model
    def _after_create(self, vals, *largs, **kwargs):
        self._check_recomputation(vals, [])
        return self

    @api.multi
    def write(self, vals):
        olds = []
        vals = self._before_write(vals)
        if 'track_old_values' in self.env.context:
            olds = [{key: record[key] for key in vals} for record in self]
        result = super(BaseModelExtension, self).write(vals)
        for record in self:
            record._after_write_record(vals)
        result = self._after_write(result, vals, olds)
        return result
    
    @api.multi
    def _before_write(self, vals, *largs, **kwargs):
        return vals
    
    @api.multi
    def _after_write_record(self, vals, *largs, **kwargs):
        return vals    
        
    @api.multi
    def _after_write(self, result, vals, olds, *largs, **kwargs):
        self._check_recomputation(vals, olds)
        self._check_notification(vals)
        return result

    @api.multi
    def unlink(self):
        info = self._before_unlink()
        infos = []
        for record in self:
            infos.append(record._before_unlink_record())
        result = super(BaseModelExtension, self).unlink()
        self._after_unlink(result, info, infos)
        return result
    
    @api.multi
    def _before_unlink(self, *largs, **kwargs):
        return {}
    
    @api.multi
    def _before_unlink_record(self, *largs, **kwargs):
        return {}    
    
    @api.multi
    def _after_unlink(self, result, info, infos, *largs, **kwargs):
        pass
    
    #----------------------------------------------------------
    # Helper
    #----------------------------------------------------------
    
    @api.multi
    def _check_recomputation(self, vals, olds, *largs, **kwargs):
        # self.trigger_computation(fields)
        pass
    
    @api.multi
    def _check_notification(self, vals, *largs, **kwargs):
        # self.notify_change(change)
        pass