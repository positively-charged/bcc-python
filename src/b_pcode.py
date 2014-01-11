import struct

PC_NONE = 0
PC_TERMINATE = 1
PC_SUSPEND = 2
PC_PUSH_NUMBER = 3
PC_LSPEC1 = 4
PC_LSPEC2 = 5
PC_LSPEC3 = 6
PC_LSPEC4 = 7
PC_LSPEC5 = 8
PC_LSPEC1_DIRECT = 9
PC_LSPEC2_DIRECT = 10
PC_LSPEC3_DIRECT = 11
PC_LSPEC4_DIRECT = 12
PC_LSPEC5_DIRECT = 13
PC_ADD = 14
PC_SUB = 15
PC_MUL = 16
PC_DIV = 17
PC_MOD = 18
PC_EQ = 19
PC_NE = 20
PC_LT = 21
PC_GT = 22
PC_LE = 23
PC_GE = 24
PC_ASSIGN_SCRIPT_VAR = 25
PC_ASSIGN_MAP_VAR = 26
PC_ASSIGN_WORLD = 27
PC_PUSH_SCRIPT_VAR = 28
PC_PUSH_MAP_VAR = 29
PC_PUSH_WORLD_VAR = 30
PC_ADD_SCRIPT_VAR = 31
PC_ADD_MAP_VAR = 32
PC_ADD_WORLD_VAR = 33
PC_SUB_SCRIPT_VAR = 34
PC_SUB_MAP_VAR = 35
PC_SUB_WORLD_VAR = 36
PC_MUL_SCRIPT_VAR = 37
PC_MUL_MAP_VAR = 38
PC_MUL_WORLD_VAR = 39
PC_DIV_SCRIPT_VAR = 40
PC_DIV_MAP_VAR = 41
PC_DIV_WORLD_VAR = 42
PC_MOD_SCRIPT_VAR = 43
PC_MOD_MAP_VAR = 44
PC_MOD_WORLD_VAR = 45
PC_INC_SCRIPT_VAR = 46
PC_INC_MAP_VAR = 47
PC_INC_WORLD_VAR = 48
PC_DEC_SCRIPT_VAR = 49
PC_DEC_MAP_VAR = 50
PC_DEC_WORLD_VAR = 51
PC_GOTO = 52
PC_IF_GOTO = 53
PC_DROP = 54  # POP STACK.
PC_DELAY = 55
PC_DELAY_DIRECT = 56
PC_RANDOM = 57
PC_RANDOM_DIRECT = 58
PC_THING_COUNT = 59
PC_THING_COUNT_DIRECT = 60
PC_TAG_WAIT = 61
PC_TAG_WAIT_DIRECT = 62
PC_POLY_WAIT = 63
PC_POLY_WAIT_DIRECT = 64
PC_CHANGE_FLOOR = 65
PC_CHANGE_FLOOR_DIRECT = 66
PC_CHANGE_CEILING = 67
PC_CHANGE_CEILING_DIRECT = 68
PC_RESTART = 69
PC_AND_LOGICAL = 70
PC_OR_LOGICAL = 71
PC_AND_BITWISE = 72
PC_OR_BITWISE = 73
PC_EOR_BITWISE = 74
PC_NEGATE_LOGICAL = 75
PC_LSHIFT = 76
PC_RSHIFT = 77
PC_UNARY_MINUS = 78
PC_IF_NOT_GOTO = 79
PC_LINE_SIDE = 80
PC_SCRIPT_WAIT = 81
PC_SCRIPT_WAIT_DIRECT = 82
PC_CLEAR_LINE_SPECIAL = 83
PC_CASE_GOTO = 84
PC_BEGIN_PRINT = 85
PC_END_PRINT = 86
PC_PRINT_STRING = 87
PC_PRINT_NUMBER = 88
PC_PRINT_CHARACTER = 89
PC_PLAYER_COUNT = 90
PC_GAME_TYPE = 91
PC_GAME_SKILL = 92
PC_TIMER = 93
PC_SECTOR_SOUND = 94
PC_AMBIENT_SOUND = 95
PC_SOUND_SEQUENCE = 96
PC_SET_LINE_TEXTURE = 97
PC_SET_LINE_BLOCKING = 98
PC_SET_LINE_SPECIAL = 99
PC_THING_SOUND = 100
PC_END_PRINT_BOLD = 101
PC_ACTIVATOR_SOUND = 102
PC_LOCAL_AMBIENT_SOUND = 103
PC_SET_LINE_MONSTER_BLOCKING = 104
PC_PLAYER_BLUE_SKULL = 105
PC_PLAYER_RED_SKULL = 106
PC_PLAYER_YELLOW_SKULL = 107
PC_PLAYER_MASTER_SKULL = 108
PC_PLAYER_BLUE_CARD = 109
PC_PLAYER_RED_CARD = 110
PC_PLAYER_YELLOW_CARD = 111
PC_PLAYER_MASTER_CARD = 112
PC_PLAYER_BLACK_SKULL = 113
PC_PLAYER_SILVER_SKULL = 114
PC_PLAYER_GOLD_SKULL = 115
PC_PLAYER_BLACK_CARD = 116
PC_PLAYER_SILVER_CARD = 117
PC_IS_MULTIPLAYER = 118
PC_PLAYER_TEAM = 119
PC_PLAYER_HEALTH = 120
PC_PLAYER_ARMOR_POINTS = 121
PC_PLAYER_FRAGS = 122
PC_PLAYER_EXPERT = 123
PC_BLUE_TEAM_COUNT = 124
PC_RED_TEAM_COUNT = 125
PC_BLUE_TEAM_SCORE = 126
PC_RED_TEAM_SCORE = 127
PC_IS_ONE_FLAG_CTF = 128
PC_GET_INVASION_WAVE = 129
PC_GET_INVASION_STATE = 130
PC_PRINT_NAME = 131
PC_MUSIC_CHANGE = 132
PC_CONSOLE_COMMAND_DIRECT = 133
PC_CONSOLE_COMMAND = 134
PC_SINGLE_PLAYER = 135
PC_FIXED_MUL = 136
PC_FIXED_DIV = 137
PC_SET_GRAVITY = 138
PC_GRAVITY_DIRECT = 139
PC_SET_AIR_CONTROL = 140
PC_SET_AIR_CONTROL_DIRECT = 141
PC_CLEAR_INVENTORY = 142
PC_GIVE_INVENTORY = 143
PC_GIVE_INVENTORY_DIRECT = 144
PC_TAKE_INVENTORY = 145
PC_TAKE_INVENTORY_DIRECT = 146
PC_CHECK_INVENTORY = 147
PC_CHECK_INVENTORY_DIRECT = 148
PC_SPAWN = 149
PC_SPAWN_DIRECT = 150
PC_SPAWN_SPOT = 151
PC_SPAWN_SPOT_DIRECT = 152
PC_SET_MUSIC = 153
PC_SET_MUSIC_DIRECT = 154
PC_LOCAL_SET_MUSIC = 155
PC_LOCAL_SET_MUSIC_DIRECT = 156
PC_PRINT_FIXED = 157
PC_PRINT_LOCALIZED = 158
PC_MORE_HUD_MESSAGE = 159
PC_OPT_HUD_MESSAGE = 160
PC_END_HUD_MESSAGE = 161
PC_END_HUD_MESSAGE_BOLD = 162
PC_SET_STYLE = 163
PC_SET_STYLE_DIRECT = 164
PC_SET_FONT = 165
PC_SET_FONT_DIRECT = 166
PC_PUSH_BYTE = 167
PC_LSPEC1_DIRECT_B = 168
PC_LSPEC2_DIRECT_B = 169
PC_LSPEC3_DIRECT_B = 170
PC_LSPEC4_DIRECT_B = 171
PC_LSPEC5_DIRECT_B = 172
PC_DELAY_DIRECT_B = 173
PC_RANDOM_DIRECT_B = 174
PC_PUSH_BYTES = 175
PC_PUSH_2BYTES = 176
PC_PUSH_3BYTES = 177
PC_PUSH_4BYTES = 178
PC_PUSH_5BYTES = 179
PC_SET_THING_SPECIAL = 180
PC_ASSIGN_GLOBAL_VAR = 181
PC_PUSH_GLOBAL_VAR = 182
PC_ADD_GLOBAL_VAR = 183
PC_SUB_GLOBAL_VAR = 184
PC_MUL_GLOBAL_VAR = 185
PC_DIV_GLOBAL_VAR = 186
PC_MOD_GLOBAL_VAR = 187
PC_INC_GLOBAL_VAR = 188
PC_DEC_GLOBAL_VAR = 189
PC_FADE_TO = 190
PC_FADE_RANGE = 191
PC_CANCEL_FADE = 192
PC_PLAY_MOVIE = 193
PC_SET_FLOOR_TRIGGER = 194
PC_SET_CEILING_TRIGGER = 195
PC_GET_ACTOR_X = 196
PC_GET_ACTOR_Y = 197
PC_GET_ACTOR_Z = 198
PC_START_TRANSLATION = 199
PC_TRANSLATION_RANGE1 = 200
PC_TRANSLATION_RANGE2 = 201
PC_END_TRANSLATION = 202
PC_CALL = 203
PC_CALL_DISCARD = 204
PC_RETURN_VOID = 205
PC_RETURN_VAL = 206
PC_PUSH_MAP_ARRAY = 207
PC_ASSIGN_MAP_ARRAY = 208
PC_ADD_MAP_ARRAY = 209
PC_SUB_MAP_ARRAY = 210
PC_MUL_MAP_ARRAY = 211
PC_DIV_MAP_ARRAY = 212
PC_MOD_MAP_ARRAY = 213
PC_INC_MAP_ARRAY = 214
PC_DEC_MAP_ARRAY = 215
PC_DUP = 216
PC_SWAP = 217
PC_WRITE_TO_INI = 218
PC_GET_FROM_INI = 219
PC_SIN = 220
PC_COS = 221
PC_VECTOR_ANGLE = 222
PC_CHECK_WEAPON = 223
PC_SET_WEAPON = 224
PC_TAG_STRING = 225
PC_PUSH_WORLD_ARRAY = 226
PC_ASSIGN_WORLD_ARRAY = 227
PC_ADD_WORLD_ARRAY = 228
PC_SUB_WORLD_ARRAY = 229
PC_MUL_WORLD_ARRAY = 230
PC_DIV_WORLD_ARRAY = 231
PC_MOD_WORLD_ARRAY = 232
PC_INC_WORLD_ARRAY = 233
PC_DEC_WORLD_ARRAY = 234
PC_PUSH_GLOBAL_ARRAY = 235
PC_ASSIGN_GLOBAL_ARRAY = 236
PC_ADD_GLOBAL_ARRAY = 237
PC_SUB_GLOBAL_ARRAY = 238
PC_MUL_GLOBAL_ARRAY = 239
PC_DIV_GLOBAL_ARRAY = 240
PC_MOD_GLOBAL_ARRAY = 241
PC_INC_GLOBAL_ARRAY = 242
PC_DEC_GLOBAL_ARRAY = 243
PC_SET_MARINE_WEAPON = 244
PC_SET_ACTOR_PROPERTY = 245
PC_GET_ACTOR_PROPERTY = 246
PC_PLAYER_NUMBER = 247
PC_ACTIVATOR_TID = 248
PC_SET_MARINE_SPRITE = 249
PC_GET_SCREEN_WIDTH = 250
PC_GET_SCREEN_HEIGHT = 251
PC_THING_PROJECTILE2 = 252
PC_STRLEN = 253
PC_SET_HUD_SIZE = 254
PC_GET_CVAR = 255
PC_CASE_GOTO_SORTED = 256
PC_SET_RESULT_VALUE = 257
PC_GET_LINE_ROW_OFFSET = 258
PC_GET_ACTOR_FLOOR_Z = 259
PC_GET_ACTOR_ANGLE = 260
PC_GET_SECTOR_FLOOR_Z = 261
PC_GET_SECTOR_CEILING_Z = 262
PC_LSPEC5_RESULT = 263
PC_GET_SIGIL_PIECES = 264
PC_GET_LEVEL_INFO = 265
PC_CHANGE_SKY = 266
PC_PLAYER_IN_GAME = 267
PC_PLAYER_IS_BOT = 268
PC_SET_CAMERA_TO_TEXTURE = 269
PC_END_LOG = 270
PC_GET_AMMO_CAPACITY = 271
PC_SET_AMMO_CAPACITY = 272
PC_PRINT_MAP_CHAR_ARRAY = 273
PC_PRINT_WORLD_CHAR_ARRAY = 274
PC_PRINT_GLOBAL_CHAR_ARRAY = 275
PC_SET_ACTOR_ANGLE = 276
PC_GRAP_INPUT = 277
PC_SET_MOUSE_POINTER = 278
PC_MOVE_MOUSE_POINTER = 279
PC_SPAWN_PROJECTILE = 280
PC_GET_SECTOR_LIGHT_LEVEL = 281
PC_GET_ACTOR_CEILING_Z = 282
PC_GET_ACTOR_POSITION_Z = 283
PC_CLEAR_ACTOR_INVENTORY = 284
PC_GIVE_ACTOR_INVENTORY = 285
PC_TAKE_ACTOR_INVENTORY = 286
PC_CHECK_ACTOR_INVENTORY = 287
PC_THING_COUNT_NAME = 288
PC_SPAWN_SPOT_FACING = 289
PC_PLAYER_CLASS = 290
PC_AND_SCRIPT_VAR = 291
PC_AND_MAP_VAR = 292
PC_AND_WORLD_VAR = 293
PC_AND_GLOBAL_VAR = 294
PC_AND_MAP_ARRAY = 295
PC_AND_WORLD_ARRAY = 296
PC_AND_GLOBAL_ARRAY = 297
PC_EOR_SCRIPT_VAR = 298
PC_EOR_MAP_VAR = 299
PC_EOR_WORLD_VAR = 300
PC_EOR_GLOBAL_VAR = 301
PC_EOR_MAP_ARRAY = 302
PC_EOR_WORLD_ARRAY = 303
PC_EOR_GLOBAL_ARRAY = 304
PC_OR_SCRIPT_VAR = 305
PC_OR_MAP_VAR = 306
PC_OR_WORLD_VAR = 307
PC_OR_GLOBAL_VAR = 308
PC_OR_MAP_ARRAY = 309
PC_OR_WORLD_ARRAY = 310
PC_OR_GLOBAL_ARRAY = 311
PC_LS_SCRIPT_VAR = 312
PC_LS_MAP_VAR = 313
PC_LS_WORLD_VAR = 314
PC_LS_GLOBAL_VAR = 315
PC_LS_MAP_ARRAY = 316
PC_LS_WORLD_ARRAY = 317
PC_LS_GLOBAL_ARRAY = 318
PC_RS_SCRIPT_VAR = 319
PC_RS_MAP_VAR = 320
PC_RS_WORLD_VAR = 321
PC_RS_GLOBAL_VAR = 322
PC_RS_MAP_ARRAY = 323
PC_RS_WORLD_ARRAY = 324
PC_RS_GLOBAL_ARRAY = 325
PC_GET_PLAYER_INFO = 326
PC_CHANGE_LEVEL = 327
PC_SECTOR_DAMAGE = 328
PC_REPLACE_TEXTURES = 329
PC_NEGATE_BINARY = 330
PC_GET_ACTOR_PITCH = 331
PC_SET_ACTOR_PITCH = 332
PC_PRINT_BIND = 333
PC_SET_ACTOR_STATE = 334
PC_THING_DAMAGE2 = 335
PC_USE_INVENTORY = 336
PC_USE_ACTOR_INVENTORY = 337
PC_CHECK_ACTOR_CEILING_TEXTURE = 338
PC_CHECK_ACTOR_FLOOR_TEXTURE = 339
PC_GET_ACTOR_LIGHT_LEVEL = 340
PC_SET_MUGSHOT_STATE = 341
PC_THING_COUNT_SECTOR = 342
PC_THING_COUNT_NAME_SECTOR = 343
PC_CHECK_PLAYER_CAMERA = 344
PC_MORPH_ACTOR = 345
PC_UNMORPH_ACTOR = 346
PC_GET_PLAYER_INPUT = 347
PC_CLASSIFY_ACTOR = 348
PC_PRINT_BINARY = 349
PC_PRINT_HEX = 350
PC_CALL_FUNC = 351
PC_SAVE_STRING = 352

# Pseudo instructions. These are used to simplify and/or improve code in the
# compiler.
# ---------------------------------------------------------------------------

PP_START = 2000000

# Same as the real instructions but with a pos_t argument.
PP_GOTO = 2000001
PP_IF_GOTO = 2000002
PP_IF_NOT_GOTO = 2000003

NODE_POS = 0
NODE_POS_USAGE = 1
NODE_CODE = 2
NODE_IMMEDIATE = 3
NODE_4BYTE_ALIGN = 4
NODE_TOTAL = 5

BUFFER_SIZE = 65536

ADD_BYTE = 0
ADD_SHORT = 1
ADD_INT = 2

class buffer_t:
   def __init__( self ):
      self.next = None
      self.data = bytearray( BUFFER_SIZE )
      self.used = 0
      self.pos = 0

class node_t:
   def __init__( self, type ):
      self.next = None
      self.type = type

class pos_t( node_t ):
   def __init__( self ):
      node_t.__init__( self, NODE_POS )
      self.term = None
      self.usages = []
      self.p_pos = 0
      self.packed = bytearray()
      self.buffer = None
      self.buffer_pos = 0
      self.size = 0
      self.node_head = None;
      self.node = None;

class pos_usage_t( node_t ):
   def __init__( self ):
      node_t.__init__( self, NODE_POS_USAGE )
      self.next_usage = None
      self.pos = None
      self.p_pos = 0

class code_t( node_t ):
   def __init__( self ):
      node_t.__init__( self, NODE_CODE )
      self.buffer = None
      self.buffer_pos = 0
      self.buffer_pos_e = 0
      self.size = 0

def add_buffer( back ):
   if back.buffer:
      if back.buffer.next:
         back.buffer = back.buffer.next
      else:
         back.buffer = buffer_t()
   else:
      back.buffer = buffer_t()
      back.buffer_head = back.buffer

def add_code( back, type, value ):
   print( 'code:', value )
   if back.code_buffer.size + 4 > BUFFER_SIZE:
      add_code_buffer( back )
   if not back.code_buffer.node or (
      back.code_buffer.node is not back.pos.node ):
      back.code_buffer.node = add_node( back, NODE_CODE )
   packed = b''
   if type == ADD_BYTE:
      packed = struct.pack( 'b', value )
   elif type == ADD_SHORT:
      packed = struct.pack( 'h', value )
   else:
      packed = struct.pack( 'i', value )
   for byte in packed:
      back.code_buffer.data[ back.code_buffer.size ] = byte
      back.code_buffer.size += 1
      back.pos.node.buffer_pos_e += 1

def add_bytes( back, bytes ):
   for byte in bytes:
      if back.buffer.pos == BUFFER_SIZE:
         add_buffer( back )
      back.buffer.data[ back.buffer.pos ] = byte
      back.buffer.pos += 1
      if back.buffer.pos > back.buffer.used:
         back.buffer.used = back.buffer.pos

def add_short( back, value ):
   add_bytes( back, struct.pack( 'h', value ) )

def add_int( back, value ):
   add_bytes( back, struct.pack( 'i', value ) )

def add_str( back, value ):
   add_bytes( back, bytes( value, 'ascii' ) )

def seek( back, pos = -1 ):
   if pos == -1:
      while back.buffer.next:
         back.buffer = back.buffer.next
      back.buffer.pos = back.buffer.used
   else:
      while True:
         if pos < BUFFER_SIZE:
            back.buffer.pos = pos
            break
         elif back.buffer.next:
            back.buffer = back.buffer.next
            pos -= BUFFER_SIZE
         else:
            back.buffer = back.buffer_head
            back.buffer.pos = 0
            break

def tell( back ):
   pos = 0
   buffer = back.buffer_head
   while True:
      if buffer is back.buffer:
         pos += buffer.pos
         break
      elif buffer.next:
         pos += BUFFER_SIZE
         buffer = buffer.next
      else:
         pos += buffer.pos
         break
   return pos

def flush( back ):
   file = open( back.options.object_file, 'wb' )
   buffer = back.buffer_head
   while buffer:
      data = buffer.data[ 0 : buffer.used ]
      file.write( data )
      buffer = buffer.next
   file.close()

def add_node( back, type ):
   node = None
   if back.node_free[ type ]:
      node = back.node_free[ type ]
      node.__init__()
      back.node_free[ type ] = node.next
   else:
      if type == NODE_POS_USAGE:
         node = pos_usage_t()
      elif type == NODE_CODE:
         node = code_t()
         node.buffer = back.code_buffer
         node.buffer_pos = back.code_buffer.size
         node.buffer_pos_e = node.buffer_pos
      elif type == NODE_IMMEDIATE:
         node = None
      else:
         node = None
   if back.pos.node:
      back.pos.node.next = node
   else:
      back.pos.node_head = node
   back.pos.node = node
   return node

def add_opc( back, code ):
   if back.compress:
      # I don't know how the compression algorithm works exactly, but at this
      # time, the following works with all of the available opcodes as of this
      # writing. Also, now that the opcode is shrinked, the 4-byte arguments
      # that follow may no longer be 4-byte aligned.
      if code >= 240:
         add_byte( back, 240 )
         add_byte( back, code - 240 )
      else:
         add_byte( back, code )
   else:
      add_int( back, code )

def add_arg( back, arg ):
   add_int( back, arg )

def add_pos( back ):
   pos = None
   if back.node_free[ NODE_POS ]:
      pos = back.node_free[ NODE_POS ]
      pos.__init__()
      back.node_free[ NODE_POS ] = pos.next
   else:
      pos = pos_t()
   if back.pos:
      back.pos.next = pos
   else:
      back.pos_head = pos
   back.pos = pos
   return pos

def use_pos( back, pos ):
   back.node_pos = pos