sqlalchemy-repl
===============

REPL for SQLAlchemy and Python REPL.

Basic usage
-----------
```
import sqlalchemy as sa
from sqlrepl import sqlrepl

engine = sa.create_engine('sqlite://')
repl = sqlrepl(engine)
```
