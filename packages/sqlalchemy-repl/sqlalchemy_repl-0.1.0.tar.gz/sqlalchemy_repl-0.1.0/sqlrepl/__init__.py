from .repl import SQLRepl as SQLRepl

def sqlrepl(engine):
    repl = SQLRepl(engine)
    repl.run()
    return repl
