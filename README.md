# Usage

    git clone https://github.com/fykosak/fks-linter.git
    cd fks-linter
    ./fks-linter <file-to-check

# Design

  - parsing is based on events (see SAX parsers for XML)
  - checkers register handlers for the events and perform various checks
  - each event comes with `context` that consists of
    - character no
    - line no
    - character no on line
      - `colno` is 1-based
      - `colidx` is 0-based
    - current line
  - for existing events and their optional arguments see class `fks.linter.Event`

  -  high-level arg
    - in math mode

# Implemented checkers #

  - line length
  - eq is indented
  - whitespace at end of line
  
# TODO

  - checkers
    - sentence begins on new line?
    - eq is part of sentence
    - missing ~
    - correctly formated labels of objects
    - check that solution doesn't end in equation
  - switch on/off individual checkers on CLI
  - various severity levels of linting errors
  - colorized output
  - (optionally) print context of linting errors
