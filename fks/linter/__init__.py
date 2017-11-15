import re

class Context:
    def __init__(self):
        self.lineno = 0
        self.charno = 0
        self.colno  = 0
        self.colidx = 0
        self.line   = None

class Event:
    LineEnd    = 'le'
    Macro      = 'm'  # (macro)
    GroupBegin = 'gb' # (depth)
    GroupEnd   = 'ge' # (depth)
    TextBegin  = 'tb' # (text begin string)
    TextEnd    = 'te' # (text end string)

    def __init__(self, e, context, *args):
        self.name = e
        self.context = context
        self.args = args

class Linter:
    # l for line (there should be also c function)
    def l(self, context, message):
        print("Line {}:\t{}".format(context.lineno, message))

class Parser:
    seq = re.compile('[a-zA-Z0-9_]')

    STATE_TEXT    = 1
    STATE_SEQ     = 2
    STATE_COMMENT = 3
        
    def __init__(self):
        self.handlers = {}

        self.fsm = {
            self.STATE_TEXT:    self._st_text,
            self.STATE_SEQ:     self._st_seq,
            self.STATE_COMMENT: self._st_comment,
        }
            
    def register(self, e, handler):
        if not e in self.handlers:
            self.handlers[e] = []
        self.handlers[e].append(handler)


    def parse(self, stream):
        self.depth = 0
        self.macro = None
        self.context = Context()

        for line in stream:
            line = line[:-1]

            self.state = self.STATE_TEXT
            self.context.lineno += 1
            self.context.colno = 0
            self.context.line = line

            begin = True

            for c in line:
                self.context.colidx = self.context.colno
                self.context.colno += 1
                self.context.charno += 1

                ps = self.state
                s = self.fsm[self.state](line,c)
                self.state = s if s else self.state

                if begin and self.state != self.STATE_COMMENT:
                    self._raise(Event.TextBegin, line[self.context.colidx:])
                elif self.state != ps and self.state == self.STATE_COMMENT:
                    self._raise(Event.TextEnd, line[:self.context.colidx])

                begin = False

            if self.state != self.STATE_COMMENT:
                self._raise(Event.TextEnd, line[:self.context.colidx + 1])

            self._raise(Event.LineEnd)

    def _raise(self, e, *args):
        #print("Raise: {}".format(e), args)
        if not e in self.handlers:
            return

        event = Event(e, self.context, *args)
        for h in self.handlers[e]:
            h(event)

    def _st_text(self, line, c):
        if c == '\\':
            self.macro = self.context.colidx + 1
            return self.STATE_SEQ
        elif c == '{':
            self.depth += 1
            self._raise(Event.GroupBegin, self.depth)
        elif c == '}':
            self._raise(Event.GroupEnd, self.depth)
            self.depth -= 1
        elif c == '%':
            return self.STATE_COMMENT

    def _st_seq(self, line, c):
        if self.seq.match(c):
            return self.STATE_SEQ
        else:
            macro = line[self.macro:self.context.colidx]
            self._raise(Event.Macro, macro)
            self.state = self.STATE_TEXT
            return self._st_text(line, c)

    def _st_comment(self, line, c):
        # comment is turned of in main loop
        pass

