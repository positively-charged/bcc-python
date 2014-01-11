import math

import common
import f_main
from f_main import ( bail, diag, DIAG_COLUMN, DIAG_ERR, DIAG_FILE, DIAG_LINE )
import f_token as tk

def read( front, usable ):
   expr = read_op( front )
   if usable and not expr.is_value:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, expr.pos,
      'expression does not produce a usable value' )
      bail( front )
   return expr

def read_op( front ):
   add = None
   add_op = 0
   add_pos = None
   shift = None
   shift_op = 0
   shift_pos = None
   lt = None
   lt_op = 0
   lt_pos = None
   eq = None
   eq_op = 0
   eq_pos = None
   bit_and = None
   bit_and_pos = None
   bit_xor = None
   bit_xor_pos = None
   bit_or = None
   bit_or_pos = None
   log_and = None
   log_and_pos = None
   log_or = None
   log_or_pos = None
   op = 0
   while True:
      operand = read_operand( front )
      while True:
         op = 0
         if front.tk == tk.T_STAR:
            op = common.BOP_MUL
         elif front.tk == tk.T_SLASH:
            op = common.BOP_DIV
         elif front.tk == tk.T_MOD:
            op = common.BOP_MOD
         else:
            break
         pos = front.tk_pos
         tk.read( front )
         rside = read_operand( front )
         add_binary( front, operand, op, pos, rside )

      if add:
         add_binary( front, add, add_op, add_pos, operand )
         operand = add
         add = None
      if front.tk == tk.T_PLUS:
         op = common.BOP_ADD
      elif front.tk == tk.T_MINUS:
         op = common.BOP_SUB
      if op:
         add = operand
         add_op = op
         add_pos = front.tk_pos
         tk.read( front )
         continue

      if shift:
         add_binary( front, shift, shift_op, shift_pos, operand )
         operand = shift
         shift = None
      if front.tk == tk.T_SHIFT_L:
         op = common.BOP_SHIFT_L
      elif front.tk == tk.T_SHIFT_R:
         op = common.BOP_SHIFT_R
      if op:
         shift = operand
         shift_op = op
         shift_pos = front.tk_pos
         tk.read( front )
         continue

      if lt:
         add_binary( front, lt, lt_op, lt_pos, operand )
         operand = lt
         lt = None
      if front.tk == tk.T_LT:
         op = common.BOP_LT
      elif front.tk == tk.T_LTE:
         op = common.BOP_LTE
      elif front.tk == tk.T_GT:
         op = common.BOP_GT
      elif front.tk == tk.T_GTE:
         op = common.BOP_GTE
      if op:
         lt = operand
         lt_op = op
         lt_pos = front.tk_pos
         tk.read( front )
         continue

      if eq:
         add_binary( front, eq, eq_op, eq_pos, operand )
         operand = eq
         eq = None
      if front.tk == tk.T_EQ:
         op = common.BOP_EQ
      elif front.tk == tk.T_NEQ:
         op = common.BOP_NEQ
      if op:
         eq = operand
         eq_op = op
         eq_pos = front.tk_pos
         tk.read( front )
         continue

      if bit_and:
         add_binary( front, bit_and, common.BOP_BIT_AND, bit_and_pos,
            operand )
         operand = bit_and
         bit_and = None
      if front.tk == tk.T_BIT_AND:
         bit_and = operand
         bit_and_pos = front.tk_pos
         tk.read( front )
         continue

      if bit_xor:
         add_binary( front, bit_xor, common.BOP_BIT_XOR, bit_xor_pos,
            operand )
         operand = bit_xor
         bit_xor = None
      if front.tk == tk.T_BIT_XOR:
         bit_xor = operand
         bit_xor_pos = front.tk_pos
         tk.read( front )
         continue

      if bit_or:
         add_binary( front, bit_or, common.BOP_BIT_OR, bit_or_pos,
            operand )
         operand = bit_or
         bit_or = None
      if front.tk == tk.T_BIT_OR:
         bit_or = operand
         bit_or_pos = front.tk_pos
         tk.read( front )
         continue

      if log_and:
         add_binary( front, log_and, common.BOP_LOG_AND, log_and_pos,
            operand )
         operand = log_and
         log_and = None
      if front.tk == tk.T_LOG_AND:
         log_and = operand
         log_and_pos = front.tk_pos
         tk.read( front )
         continue

      if log_or:
         add_binary( front, log_or, common.BOP_LOG_OR, log_or_pos,
            operand )
         operand = log_or
         log_or = None
      if front.tk == tk.T_LOG_OR:
         log_or = operand
         log_or_pos = front.tk_pos
         tk.read( front )
         continue

      break
   return operand

def read_operand( front ):
   # Prefix operations.
   ops = {
      tk.T_INC : common.UOP_PRE_INC,
      tk.T_DEC : common.UOP_PRE_DEC,
      tk.T_MINUS : common.UOP_MINUS,
      tk.T_LOG_NOT : common.UOP_LOG_NOT,
      tk.T_BIT_NOT : common.UOP_BIT_NOT }
   if front.tk in ops:
      op = ops[ front.tk ]
      tk.read( front )
      pos = front.tk_pos
      expr = read_operand( front )
      if op == common.UOP_PRE_INC or op == common.UOP_PRE_DEC:
         # Only an l-value can be incremented.
         if expr.is_space:
            add_unary( expr, op )
            expr.is_space = False
         else:
            action = 'incremented'
            if op == common.UOP_PRE_DEC:
               action = 'decremented'
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
               'operand cannot be %s', action )
            bail( front )
      else:
         # Remaining operations require a value to work on.
         if expr.is_value:
            add_unary( expr, op )
            expr.is_space = False
         else:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
               'operand cannot be used in unary operation' )
            bail( front )
   else:
      expr = common.expr_t()
      expr.pos = front.tk_pos
      read_primary( front, expr )
      read_postfix( front, expr )
   return expr

def add_unary( expr, op ):
   unary = common.unary_t()
   unary.op = op
   unary.operand = expr.root
   expr.root = unary
   if expr.folded:
      if op == common.UOP_MINUS:
         expr.value = ( - expr.value )
      elif op == common.UOP_LOG_NOT:
         expr.value = ( not expr.value )
      elif op == common.UOP_BIT_NOT:
         expr.value = ( ~ expr.value )
      else:
         expr.folded = False

def read_primary( front, expr ):
   if front.tk == tk.T_ID:
      expr.folded = False
      object = f_main.find_name( front, front.tk_text )
      if object:
         expr.root = object
         tk.read( front )
         if object.node == common.NODE_CONSTANT:
            expr.value = object.value
            expr.folded = True
            expr.is_value = True
         elif object.node == common.NODE_VAR:
            expr.is_value = True
            if object.dim:
               expr.array = object
               expr.dim = 0
            else:
               expr.is_space = True
         else:
            expr.root = object
      # User functions can be used before declared.
      elif tk.peek( front ) == tk.T_PAREN_L:
         pass
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'undefined object used: %s', front.tk_text )
         bail( front )
   elif front.tk == tk.T_PAREN_L:
      tk.read( front )
      expr = read_op( front )
      tk.test( front, tk.T_PAREN_R )
      tk.read( front )
   else:
      is_str = False
      if front.tk == tk.T_LIT_STRING:
         is_str = True
      literal = common.literal_t()
      literal.is_str = is_str
      literal.value = read_literal( front )
      expr.root = literal
      expr.value = literal.value
      expr.folded = True
      expr.is_value = True

def read_literal( front ):
   value = 0
   if front.tk == tk.T_LIT_DECIMAL:
      value = int( front.tk_text )
      tk.read( front )
   elif front.tk == tk.T_LIT_OCTAL:
      value = int( front.tk_text, 8 )
      tk.read( front )
   elif front.tk == tk.T_LIT_HEX:
      value = int( front.tk_text, 16 )
      tk.read( front )
   elif front.tk == tk.T_LIT_FIXED:
      num = float( front.tk_text )
      value = (
         # Whole.
         ( int( num ) << 16 ) +
         # Fraction.
         ( int( ( 1 << 16 ) * ( num - math.floor( num ) ) ) ) )
      tk.read( front )
   elif front.tk == tk.T_LIT_CHAR:
      value = ord( front.tk_text )
      tk.read( front )
   elif front.tk == tk.T_LIT_STRING:
      try:
         value = front.str_table.index( front.tk_text )
         tk.read( front )
      except ValueError:
         front.str_table.append( front.tk_text )
         value = len( front.str_table ) - 1
         tk.read( front )
   else:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'missing literal value' )
      bail( front )
   return value

def read_postfix( front, expr ):
   while True:
      if front.tk == tk.T_BRACKET_L:
         if not expr.array or expr.dim == len( expr.array.dim ):
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, 'accessing something not an array' )
            bail( front )
         tk.read( front )
         index = read( front, true )
         tk.test( front, tk.T_BRACKET_R )
         tk.read( front )
         sub = common.subscript_t()
         sub.operand = expr.root
         sub.index = index
         expr.root = sub
         expr.dim += 1
         if expr.dim == len( expr.array.dim ):
            expr.is_value = True
            expr.is_space = True
            expr.array = None
         else:
            expr.is_value = False
            expr.is_space = False
      elif front.tk == tk.T_INC or front.tk == tk.T_DEC:
         if expr.is_space:
            op = common.UOP_POST_INC
            if front.tk == tk.T_DEC:
               op = common.UOP_POST_DEC
            tk.read( front )
            add_unary( expr, op )
            expr.is_space = False
         else:
            action = 'incremented'
            if front.tk == tk.T_DEC:
               action = 'decremented'
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, 'operand to the left cannot be %s', action )
            bail( front )
      elif ( front.tk == tk.T_PAREN_L and
         # When reading the script number, the left parenthesis of the
         # parameter list can be mistaken for a function call. Avoid function
         # calls in this situation.
         not front.reading_script_number ):
         read_call( front, expr )
      else:
         break

def read_call( front, expr ):
   pos = front.tk_pos
   tk.test( front, tk.T_PAREN_L )
   tk.read( front )
   func = expr.root
   if func.node != common.NODE_FUNC:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
         'calling something not a function' )
      bail( front )
   # Call to a latent function cannot appear in a function.
   elif func.type == common.FUNC_DED and func.impl[ 'latent' ] and \
      front.func:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
         'latent function called inside function' )
      bail( front )
   call = common.call_t()
   call.func = func
   args = 0
   if front.tk == tk.T_ID and tk.peek( front ) == tk.T_COLON:
      if func.type != common.FUNC_FORMAT:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'format-list argument given to non-format function' )
         bail( front )
      while True:
         tk.test( front, tk.T_ID )
         item = common.format_item_t()
         casts = {
            'a' : common.FCAST_ARRAY,
            'b' : common.FCAST_BINARY,
            'c' : common.FCAST_CHAR,
            'd' : common.FCAST_DECIMAL,
            'f' : common.FCAST_FIXED,
            'i' : common.FCAST_DECIMAL,
            'k' : common.FCAST_KEY,
            'l' : common.FCAST_LOCAL_STRING,
            'n' : common.FCAST_NAME,
            's' : common.FCAST_STRING,
            'x' : common.FCAST_HEX }
         if front.tk_text in casts:
            item.cast = casts[ front.tk_text ]
            tk.read( front )
         else:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, 'unknown format cast: %s', front.tk_text )
            bail( front )
         tk.test( front, tk.T_COLON )
         tk.read( front )
         if item.cast == common.FCAST_ARRAY:
            arg = read( front, False )
            if not arg.array:
               diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
                  arg.pos, 'argument not an array' )
               bail( front )
            elif arg.dim != len( arg.array.dim ) - 1:
               diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
                  arg.pos, 'array argument not of a single dimension' )
               bail( front )
            item.expr = arg
         else:
            item.expr = read( front, True )
         call.args.append( item )
         if front.tk == tk.T_COMMA:
            tk.read( front )
         else:
            break
      # All format items count as a single argument.
      args += 1
      if front.tk == tk.T_SEMICOLON:
         tk.read( front )
         while True:
            call.args.append( read( front, True ) )
            args += 1
            if front.tk == tk.T_COMMA:
               tk.read( front )
            else:
               break
   else:
      if func.type == common.FUNC_FORMAT:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'missing format-list argument' )
         bail( front )
      # This relic is not necessary in new code. The compiler is smart enough
      # to figure out when to use the constant version of a pcode.
      if front.tk == tk.T_CONST:
         tk.read( front )
         tk.test( front, tk.T_COLON )
         tk.read( front )
      update_params = False
      if func.type == common.FUNC_USER and not func.impl[ 'def_params' ]:
         func.impl[ 'def_params' ] = True
         update_params = True
      if front.tk != tk.T_PAREN_R:
         while True:
            call.args.append( read( front, True ) )
            args += 1
            if update_params:
               func.min_param += 1
               func.max_param += 1
            if front.tk == tk.T_COMMA:
               tk.read( front )
            else:
               break
   if args < func.min_param or args > func.max_param:
      required = func.min_param
      if args > func.max_param:
         required = func.max_param
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         pos, 'function expects %d argument%s but %d given', required,
         '' if required == 1 else 's', args )
      bail( front )
   tk.test( front, tk.T_PAREN_R )
   tk.read( front )
   expr.root = call
   expr.func = None
   if func.value:
      expr.is_value = True
            