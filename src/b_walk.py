import common
import b_pcode as pcode
import b_pcode as obj

class result_t:
   def __init__( self ):
      self.push = False
      self.pushed = False
      self.index = 0
      self.storage = common.STORAGE_LOCAL
      self.dim = 0
      self.dims = None
      self.is_array = False

def do_block( back, block ):
   for object in block.stmts:
      if object.node == common.NODE_EXPR:
         do_expr( back, object, False )
      elif object.node == common.NODE_IF:
         do_if( back, object )
      elif object.node == common.NODE_WHILE:
         do_while( back, object )
      elif object.node == common.NODE_FOR:
         do_for( back, object )
      elif object.node == common.NODE_LABEL:
         object.obj_pos = obj.tell( back )
         stmt = object.stmts
         while stmt:
            if stmt.obj_pos:
               obj.seek( back, stmt.obj_pos )
               obj.add_opc( back, obj.PC_GOTO )
               obj.add_arg( back, object.obj_pos )
            stmt = stmt.next
         obj.seek( back )
      elif object.node == common.NODE_GOTO:
         if object.label.obj_pos:
            obj.add_opc( back, obj.PC_GOTO )
            obj.add_arg( back, object.label.obj_pos )
         else:
            object.obj_pos = obj.tell( back )
            obj.add_opc( back, obj.PC_GOTO )
            obj.add_arg( back, 0 )

def do_expr( back, expr, push ):
   result = result_t()
   result.push = push
   do_operand( back, result, expr.root )
   if not push and result.pushed:
      obj.add_opc( back, obj.PC_DROP )

def do_operand( back, result, object ):
   if object.node == common.NODE_CALL:
      do_call( back, result, object )
   elif object.node == common.NODE_LITERAL:
      obj.add_opc( back, obj.PC_PUSH_NUMBER )
      obj.add_arg( back, object.value )
      result.pushed = True
      # Strings in a library need to be tagged.
      if back.module.name and object.is_str:
         pcode.add( back, pcode.PC_TAG_STRING )

def do_call( back, result, call ):
   func = call.func
   if func.type == common.FUNC_ASPEC:
      i = 0
      while i < len( call.args ):
         do_expr( back, call.args[ i ], True )
         i += 1
      if i:
         codes = [
            pcode.PC_LSPEC1,
            pcode.PC_LSPEC2,
            pcode.PC_LSPEC3,
            pcode.PC_LSPEC4,
            pcode.PC_LSPEC5 ]
         pcode.add( back, codes[ i - 1 ], func.impl[ 'id' ] )
      else:
         pcode.add( back, pcode.PC_PUSH_NUMBER, 0 )
         pcode.add( back, pcode.PC_LSPEC1, func.impl[ 'id' ] )
   elif func.type == common.FUNC_FORMAT:
      obj.add_opc( back, obj.PC_BEGIN_PRINT )
      i = 0
      # Format-list argument.
      while i < len( call.args ):
         item = call.args[ i ]
         if item.node == common.NODE_FORMAT_ITEM:
            if item.cast == common.FCAST_ARRAY:
               pass
            else:
               casts = [
                  0,
                  obj.PC_PRINT_BINARY,
                  obj.PC_PRINT_CHARACTER,
                  obj.PC_PRINT_NUMBER,
                  obj.PC_PRINT_FIXED,
                  obj.PC_PRINT_BIND,
                  obj.PC_PRINT_LOCALIZED,
                  obj.PC_PRINT_NAME,
                  obj.PC_PRINT_STRING,
                  obj.PC_PRINT_HEX ]
               do_expr( back, item.expr, True )
               obj.add_opc( back, casts[ item.cast ] )
            i += 1
         else:
            break
      # Other arguments.
      if func.max_param > 1:
         obj.add_opc( back, obj.PC_MORE_HUD_MESSAGE )
         param = 1
         while i < len( call.args ):
            if param == func.min_params:
               obj.add_opc( back, obj.PC_OPT_HUD_MESSAGE )
            do_expr( back, call.args[ i ], True )
            param += 1
            i += 1
      obj.add_opc( back, func.impl[ 'opcode' ] )
   elif func.type == common.FUNC_EXT:
      for arg in call.args:
         do_expr( back, arg, True )
      pcode.add( back, pcode.PC_CALL_FUNC, len( call.args ),
         func.impl[ 'id' ] )
      if func.value:
         result.pushed = True
   elif func.type == common.FUNC_DED:
      for arg in call.args:
         do_expr( back, arg, True )
      obj.add_opc( back, func.impl[ 'opcode' ] )
   elif func.type == common.FUNC_USER:
      for arg in call.args:
         do_expr( back, arg, True )
      if func.value:
         pcode.add( back, pcode.PC_CALL, func.impl[ 'index' ] )
         result.pushed = True
      else:
         pcode.add( back, pcode.PC_CALL_DISCARD, func.impl[ 'index' ] )
   elif func.type == common.FUNC_INTERNAL:
      pass

def do_if( back, stmt ):
   do_expr( back, stmt.cond, True )
   cond = obj.tell( back )
   obj.add_opc( back, obj.PC_IF_NOT_GOTO )
   obj.add_arg( back, 0 )
   do_block( back, stmt.body )
   finish = obj.tell( back )
   obj.seek( back, cond )
   obj.add_opc( back, obj.PC_IF_NOT_GOTO )
   obj.add_arg( back, finish )
   obj.seek( back )

def do_while( back, stmt ):
   jump = 0
   if stmt.type == common.WHILE_WHILE or \
      stmt.type == common.WHILE_UNTIL:
      jump = obj.tell( back )
      obj.add_opc( back, obj.PC_GOTO )
      obj.add_arg( back, 0 )
   body = obj.tell( back )
   do_block( back, stmt.body )
   cond = obj.tell( back )
   # Optimization: If the loop condition is true, it is not needed.
   if stmt.cond.folded:
      if stmt.type == common.WHILE_WHILE or \
         stmt.type == common.WHILE_DO_WHILE:
         if stmt.cond.value:
            obj.add_opc( back, obj.PC_GOTO )
            obj.add_arg( back, body )
      else:
         if not stmt.cond.value:
            obj.add_opc( back, obj.PC_GOTO )
            obj.add_arg( back, body )
   else:
      do_expr( back, stmt.cond, True )
      if stmt.type == common.WHILE_WHILE or \
         stmt.type == common.WHILE_DO_WHILE:
         obj.add_opc( back, obj.PC_IF_GOTO )
      else:
         obj.add_opc( back, obj.PC_IF_NOT_GOTO )
      obj.add_arg( back, body )
   if stmt.type == common.WHILE_WHILE or \
      stmt.type == common.WHILE_UNTIL:
      obj.seek( back, jump )
      obj.add_opc( back, obj.PC_GOTO )
      obj.add_arg( back, cond )
      obj.seek( back )

def do_for( back, stmt ):
   if stmt.init:
      for object in stmt.init:
         if object.node == common.NODE_EXPR:
            do_expr( back, object, False )
         else:
            pass
   jump = obj.tell( back )
   obj.add_opc( back, obj.PC_GOTO )
   obj.add_arg( back, 0 )
   body = obj.tell( back )
   do_block( back, stmt.body )
   if stmt.post:
      for object in stmt.post:
         do_expr( back, object, False )
   cond = obj.tell( back )
   if stmt.cond:
      do_expr( back, stmt.cond, True )
      obj.add_opc( back, obj.PC_IF_GOTO )
      obj.add_arg( back, body )
   else:
      obj.add_opc( back, obj.PC_GOTO )
      obj.add_arg( back, body )
   obj.seek( back, jump )
   obj.add_opc( back, obj.PC_GOTO )
   obj.add_arg( back, cond )
   obj.seek( back )