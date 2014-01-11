import common
import f_main
from f_main import ( bail, diag, DIAG_COLUMN, DIAG_ERR, DIAG_FILE, DIAG_LINE )
import f_token as tk
import f_dec
import f_expr
import b_chunk

def compile( args ):
   options = common.options_t()
   # Program name not needed.
   if not read_options( options, args[ 1 : ]  ):
      return False
   front = f_main.front_t()
   front.options = options
   # Top scope.
   f_main.add_scope( front )
   f_dec.load_ded_format_funcs( front )
   if not tk.load_file( front, options.source_file ):
      print( 'error: failed to load file:', options.source_file )
      exit( 1 )

   '''
   while True:
      print( tk.peek( front ) )
      tk.read( front )
      print( front.tk_text )
      if front.tk == tk.k_end:
         break
   exit( 0 )'''

   try:
      tk.read( front )
      read_module( front )
   except f_main.fatal_error_t:
      exit( 1 )
   if front.num_err:
      exit( 1 )
   b_chunk.publish( front.module, front.str_table, options )
   exit( 0 )

def read_options( options, args ):
   i = 0
   count = len( args )
   while i < count:
      name = ''
      arg = args[ i ]
      if arg[ 0 ] == '-':
         if len( arg ) > 1:
            name = arg[ 1 ]
            i += 1
         else:
            print( 'error: \'-\' without an option name' )
            return False
      else:
         break
      if name == 'i' or name == 'I':
         if i < count:
            options.includes.append( args[ i ] )
            i += 1
         else:
            print( 'error: missing path in include-path argument' )
            return False
      elif name == 'e':
         options.err_file = True
      else:
         print( 'error: unknown option:', name )
         return False
   if i < count:
      options.source_file = args[ i ]
      i += 1
   else:
      print( 'error: missing source file to compile' )
      return False
   if i < count:
      options.object_file = args[ i ]
   return True

def read_module( front ):
   got_header = False
   if front.tk == tk.T_HASH:
      pos = front.tk_pos
      tk.read( front )
      if front.tk == tk.T_ID and front.tk_text == 'library':
         print( front.tk )
         pass
      else:
         read_dirc( front, pos )
   # Header required for an imported module.
   if front.importing and not got_header:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, 
         front.tk_pos, 'missing #library name in imported module' )
   while True:
      if front.tk == tk.T_SCRIPT:
         f_dec.read_script( front )
      elif f_dec.is_dec( front ):
         f_dec.read( front, f_dec.AREA_TOP )
      elif front.tk == tk.T_HASH:
         pos = front.tk_pos
         tk.read( front )
         read_dirc( front, pos )
      elif front.tk == tk.T_SPECIAL:
         f_dec.read_bfunc_list( front )
      elif front.tk == tk.T_END:
         tk.unload_file( front )
         if not front.file:
            break
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'unexpected token: %s', front.tk_text )
         tk.read( front )

def read_dirc( front, pos ):
   tk.test( front, tk.T_ID )
   if front.tk_text == 'define' or front.tk_text == 'libdefine':
      tk.read( front )
      name = f_dec.read_unique_name( front )
      expr = f_expr.read( front, True )
      if not front.importing or name[ 0 ] == 'l':
         constant = common.constant_t()
         constant.value = expr.value
         constant.pos = pos
         front.scope.names[ name ] = constant
   elif front.tk_text == 'include':
      tk.read( front )
      tk.test( front, tk.T_LIT_STRING )
      include_file( front )
      tk.read( front )
   elif front.tk_text == 'import':
      pass
   elif front.tk_text == 'library':
      tk.read( front )
      tk.test( front, tk.T_LIT_STRING )
      tk.read( front )
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
         '#library name between code' )
      diag( front, DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
         '#library name must appear at the very top, '
         'before any other code' )
   # Switch to the Big-E format.
   elif front.tk_text == 'nocompact':
      tk.read( front )
      if not front.importing:
         front.options.format = common.FORMAT_BIG_E
   elif front.tk_text == 'encryptstrings':
      tk.read( front )
      if not front.importing:
         front.options.encrypt_str = True
   elif (
      # NOTE: Not sure what these two are.
      front.tk_text == 'wadauthor' or
      front.tk_text == 'nowadauthor' ):
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
         'directive not supported: %s', front.tk_text )
      tk.read( front )
   else:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
         'unknown directive: %s', front.tk_text )
      bail( front )

def include_file( front ):
   if front.tk_text == '':
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'path is empty' )
      bail( front )
   elif not tk.load_file( front, front.tk_text ):
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'failed to load file: %s', front.tk_text )
      bail( front )

def read_stmt( front ):
   if front.tk == tk.T_BRACE_L:
      f_main.add_scope( front )
      read_block( front )
      f_main.pop_scope( front )
   elif front.tk == tk.T_IF:
      tk.read( front )
      tk.test( front, tk.T_PAREN_L )
      tk.read( front )
      expr = f_expr.read( front, True )
      tk.test( front, tk.T_PAREN_R )
      tk.read( front )
      block = common.block_t()
      block.parent = front.block
      front.block = block
      read_stmt( front )
      block_else = None
      if front.tk == tk.T_ELSE:
         tk.read( front )
         block_else = common.block_t()
         block_else.parent = block.parent
         front.block = block_else
         read_stmt( front )
      stmt = common.if_t()
      stmt.cond = expr
      stmt.body = block
      stmt.else_body = block_else
      block.parent.stmts.append( stmt )
      front.block = block.parent
   elif front.tk == tk.T_SWITCH:
      tk.read( front )
      tk.test( front, tk.T_PAREN_L )
      tk.read( front )
      stmt = common.switch_t()
      stmt.cond = f_expr.read( front, True )
      tk.test( front, tk.T_PAREN_R )
      tk.read( front )
      parent = front.case_stmt
      front.case_stmt = stmt
      block = common.block_t()
      block.in_switch = True
      block.parent = front.block
      front.block = block
      f_main.add_scope( front )
      read_stmt( front )
      f_main.pop_scope( front )
      front.block = block.parent
      front.case_stmt = parent
      stmt.body = block
      front.block.stmts.append( stmt )
   elif front.tk in [ tk.T_CASE, tk.T_DEFAULT ]:
      pos = front.tk_pos
      block = front.block
      while block and not block.in_switch:
         block = block.parent
      if not block:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'case outside switch statement' )
      elif block is not front.block:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'case inside a nested statement' )
      expr = None
      if front.tk == tk.T_CASE:
         tk.read( front )
         expr = f_expr.read( front, True )
      else:
         tk.test( front, tk.T_DEFAULT )
         tk.read( front )
      tk.test( front, tk.T_COLON )
      tk.read( front )
      if expr:
         if not expr.folded:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               expr.pos, 'case value not constant' )
            bail( front )
         for stmt in front.case_stmt.cases:
            if stmt.expr and stmt.expr.value == expr.value:
               diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
                  pos, 'case with value %d is duplicated', expr.value )
               diag( front, DIAG_FILE | DIAG_LINE | DIAG_COLUMN, stmt.pos,
                  'previous case found here' )
      else:
         if front.case_stmt.default_case:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
               'default case is duplicated' )
            diag( front, DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.case_stmt.default_case.pos,
               'previous default case found here' )
            bail( front )
      stmt = common.case_t()
      stmt.expr = expr
      stmt.pos = pos
      front.block.stmts.append( stmt )
      front.case_stmt.cases.append( stmt )
      if expr:
         pass
      else:
         front.case_stmt.default_case = stmt
   elif front.tk in [ tk.T_WHILE, tk.T_UNTIL, tk.T_DO ]:
      do = False
      if front.tk == tk.T_DO:
         tk.read( front )
         do = True
      type = common.WHILE_WHILE
      expr = None
      if not do:
         if front.tk == tk.T_UNTIL:
            type = common.WHILE_UNTIL
            tk.read( front )
         else:
            tk.test( front, tk.T_WHILE )
            tk.read( front )
         tk.test( front, tk.T_PAREN_L )
         tk.read( front )
         expr = f_expr.read( front, True )
         tk.test( front, tk.T_PAREN_R )
         tk.read( front )
      block = common.block_t()
      block.in_loop = True
      block.parent = front.block
      front.block = block
      read_stmt( front )
      front.block = block.parent
      if do:
         type = common.WHILE_DO_WHILE
         if front.tk == tk.T_UNTIL:
            type = common.WHILE_DO_UNTIL
            tk.read( front )
         else:
            tk.test( front, tk.T_WHILE )
            tk.read( front )
         tk.test( front, tk.T_PAREN_L )
         tk.read( front )
         expr = f_expr.read( front, True )
         tk.test( front, tk.T_PAREN_R )
         tk.read( front )
         tk.test( front, tk.T_SEMICOLON )
         tk.read( front )
      stmt = common.while_t()
      stmt.type = type
      stmt.cond = expr
      stmt.body = block
      block.parent.stmts.append( stmt )
   elif front.tk == tk.T_FOR:
      tk.test( front, tk.T_FOR )
      tk.read( front )
      tk.test( front, tk.T_PAREN_L )
      tk.read( front )
      f_main.add_scope( front )
      # Optional initialization:
      dec = None
      init = None
      if front.tk != tk.T_SEMICOLON:
         if f_dec.is_dec( front ):
            front.dec_for = []
            f_dec.read( front, f_dec.AREA_FOR )
            dec = front.dec_for
            front.dec_for = None
         else:
            init = []
            while True:
               init.append( f_expr.read( front, False ) )
               if front.tk == tk.T_COMMA:
                  tk.read( front )
               else:
                  tk.test( front, tk.T_SEMICOLON )
                  tk.read( front )
                  break
      else:
         tk.read( front )
      # Optional condition:
      cond = None
      if front.tk != tk.T_SEMICOLON:
         cond = f_expr.read( front, True )
         tk.test( front, tk.T_SEMICOLON )
         tk.read( front )
      else:
         tk.read( front )
      # Optional post-expression:
      post = None
      if front.tk != tk.T_PAREN_R:
         post = []
         while True:
            post.append( f_expr.read( front, False ) )
            if front.tk == tk.T_COMMA:
               tk.read( front )
            else:
               tk.test( front, tk.T_PAREN_R )
               tk.read( front )
               break
      else:
         tk.read( front )
      block = common.block_t()
      block.in_loop = True
      block.parent = front.block
      front.block = block
      read_stmt( front )
      front.block = block.parent
      f_main.pop_scope( front )
      stmt = common.for_t()
      stmt.init = init
      if dec:
         stmt.dec = dec
      stmt.cond = cond
      stmt.post = post
      stmt.body = block
      front.block.stmts.append( stmt )
   elif front.tk == tk.T_BREAK:
      pos = front.tk_pos
      tk.read( front )
      tk.test( front, tk.T_SEMICOLON )
      tk.read( front )
      block = front.block
      while block and not ( block.in_loop or block.in_switch ):
         block = block.parent
      if block:
         stmt = common.jump_t()
         front.block.stmts.append( stmt )
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'break outside loop or switch' )
   elif front.tk ==  tk.T_CONTINUE:
      pos = front.tk_pos
      tk.read( front )
      tk.test( front, tk.T_SEMICOLON )
      tk.read( front )
      block = front.block
      while block and not block.in_loop:
         block = block.parent
      if block:
         stmt = common.jump_t()
         stmt.type = common.JUMP_CONTINUE
         front.block.stmts.append( stmt )
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'continue outside loop' )
   elif front.tk in [ tk.T_TERMINATE, tk.T_SUSPEND, tk.T_RESTART ]:
      block = front.block
      while block and not block.in_script:
         block = block.parent
      if block:
         stmt = common.script_jump_t()
         if front.tk == tk.T_SUSPEND:
            stmt.type = common.SCRIPT_JUMP_SUSPEND
         elif front.tk == tk.T_RESTART:
            stmt.type = common.SCRIPT_JUMP_RESTART
         front.block.stmts.append( stmt )
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'script-jump statement outside script' )
      tk.read( front )
      tk.test( front, tk.T_SEMICOLON )
      tk.read( front )
   elif front.tk == tk.T_RETURN:
      pos = front.tk_pos
      tk.read( front )
      expr = None
      if front.tk != tk.T_SEMICOLON:
         expr = f_expr.read( front, True )
      tk.test( front, tk.T_SEMICOLON )
      tk.read( front )
      if not front.func:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'return statement outside a function' )
      elif front.func.value and not expr:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'return statement missing return value' )
      elif expr and not front.func.value:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            expr.pos, 'returning value in void function' )
      else:
         stmt = common.return_t()
         stmt.expr = expr
         front.block.stmts.append( stmt )
   elif front.tk == tk.T_PALTRANS:
      read_paltrans( front )
   # goto label.
   elif front.tk == tk.T_ID and tk.peek( front ) == tk.T_COLON:
      label = None
      for prev in front.goto_labels:
         if prev.name == front.tk_text:
            label = prev
            break
      if label:
         if label.defined:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, 'duplicate label named \'%s\'', front.tk_text )
            diag( front, DIAG_FILE | DIAG_LINE | DIAG_COLUMN, label.pos,
               'label previously found here' )
            bail( front )
         else:
            label.defined = True
            label.pos = front.tk_pos
      else:
         label = common.label_t()
         label.name = front.tk_text
         label.defined = True
         label.pos = front.tk_pos
         front.goto_labels.append( label )
      front.block.stmts.append( label )
      tk.read( front )
      tk.read( front )
   elif front.tk == tk.T_GOTO:
      tk.read( front )
      tk.test( front, tk.T_ID )
      label = None
      for prev in front.goto_labels:
         if prev.name == front.tk_text:
            label = prev
            break
      if not label:
         label = common.label_t()
         label.name = front.tk_text
         label.pos = front.tk_pos
         front.goto_labels.append( label )
      tk.read( front )
      tk.test( front, tk.T_SEMICOLON )
      tk.read( front )
      stmt = common.goto_t()
      stmt.label = label
      front.block.stmts.append( stmt )
      stmt.next = label.stmts
      label.stmts = stmt
   else:
      if front.tk != tk.T_SEMICOLON:
         expr = f_expr.read( front, False )
         front.block.stmts.append( expr )
      tk.test( front, tk.T_SEMICOLON )
      tk.read( front )

def read_block( front ):
   tk.test( front, tk.T_BRACE_L )
   tk.read( front )
   while True:
      if f_dec.is_dec( front ):
         f_dec.read( front, f_dec.AREA_LOCAL )
      elif front.tk == tk.T_BRACE_R:
         tk.read( front )
         break
      else:
         read_stmt( front )
   # All goto statements need to refer to valid labels.
   if front.block.in_script:
      for label in front.goto_labels:
         if not label.defined:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               label.pos, 'label \'%s\' not found', label.name )
            bail( front )
      front.goto_labels = []