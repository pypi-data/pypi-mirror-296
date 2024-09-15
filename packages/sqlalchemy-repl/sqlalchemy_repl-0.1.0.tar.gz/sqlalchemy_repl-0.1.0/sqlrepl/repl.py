import sqlalchemy as sa
import prompt_toolkit.lexers
import pygments.lexers.sql
import shlex
from tabulate import tabulate

from .settings import DEFAULT_SETTINGS
from .cmd import DEFAULT_CMD

class SQLRepl:
    settings = DEFAULT_SETTINGS
    cmd = DEFAULT_CMD

    def __init__(self, engine):

        self.engine = engine
        self.connection = self.engine.connect()
        self.result = None
        self.columns = None
        self.query = None
        self.cursor = None

        self.prompt_session = prompt_toolkit.PromptSession(
            lexer=prompt_toolkit.lexers.PygmentsLexer(
                pygments.lexers.sql.SqlLexer
            )
        )
        self.prompt = '>'

    def run(self):
        while True:
            try:
                text = self.prompt_session.prompt(self.prompt)
            except KeyboardInterrupt:  # ^C
                continue
            except EOFError:  # ^D
                break

            try:
                if len(text) == 0:
                    continue
                elif text.startswith(':'):
                    cmd, *args = shlex.split(text[1:])
                    try:
                        cmd = self.cmd[cmd]
                    except KeyError:
                        print(f"Command '{cmd}' not found")
                        continue
                    cmd(self, *args)
                else:
                    self.query = text
                    self.execute()
                    self.print()
            except Exception as e:
                print(repr(e))

    def execute(self):
        if self.query is None:
            return
        self.cursor = self.connection.execute(sa.text(self.query))
        # TODO: what to do when doesnt return rows
        self.columns = list(self.cursor.keys())
        if (preview:=self.settings['preview']) > 0:
            rows = self.cursor.fetchmany(preview)
        else:
            rows = self.cursor.fetchall()
        self.result = rows

    def print(self):
        if self.result is not None:
            if self.columns is not None:
                print(tabulate(self.result, headers=self.columns))
            else:
                print(tabulate(self.result))
