import os

import f_main
from f_main import ( bail, diag, DIAG_COLUMN, DIAG_ERR, DIAG_FILE, DIAG_LINE )

T_END = 0
T_HASH = 1
T_BRACKET_L  = 2
T_BRACKET_R = 3
T_PAREN_L = 4
T_PAREN_R = 5
T_BRACE_L = 6
T_BRACE_R = 7
T_DOT = 8
T_INC = 9
T_DEC = 10
T_ID = 11
T_COMMA = 12
T_COLON = 13
T_SEMICOLON = 14
T_ASSIGN = 15
T_ASSIGN_ADD = 16
T_ASSIGN_SUB = 17
T_ASSIGN_MUL = 18
T_ASSIGN_DIV = 19
T_ASSIGN_MOD = 20 
T_ASSIGN_SHIFT_L = 21
T_ASSIGN_SHIFT_R = 22
T_ASSIGN_BIT_AND = 23
T_ASSIGN_BIT_XOR = 24
T_ASSIGN_BIT_OR = 25
T_EQ = 26
T_NEQ = 27
T_LOG_NOT = 28
T_LOG_AND = 29
T_LOG_OR = 30
T_BIT_AND = 31
T_BIT_OR = 32
T_BIT_XOR = 33
T_BIT_NOT = 34
T_LT = 35
T_LTE = 36
T_GT = 37
T_GTE = 38
T_PLUS = 39
T_MINUS = 40
T_SLASH = 41
T_STAR = 42
T_MOD = 43
T_SHIFT_L = 44
T_SHIFT_R = 45
T_QUESTION = 46
T_BREAK = 47
T_CASE = 48
T_CONST = 49
T_CONTINUE = 50
T_DEFAULT = 51
T_DO = 52
T_ELSE = 53
T_ENUM = 54
T_FOR = 55
T_IF = 56
T_INT = 57
T_RETURN = 58
T_STATIC = 59
T_STR = 60
T_STRUCT = 61
T_SWITCH = 62
T_VOID = 63
T_WHILE = 64
T_BOOL = 65
T_LIT_DECIMAL = 66
T_LIT_OCTAL = 67
T_LIT_HEX = 68
T_LIT_BINARY = 69
T_LIT_FIXED = 70
T_LIT_STRING = 71
T_LIT_CHAR = 72
T_PALTRANS = 73
T_GLOBAL = 74
T_SCRIPT = 75
T_UNTIL = 76
T_WORLD = 77
T_OPEN = 78
T_RESPAWN = 79
T_DEATH = 80
T_ENTER = 81
T_PICKUP = 82
T_BLUE_RETURN = 83
T_RED_RETURN = 84
T_WHITE_RETURN = 85
T_LIGHTNING = 86
T_DISCONNECT = 87
T_UNLOADING = 88
T_CLIENTSIDE = 89
T_NET = 90
T_RESTART = 91
T_SUSPEND = 92
T_TERMINATE = 93
T_FUNCTION = 94
T_SPECIAL = 95
T_GOTO = 96

def load_file( front, user_path ):
   direct = False
   includes_i = 0
   path = ''
   while True:
      if not direct:
         path = user_path
         direct = True
      elif includes_i < len( front.options.includes ):
         path = front.options.includes[ includes_i ] + '/' + user_path
         includes_i += 1
      else:
         return False
      path = os.path.abspath( path )
      if path:
         try:
            source = open( path )
            file = f_main.file_t()
            file.path = user_path
            file.load_path = path
            file.text = source.read()
            file.length = len( file.text )
            if front.file:
               front.file.ch = front.ch
               front.files.append( front.file )
            front.file = file
            front.ch = file.text[ 0 ]
            source.close()
            return True
         except IOError:
            pass

def unload_file( front ):
   if front.files:
      front.files_unloaded.append( front.file )
      front.file = front.files.pop()
      front.ch = front.file.ch
      read( front )
   else:
      front.file = None

def read_ch( front ):
   pos = front.file.pos + 1
   if pos < front.file.length:
      if front.ch == '\n':
         front.file.line += 1
         front.file.column = 0
      else:
         front.file.column += 1
      front.ch = front.file.text[ pos ]
      front.file.pos = pos
   else:
      front.ch = ''
      front.file.pos = front.file.length

def peek_ch( front ):
   pos = front.file.pos + 1
   if pos < front.file.length:
      return front.file.text[ pos ]
   else:
      return ''

def read( front ):
   token = front.tk_peeked
   if not token:
      token = read_token( front )
   front.tk = token[ 'type' ]
   front.tk_pos = token[ 'pos' ]
   front.tk_text = token[ 'text' ]
   front.tk_peeked = None

def peek( front ):
   if not front.tk_peeked:
      front.tk_peeked = read_token( front )
   return front.tk_peeked[ 'type' ]

def found( front, token, type ):
   token[ 'type' ] = type
   if not token[ 'text' ]:
      pos_e = front.file.pos
      if token[ 'pos_e' ]:
         pos_e = token[ 'pos_e' ]
      token[ 'text' ] = front.file.text[ token[ 'pos_s' ] : pos_e ]
   token[ 'pos' ] = {
      'file' : token[ 'pos_f' ], 
      'line' : token[ 'pos_l' ],
      'column' : token[ 'pos_c' ] }
   token[ 'state' ] = None

def read_token( front ):
   token = {
      'state' : state_start,
      'pos_s' : 0,
      'pos_e' : 0,
      'pos_f' : None,
      'pos_l' : 0,
      'pos_c' : 0,
      'type' : T_END,
      'text' : ''
   }
   while token[ 'state' ]:
      token[ 'state' ]( front, token )
   return token

def state_start( front, token ):
   while front.ch.isspace():
      read_ch( front )
   token[ 'pos_s' ] = front.file.pos
   token[ 'pos_f' ] = front.file
   token[ 'pos_l' ] = front.file.line
   token[ 'pos_c' ] = front.file.column
   if front.ch.isalpha() or front.ch == '_':
      while front.ch.isalnum() or front.ch == '_':
         read_ch( front )
      id = front.file.text[ token[ 'pos_s' ] : front.file.pos ]
      id = id.lower()
      token[ 'text' ] = id
      reserved = {
         'bluereturn' : T_BLUE_RETURN,
         'bool' : T_BOOL,
         'break' : T_BREAK,
         'case' : T_CASE,
         'clientside' : T_CLIENTSIDE,
         'const' : T_CONST,
         'continue' : T_CONTINUE,
         'createtranslation' : T_PALTRANS,
         'death' : T_DEATH,
         'default' : T_DEFAULT,
         'disconnect' : T_DISCONNECT,
         'do' : T_DO,
         'else' : T_ELSE,
         'enter' : T_ENTER,
         'for' : T_FOR,
         'function' : T_FUNCTION,
         'global' : T_GLOBAL,
         'goto' : T_GOTO,
         'if' : T_IF,
         'int' : T_INT,
         'lightning' : T_LIGHTNING,
         'net' : T_NET,
         'open' : T_OPEN,
         'redreturn' : T_RED_RETURN,
         'respawn' : T_RESPAWN,
         'restart' : T_RESTART,
         'return' : T_RETURN,
         'script' : T_SCRIPT,
         'special' : T_SPECIAL,
         'static' : T_STATIC,
         'str' : T_STR,
         'suspend' : T_SUSPEND,
         'switch' : T_SWITCH,
         'terminate' : T_TERMINATE,
         'unloading' : T_UNLOADING,
         'until' : T_UNTIL,
         'void' : T_VOID,
         'while' : T_WHILE,
         'whitereturn' : T_WHITE_RETURN,
         'world' : T_WORLD
      }
      if id in reserved:
         found( front, token, reserved[ id ] )
      else:
         found( front, token, T_ID )
   elif front.ch == '0':
      read_ch( front )
      # Fixed literal.
      if front.ch == '.':
         read_ch( front )
         while front.ch.isdigit():
            read_ch( front )
         found( front, token, T_LIT_FIXED )
      # Hexadecimal literal.
      elif front.ch == 'x' or front.ch == 'X':
         read_ch( front )
         while ( 
            ( front.ch >= '0' and front.ch <= '9' ) or
            ( front.ch >= 'a' and front.ch <= 'f' ) or
            ( front.ch >= 'A' and front.ch <= 'F' ) ):
            read_ch( front )
         token[ 'pos_s' ] += 2
         found( front, token, T_LIT_HEX )
      # Octal literal.
      else:
         length = 0
         while front.ch >= '0' and front.ch <= '7':
            read_ch( front )
            length += 1
         if length:
            token[ 'pos_s' ] += 1
            found( front, token, T_LIT_OCTAL )
         else:
            found( front, token, T_LIT_DECIMAL )
            
   elif front.ch >= '1' and front.ch <= '9':
      while front.ch.isdigit():
         read_ch( front )
      if front.ch == '.':
         read_ch( front )
         while front.ch.isdigit():
            read_ch( front )
         found( front, token, T_LIT_FIXED )
      else:
         found( front, token, T_LIT_DECIMAL )
   elif front.ch == '"':
      read_ch( front )
      while True:
         if front.ch == '':
            # Error
            pass
         elif front.ch == '"':
            read_ch( front )
            break
         else:
            read_ch( front )
      token[ 'pos_s' ] += 1
      token[ 'pos_e' ] = front.file.pos - 1
      found( front, token, T_LIT_STRING )
   elif front.ch == '\'':
      read_ch( front )
      if front.ch == '\\':
         pass
      elif front.ch == '\'' or front.ch == '':
         pass
      else:
         read_ch( front )
         if front.ch == '\'':
            token[ 'pos_s' ] += 1
            token[ 'pos_e' ] = front.file.pos
            read_ch( front )
            found( front, token, T_LIT_CHAR )
         else:
            pass
   elif front.ch == '=':
      read_ch( front )
      if front.ch == '=':
         found( front, token, T_EQ )
         read_ch( front )
      else:
         found( front, token, T_ASSIGN )
   elif front.ch == '!':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_NEQ )
      else:
         found( front, token, T_LOG_NOT )
   elif front.ch == '+':
      read_ch( front )
      if front.ch == '+':
         read_ch( front )
         found( front, token, T_INC )
      elif front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_ADD )
      else:
         found( front, token, T_PLUS )
   elif front.ch == '-':
      read_ch( front )
      if front.ch == '-':
         read_ch( front )
         found( front, token, T_DEC )
      elif front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_SUB )
      else:
         found( front, token, T_MINUS )
   elif front.ch == '*':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_MUL )
      else:
         found( front, token, T_STAR )
   elif front.ch == '/':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_DIV )
      elif front.ch == '/':
         while front.ch != '' and front.ch != '\n':
            read_ch( front )
      elif front.ch == '*':
         while True:
            if front.ch == '':
               pass
            elif front.ch == '*' and peek_ch( front ) == '/':
               read_ch( front )
               read_ch( front )
               break
            else:
               read_ch( front )
      else:
         found( front, token, T_SLASH )
   elif front.ch == '%':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_MOD )
      else:
         found( front, token, T_MOD )
   elif front.ch == '<':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_LTE )
      elif front.ch == '<':
         read_ch( front )
         if front.ch == '=':
            read_ch( front )
            found( front, token, T_ASSIGN_SHIFT_L )
         else:
            found( front, token, T_SHIFT_L )
      else:
         found( front, token, T_LT )
   elif front.ch == '>':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_GTE )
      elif front.ch == '>':
         read_ch( front )
         if front.ch == '=':
            read_ch( front )
            found( front, token, T_ASSIGN_SHIFT_R )
         else:
            found( front, token, T_SHIFT_R )
      else:
         found( front, token, T_GT )
   elif front.ch == '&':
      read_ch( front )
      if front.ch == '&':
         read_ch( front )
         found( front, token, T_LOG_AND )
      elif front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_BIT_AND )
      else:
         found( front, token, T_BIT_AND )
   elif front.ch == '|':
      read_ch( front )
      if front.ch == '|':
         read_ch( front )
         found( front, token, T_LOG_OR )
      elif front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_BIT_OR )
      else:
         found( front, token, T_BIT_OR )
   elif front.ch == '^':
      read_ch( front )
      if front.ch == '=':
         read_ch( front )
         found( front, token, T_ASSIGN_BIT_XOR )
      else:
         found( front, token, T_BIT_XOR )
   else:
      tokens = {
         ';' : T_SEMICOLON,
         ',' : T_COMMA,
         '(' : T_PAREN_L,
         ')' : T_PAREN_R,
         '[' : T_BRACKET_L,
         ']' : T_BRACKET_R,
         '{' : T_BRACE_L,
         '}' : T_BRACE_R,
         ':' : T_COLON,
         '~' : T_BIT_NOT,
         '#' : T_HASH
      }
      if front.ch in tokens:
         type = tokens[ front.ch ]
         read_ch( front )
         found( front, token, type )
      elif front.ch == '':
         found( front, token, T_END )
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'invalid character \'%s\'', front.ch )
         read_ch( front )

def test( front, expected ):
   if front.tk != expected:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'unexpected token: %s', front.tk_text )
      bail( front )