###################################################################################
#
#    Copyright (C) 2018 MuK IT GmbH
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

from odoo import api, models, fields
from odoo.osv import expression

from odoo.addons.muk_utils.tools import utils

_logger = logging.getLogger(__name__)

class Base(models.AbstractModel):
    
    _inherit = 'base'
    
    #----------------------------------------------------------
    # Hierarchy Methods
    #----------------------------------------------------------
    
    @api.model
    def search_parents(self, domain=[], order=None):
        """ This method finds the top level elements of the hierarchy for a given search query.
            
            :param domain: a search domain <reference/orm/domains> (default: empty list)
            :param order: a string to define the sort order of the query (default: none)
            :returns: the top level elements for the given search query 
        """
        return self.browse(self._search_parents(domain=domain, order=order))
    
    @api.model
    def search_read_parents(self, domain=[], fields=None, order=None):
        """ This method finds the top level elements of the hierarchy for a given search query.
            
            :param domain: a search domain <reference/orm/domains> (default: empty list)
            :param fields: a list of fields to read (default: all fields of the model)
            :param order: a string to define the sort order of the query (default: none)
            :returns: the top level elements for the given search query 
        """
        records = self.search_parents(domain=domain, order=order)
        if not records:
            return []
        if fields and fields == ['id']:
            return [{'id': record.id} for record in records]
        result = records.read(fields)
        if len(result) <= 1:
            return result
        index = {vals['id']: vals for vals in result}
        return [index[record.id] for record in records if record.id in index]
        
    @api.model
    def _search_parents(self, domain=[], order=None):
        if not self._parent_store or self._parent_name not in self._fields:
            raise TypeError("Model %r does not exist in registry." % name)
        self.check_access_rights('read')
        if expression.is_false(self, domain):
            return []
        query = self._where_calc(domain)
        self._apply_ir_rules(query, 'read')
        from_clause, where_clause, where_clause_arguments = query.get_sql()
        parent_where = where_clause and (" WHERE %s" % where_clause) or ''
        parent_query = 'SELECT "%s".id FROM ' % self._table + from_clause + parent_where
        no_parent_clause ='"{table}"."{field}" IS NULL'.format(
            table=self._table, 
            field=self._parent_name
        )
        no_access_clause ='"{table}"."{field}" NOT IN ({query})'.format(
            table=self._table,
            field=self._parent_name,
            query=parent_query
        )
        parent_clause = '({0} OR {1})'.format(
            no_parent_clause,
            no_access_clause
        )
        order_by = self._generate_order_by(order, query)
        from_clause, where_clause, where_clause_params = query.get_sql()

        where_str = (
            where_clause and 
            (" WHERE %s AND %s" % (where_clause, parent_clause)) or 
            (" WHERE %s" % parent_clause)
        )
        query_str = 'SELECT "%s".id FROM ' % self._table + from_clause + where_str + order_by
        complete_where_clause_params = where_clause_params + where_clause_arguments
        self._cr.execute(query_str, complete_where_clause_params)
        return utils.uniquify_list([x[0] for x in self._cr.fetchall()])