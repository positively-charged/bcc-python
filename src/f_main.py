import sys

import common

class front_t:
   def __init__( self ):
      self.options = None
      self.file = None
      self.files = []
      self.files_unloaded = []
      self.text = ''
      self.text_pos = 0
      self.ch = ''
      self.tk = 0
      self.tk_pos = None
      self.tk_pos_s = 0
      self.tk_pos_e = 0
      self.tk_text = ''
      self.tk_peek = False
      self.tk_peeked = None
      self.tk_state = None
      self.module = common.module_t()
      self.scope = None
      self.scopes = []
      self.block = None
      self.importing = False
      self.dec_params = None
      self.dec_for = None
      self.str_table = []
      self.reading_script_number = False
      self.case_stmt = None
      self.num_err = 0
      self.func = None
      self.goto_labels = []
      self.goto_stmts = []

class file_t:
   def __init__( self ):
      self.path = ''
      self.load_path = ''
      self.text = ''
      self.length = 0
      self.pos = 0
      self.line = 1
      self.column = 0
      self.ch = ''

class scope_t:
   def __init__( self ):
      self.names = {}
      self.index = 0
      self.index_high = 0

class fatal_error_t( Exception ):
   pass

DIAG_FILE = 0x1
DIAG_LINE = 0x2
DIAG_COLUMN = 0x4
DIAG_WARN = 0x10
DIAG_ERR = 0x20

def diag( front, flags, *args ):
   if flags & DIAG_FILE:
      pos = args[ 0 ]
      args = args[ 1 : ]
      sys.stdout.write( pos[ 'file' ].path )
      if flags & DIAG_LINE:
         sys.stdout.write( ':' )
         sys.stdout.write( '%d' % pos[ 'line' ] )
         if flags & DIAG_COLUMN:
            sys.stdout.write( ':' )
            sys.stdout.write( '%d' % pos[ 'column' ] )
      sys.stdout.write( ': ' )
   type = flags & 0x70
   if type == DIAG_ERR:
      sys.stdout.write( 'error: ' )
      front.num_err += 1
   elif type == DIAG_WARN:
      sys.stdout.write( 'warning: ' )
   sys.stdout.write( args[ 0 ] % args[ 1 : ] )
   sys.stdout.write( '\n' )

def bail( front ):
   raise fatal_error_t()

def add_scope( front ):
   scope = scope_t()
   front.scopes.append( scope )
   front.scope = scope

def pop_scope( front ):
   front.scopes.pop()
   front.scope = front.scopes[ -1 ]

def find_name( front, name ):
   for scope in front.scopes[ :: -1 ]:
      if name in scope.names:
         return scope.names[ name ]
   return None