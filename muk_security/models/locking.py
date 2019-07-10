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

import os
import hashlib
import logging
import itertools

from odoo import _
from odoo import models, api, fields
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)

class BaseModelLocking(models.AbstractModel):
    
    _name = 'muk_security.locking'
    _description = 'MuK Locking Model'
    _inherit = 'muk_utils.model'
    
    #----------------------------------------------------------
    # Database
    #----------------------------------------------------------
    
    locked = fields.Many2one(
        comodel_name='muk_security.lock', 
        compute='_compute_lock', 
        string="Locked")
    
    locked_state = fields.Boolean(
        compute='_compute_lock', 
        string="Locked")
    
    locked_by = fields.Many2one(
        related='locked.locked_by_ref',
        comodel_name='res.users',
        string="Locked by")
    
    editor = fields.Boolean(
        compute='_compute_editor', 
        string="Editor")

    #----------------------------------------------------------
    # Functions
    #----------------------------------------------------------

    @api.model
    def generate_operation_key(self):
        return hashlib.sha1(os.urandom(128)).hexdigest()
        
    #----------------------------------------------------------
    # Locking
    #----------------------------------------------------------

    @api.multi
    def lock(self, user=None, operation=None, *largs, **kwargs):
        result = []
        for record in self:
            lock = record.is_locked()
            if lock and lock.operation and lock.operation == operation:
                result.append({
                    'record': record, 
                    'lock': lock, 
                    'token': lock.token})
            elif lock and ((lock.operation and lock.operation != operation) or not lock.operation):
                raise AccessError(_("The record (%s[%s]) is locked, so it can't be locked again.") %
                                   (record._name, record.id))
            else:
                token = hashlib.sha1(os.urandom(128)).hexdigest()
                lock = self.env['muk_security.lock'].sudo().create({
                    'locked_by': user and user.name or "System",
                    'locked_by_ref': user and user.id or None,
                    'lock_ref': record._name + ',' + str(record.id),
                    'token': token,
                    'operation': operation})
                result.append({
                    'record': record, 
                    'lock': lock, 
                    'token': token})
        return result
    
    @api.multi
    def unlock(self, *largs, **kwargs):
        for record in self:
            locks = self.env['muk_security.lock'].sudo().search(
                [('lock_ref', '=', "%s,%s" % (record._name, str(record.id)))])
            locks.sudo().unlink()
        return True
    
    @api.model
    def unlock_operation(self, operation, *largs, **kwargs):
        locks = self.env['muk_security.lock'].sudo().search([('operation', '=', operation)])
        references = [
            list((k, list(map(lambda rec: rec.lock_ref_id, v)))) 
               for k, v in itertools.groupby(
                   locks.sorted(key=lambda rec: rec.lock_ref_model),
                   lambda rec: rec.lock_ref_model)]
        locks.sudo().unlink()
        return references
    
    @api.multi
    def is_locked(self, *largs, **kwargs):
        self.ensure_one()
        lock = self.env['muk_security.lock'].sudo().search(
            [('lock_ref', '=', self._name + ',' + str(self.id))], limit=1)
        if lock.id:
            return lock
        return False
    
    @api.multi
    def is_locked_by(self, *largs, **kwargs):
        self.ensure_one()
        lock = self.env['muk_security.lock'].sudo().search(
            [('lock_ref', '=', self._name + ',' + str(self.id))], limit=1)
        if lock.id:
            return lock.locked_by_ref
        return False
    
    @api.multi
    def _checking_lock_user(self, *largs, **kwargs):
        for record in self:
            lock = record.is_locked()
            if lock and lock.locked_by_ref and not lock.locked_by_ref.id != self.env.user.id:
                raise AccessError(_("The record (%s[%s]) is locked by a user, so it can't be changes or deleted.") %
                                   (self._name, self.id))
                
    @api.multi
    def _checking_lock(self, operation=None, *largs, **kwargs):
        self._checking_lock_user()
        for record in self:
            lock = record.is_locked()
            if lock and lock.operation and lock.operation != operation:
                print(operation, lock.operation)
                raise IOError
                raise AccessError(_("The record (%s[%s]) is locked, so it can't be changes or deleted.") %
                                   (self._name, self.id))
    
    @api.multi
    def user_lock(self, *largs, **kwargs):
        self.ensure_one()
        lock = self.is_locked()
        if lock:
            if lock.locked_by_ref:
                raise AccessError(_("The record is already locked by another user. (%s)") % lock.locked_by_ref.name)
            else:
                raise AccessError(_("The record is already locked."))
        return self.lock(user=self.env.user)
    
    @api.multi
    def user_unlock(self, *largs, **kwargs):
        self.ensure_one()
        lock = self.is_locked()
        if lock:
            if lock.locked_by_ref and lock.locked_by_ref.id == self.env.user.id:
                self.unlock()
            else:
                if lock.locked_by_ref:
                    raise AccessError(_("The record is already locked by another user. (%s)") % lock.locked_by_ref.name)
                else:
                    raise AccessError(_("The record is already locked."))
        return True

    #----------------------------------------------------------
    # Read, View 
    #----------------------------------------------------------
    
    @api.multi
    def _compute_lock(self):
        for record in self:
            locked = record.is_locked()
            record.update({
                'locked_state': bool(locked),
                'locked': locked})
    
    @api.depends('locked')  
    def _compute_editor(self):
        for record in self:
            record.editor = record.is_locked_by() == record.env.user
     
    #----------------------------------------------------------
    # Create, Update, Delete
    #----------------------------------------------------------

    @api.multi
    def write(self, vals):
        operation = self.generate_operation_key()
        vals = self._before_write_operation(vals, operation)
        process_operation = self.env.context['operation'] if 'operation' in self.env.context else operation
        result = super(BaseModelLocking, self.with_context(operation=process_operation)).write(vals)
        for record in self:
            record._after_write_record_operation(vals, operation)
        result = self._after_write_operation(result, vals, operation)
        return result

    @api.multi
    def _before_write_operation(self, vals, operation, *largs, **kwargs):
        if 'operation' in self.env.context:
            self._checking_lock(self.env.context['operation'])
        else:
            self._checking_lock(operation)
        return vals
    
    @api.multi
    def _after_write_record_operation(self, vals, operation, *largs, **kwargs):
        return vals    
    
    @api.multi
    def _after_write_operation(self, result, vals, operation, *largs, **kwargs):
        return result

    @api.multi
    def unlink(self):  
        operation = self.generate_operation_key()
        self._before_unlink_operation(operation)
        for record in self:
            record._before_unlink_record_operation(operation)
        process_operation = self.env.context['operation'] if 'operation' in self.env.context else operation
        result = super(BaseModelLocking, self.with_context(operation=process_operation)).unlink()
        self._after_unlink_operation(result, operation)
        return result
    
    @api.multi
    def _before_unlink_operation(self, operation, *largs, **kwargs):
        if 'operation' in self.env.context:
            self._checking_lock(self.env.context['operation'])
        else:
            self._checking_lock(operation)
    
    @api.multi
    def _before_unlink_record_operation(self, operation, *largs, **kwargs):
        pass
    
    @api.multi
    def _after_unlink_operation(self, result, operation, *largs, **kwargs):
        pass
