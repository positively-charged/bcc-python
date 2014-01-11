FORMAT_ZERO = 0
FORMAT_BIG_E = 1
FORMAT_LITTLE_E = 2

class options_t:
   def __init__( self ):
      self.format = FORMAT_LITTLE_E
      self.includes = []
      self.err_file = False
      self.source_file = ''
      self.object_file = 'object.o'
      self.encrypt_str = False

STORAGE_LOCAL = 0
STORAGE_MAP = 1
STORAGE_WORLD = 2
STORAGE_GLOBAL = 3

INITIAL_EXPR = 0
INITIAL_JUMP = 1

class initial_t:
   def __init__( self ):
      self.type = INITIAL_EXPR
      self.value = 0

class dim_t:
   def __init__( self ):
      self.size = 0
      self.element_size = 0

NODE_CONSTANT = 0
NODE_LITERAL = 1
NODE_UNARY = 2
NODE_BINARY = 3
NODE_CALL = 4
NODE_SUBSCRIPT = 5
NODE_EXPR = 6
NODE_VAR = 7
NODE_SCRIPT = 8
NODE_SCRIPT_JUMP = 9
NODE_FUNC = 10
NODE_IF = 11
NODE_JUMP = 12
NODE_WHILE = 13
NODE_RETURN = 14
NODE_FOR = 15
NODE_SWITCH = 16
NODE_CASE = 17
NODE_PARAM = 18
NODE_FORMAT_ITEM = 19
NODE_ASSIGN = 20    
NODE_LABEL = 21
NODE_GOTO = 22

class constant_t:
   def __init__( self ):
      self.node = NODE_CONSTANT
      self.value = 0
      self.pos = None

class literal_t:
   def __init__( self ):
      self.node = NODE_LITERAL
      self.value = 0

UOP_NONE = 0
UOP_MINUS = 1
UOP_LOG_NOT = 2
UOP_BIT_NOT = 3
UOP_PRE_INC = 4
UOP_PRE_DEC = 5
UOP_POST_INC = 6
UOP_POST_DEC = 6

class unary_t:
   def __init__( self ):
      self.node = NODE_UNARY
      self.op = UOP_NONE
      self.operand = None

BOP_NONE = 0
BOP_LOG_OR = 1
BOP_LOG_AND = 2
BOP_BIT_OR = 14
BOP_BIT_XOR = 15
BOP_BIT_AND = 16
BOP_EQ = 17
BOP_NEQ = 18
BOP_LT = 19
BOP_LTE = 20
BOP_GT = 21
BOP_GTE = 22
BOP_SHIFT_L = 23
BOP_SHIFT_R = 24
BOP_ADD = 25
BOP_SUB = 26
BOP_MUL = 27
BOP_DIV = 28
BOP_MOD = 29

class binary_t:
   def __init__( self ):
      self.node = NODE_BINARY
      self.op = BOP_NONE
      self.lside = None
      self.rside = None

AOP_NONE = 0
AOP_ADD = 1
AOP_SUB = 2
AOP_MUL = 3
AOP_DIV = 4
AOP_MOD = 5
AOP_SHIFT_L = 6
AOP_SHIFT_R = 7
AOP_BIT_AND = 8
AOP_BIT_XOR = 9
AOP_BIT_OR = 10

class assign_t:
   def __init__( self ):
      self.node = NODE_ASSIGN
      self.op = AOP_NONE
      self.lside = None
      self.rside = None

class call_t:
   def __init__( self ):
      self.node = NODE_CALL
      self.func = None
      self.args = []

class subscript_t:
   def __init__( self ):
      self.node = NODE_SUBSCRIPT
      self.operand = None
      self.index = None

class expr_t:
   def __init__( self ):
      self.node = NODE_EXPR
      self.pos = None
      self.folded = False
      self.is_value = False
      self.is_space = False
      self.value = 0
      self.array = None
      self.dim = -1

class var_t:
   def __init__( self ):
      self.node = NODE_VAR
      self.pos = None
      self.name = ''
      self.dim = None
      self.storage = STORAGE_LOCAL
      self.index = 0
      self.size = 0
      self.initial = None

SCRIPT_TYPE_CLOSED = 0
SCRIPT_TYPE_OPEN = 1
SCRIPT_TYPE_RESPAWN = 2
SCRIPT_TYPE_DEATH = 3
SCRIPT_TYPE_ENTER = 4
SCRIPT_TYPE_PICKUP = 5
SCRIPT_TYPE_BLUE_RETURN = 6
SCRIPT_TYPE_RED_RETURN = 7
SCRIPT_TYPE_WHITE_RETURN = 8
SCRIPT_TYPE_LIGHTNING = 9
SCRIPT_TYPE_UNLOADING = 10
SCRIPT_TYPE_DISCONNECT = 11
SCRIPT_TYPE_RETURN = 12

SCRIPT_FLAG_NET = 1
SCRIPT_FLAG_CLIENTSIDE = 2

class script_t:
   def __init__( self ):
      self.node = NODE_SCRIPT
      self.pos = None
      self.number = 0
      self.num_param = 0
      self.type = SCRIPT_TYPE_CLOSED
      self.flags = 0
      self.offset = 0
      self.body = None
      self.size = 0

FLOW_GOING = 0
FLOW_DEAD = 1
FLOW_JUMP = 2

class block_t:
   def __init__( self ):
      self.in_script = False
      self.in_loop = False
      self.in_switch = False
      self.stmts = []
      self.flow = FLOW_GOING
      self.parent = None

JUMP_BREAK = 0
JUMP_CONTINUE = 1

class jump_t:
   def __init__( self ):
      self.node = NODE_JUMP
      self.type = JUMP_BREAK

SCRIPT_JUMP_TERMINATE = 0
SCRIPT_JUMP_SUSPEND = 1
SCRIPT_JUMP_RESTART = 2

class script_jump_t:
   def __init__( self ):
      self.node = NODE_SCRIPT_JUMP
      self.type = SCRIPT_JUMP_TERMINATE

class return_t:
   def __init__( self ):
      self.node = NODE_RETURN
      self.expr = None

FUNC_ASPEC = 0
FUNC_EXT = 1
FUNC_DED = 2
FUNC_FORMAT = 3
FUNC_USER = 4
FUNC_INTERNAL = 4

class func_t:
   def __init__( self ):
      self.node = NODE_FUNC
      self.pos = None
      self.type = FUNC_USER
      # Returns value or not.
      self.value = False
      self.name = ''
      self.min_param = 0
      self.max_param = 0
      self.impl = {}

FCAST_ARRAY = 0
FCAST_BINARY = 1
FCAST_CHAR = 2
FCAST_DECIMAL = 3
FCAST_FIXED = 4
FCAST_KEY = 5
FCAST_LOCAL_STRING = 6
FCAST_NAME = 7
FCAST_STRING = 8
FCAST_HEX = 9

class format_item_t:
   def __init__( self ):
      self.node = NODE_FORMAT_ITEM
      self.cast = FCAST_ARRAY
      self.expr = None

class if_t:
   def __init__( self ):
      self.node = NODE_IF
      self.cond = None
      self.body = None
      self.else_body = None

WHILE_WHILE = 0
WHILE_UNTIL = 1
WHILE_DO_WHILE = 2
WHILE_DO_UNTIL = 3

class while_t:
   def __init__( self ):
      self.node = NODE_WHILE
      self.type = WHILE_WHILE
      self.cond = None
      self.body = None

class for_t:
   def __init__( self ):
      self.node = NODE_FOR
      self.init = None
      self.cond = None
      self.post = None
      self.body = None

class switch_t:
   def __init__( self ):
      self.node = NODE_SWITCH
      self.cond = None
      self.cases = []
      self.cases_sorted = []
      self.default_case = None
      self.body = None

class case_t:
   def __init__( self ):
      self.node = NODE_CASE
      self.expr = None
      self.pos = None

class label_t:
   def __init__( self ):
      self.node = NODE_LABEL
      self.name = ''
      self.pos = None
      self.defined = False
      self.stmts = None
      self.obj_pos = 0

class goto_t:
   def __init__( self ):
      self.node = NODE_GOTO
      self.label = None
      # Linked list of goto statements that refer to the same label.
      self.next = None
      self.obj_pos = 0

class module_t:
   def __init__( self ):
      self.name = ''
      self.vars = []
      self.arrays = []
      self.scripts = []
      self.funcs = []
      self.imports = []

class struct_t:
   def __init__( self ):
      self.node = NODE_STRUCT
      self.members = []
      self.offset_int = 0
      self.offset_str = 0
      self.size = 0