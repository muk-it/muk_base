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

import json
import logging
import psycopg2
import functools

from contextlib import closing
from datetime import datetime

from werkzeug.contrib.sessions import SessionStore

from odoo.sql_db import db_connect
from odoo.tools import config, DEFAULT_SERVER_DATETIME_FORMAT

_logger = logging.getLogger(__name__)

def ensure_cursor(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        for attempts in range(1, 6):
            try:
                return func(self, *args, **kwargs)
            except psycopg2.InterfaceError as error:
                _logger.info("SessionStore connection failed! (%s/5)" % attempts)
                if attempts < 5:
                    self._open_connection()
                else:
                    raise error
    return wrapper

class PostgresSessionStore(SessionStore):
    
    def __init__(self, *args, **kwargs):
        super(PostgresSessionStore, self).__init__(*args, **kwargs)
        self.dbname = config.get('session_store_dbname', 'session_store')
        self._open_connection()
        self._setup_db()
    
    def _create_database(self):
        with closing(db_connect("postgres").cursor()) as cursor:
            cursor.autocommit(True)
            cursor.execute("""
                CREATE DATABASE {dbname} 
                ENCODING 'unicode'
                TEMPLATE 'template0';
            """.format(dbname=self.dbname))
        self._setup_db()
        
    def _open_connection(self, create_db=True):
        try:
            connection = db_connect(self.dbname, allow_uri=True)
            self.cursor = connection.cursor()
            self.cursor.autocommit(True)
        except:
            if not create_db:
                raise
            self._create_database()
            return self._open_connection(create_db=False)

    @ensure_cursor
    def _setup_db(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                sid varchar PRIMARY KEY,
                write_date timestamp without time zone NOT NULL,
                payload text NOT NULL
            );
        """)
    
    @ensure_cursor
    def save(self, session):
        self.cursor.execute("""
            INSERT INTO sessions (sid, write_date, payload)
            VALUES (%(sid)s, now() at time zone 'UTC', %(payload)s)
            ON CONFLICT (sid)
            DO UPDATE SET payload = %(payload)s, write_date = now() at time zone 'UTC';
        """, dict(sid=session.sid, payload=json.dumps(dict(session))))
        
    @ensure_cursor
    def delete(self, session):
        self.cursor.execute("DELETE FROM sessions WHERE sid=%s;", [session.sid])
    
    @ensure_cursor
    def get(self, sid):
        if not self.is_valid_key(sid):
            return self.new()
        self.cursor.execute("""
            SELECT payload, write_date 
            FROM sessions WHERE sid=%s;
        """, [sid])
        try:
            payload, write_date = self.cursor.fetchone()
            if isinstance(write_date, str):
                write_date = datetime.strptime(
                    write_date, DEFAULT_SERVER_DATETIME_FORMAT
                )
            if write_date.date() != datetime.today().date():
                self.cursor.execute("""
                    UPDATE sessions 
                    SET write_date = now() at time zone 'UTC' 
                    WHERE sid=%s;
                """, [sid])
            return self.session_class(json.loads(payload), sid, False)
        except Exception as error:
            _logger.exception("PostgresSessionStore", exc_info=error)
            return self.session_class({}, sid, False)
    
    @ensure_cursor
    def list(self):
        self.cursor.execute("SELECT sid FROM sessions;")
        return [record[0] for record in self.cursor.fetchall()]
    
    @ensure_cursor
    def clean(self):
        self.cursor.execute("""
            DELETE FROM sessions 
            WHERE now() at time zone 'UTC' - write_date > '7 days';
        """)