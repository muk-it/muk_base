# MuK Large Objects Field

PostgreSQL offers support for large objects, which provide stream-style access to user data that is stored in a special large-object structure. They are useful with data values too large to be manipulated conveniently as a whole.

Psycopg allows access to the large object using the `lobject` class. Objects are generated using the `connection.lobject()` factory method. Data can be retrieved either as bytes or as Unicode strings.

Psycopg large object support efficient import/export with file system files using the `lo_import()` and `lo_export()` libpq functions.

Changed in version 2.6: added support for large objects greated than 2GB. Note that the support is enabled only if all the following conditions are verified:

* the Python build is 64 bits;
* the extension was built against at least libpq 9.3;
* the server version is at least PostgreSQL 9.3 (server_version must be >= 90300).

If Psycopg was built with 64 bits large objects support (i.e. the first two contidions above are verified), the `psycopg2.__version__` constant will contain the lo64 flag. If any of the contition is not met several lobject methods will fail if the arguments exceed 2GB.