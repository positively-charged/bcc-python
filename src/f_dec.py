import common
import f_main
from f_main import ( bail, diag, DIAG_COLUMN, DIAG_ERR, DIAG_FILE, DIAG_LINE )
import f_stmt
import f_token as tk
import f_expr
import b_opcode

AREA_TOP = 0
AREA_LOCAL = 1
AREA_FOR = 2
AREA_PARAM = 3

MAX_MAP_LOCATIONS = 128
MAX_WORLD_LOCATIONS = 256
MAX_GLOBAL_LOCATIONS = 64

SCRIPT_MIN_NUM = 0
SCRIPT_MAX_NUM = 999
SCRIPT_MAX_PARAMS = 3

def is_dec( front ):
   return front.tk in [ tk.T_INT, tk.T_STR, tk.T_BOOL, tk.T_VOID,
      tk.T_FUNCTION, tk.T_WORLD, tk.T_GLOBAL, tk.T_STATIC ]

def read( front, area ):
   dec = {
      'area' : area,
      'pos' : front.tk_pos,
      'storage' : common.STORAGE_LOCAL,
      'storage_pos' : None,
      'storage_name' : 'local',
      'value' : False,
      'name' : '',
      'name_pos' : None,
      'dim' : [],
      'dim_implicit' : None,
      'initials' : []
   }
   func = False
   if front.tk == tk.T_FUNCTION and area == AREA_TOP:
      tk.read( front )
      func = True

   # Storage.
   if not func:
      if front.tk == tk.T_GLOBAL:
         dec[ 'storage' ] = common.STORAGE_GLOBAL
         dec[ 'storage_pos' ] = front.tk_pos
         dec[ 'storage_name' ] = front.tk_text
         tk.read( front )
      elif front.tk == tk.T_WORLD:
         dec[ 'storage' ] = common.STORAGE_WORLD
         dec[ 'storage_pos' ] = front.tk_pos
         dec[ 'storage_name' ] = front.tk_text
         tk.read( front )
      elif front.tk == tk.T_STATIC:
         dec[ 'storage' ] = common.STORAGE_MAP
         dec[ 'storage_name' ] = 'map'
         if area == AREA_FOR:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, 'static variable in for loop initialization' )
         elif area == AREA_PARAM:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, '\'static\' used in parameter' )
         elif area == AREA_TOP:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, '\'static\' used in top scope' )
         tk.read( front )
      elif area == AREA_TOP:
         dec[ 'storage' ] = common.STORAGE_MAP
         dec[ 'storage_name' ] = 'map'

   # Type.
   if front.tk in [ tk.T_INT, tk.T_STR, tk.T_BOOL ]:
      # Scripts can only have integer parameters.
      if area == AREA_PARAM and front.dec_params[ 'is_script' ] and \
         front.tk != tk.T_INT:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'script parameter not of \'int\' type' )
      dec[ 'value' ] = True
      tk.read( front )
   elif front.tk == tk.T_VOID:
      tk.read( front )
   else:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'expecting type in declaration' )
      raise Exception
      bail( front )

   while True:
      # Storage index.
      if not func:
         if front.tk == tk.T_LIT_DECIMAL:
            pos = front.tk_pos
            dec[ 'storage_index' ] = f_expr.read_literal( front )
            tk.test( front, tk.T_COLON )
            tk.read( front )
            max_loc = MAX_WORLD_LOCATIONS
            if dec[ 'storage' ] != common.STORAGE_WORLD:
               if dec[ 'storage' ] == common.STORAGE_GLOBAL:
                  max_loc = MAX_GLOBAL_LOCATIONS
               else:
                  diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
                     pos, 'index specified for %s storage',
                     dec[ 'storage_name' ] )
                  bail( front )
            if dec[ 'storage_index' ] >= max_loc:
               diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
                  pos, 'index specified for %s storage',
                  dec[ 'storage_name' ] )
               bail( front )
         else:
            # Index must be explicitly specified for these storages.
            if dec[ 'storage' ] == common.STORAGE_WORLD or \
               dec[ 'storage' ] == common.STORAGE_GLOBAL:
               diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
                  front.tk_pos, 'missing index for %s storage',
                  dec[ 'storage_name' ] )
               bail( front )

      # Name.
      if front.tk == tk.T_ID:
         dec[ 'name_pos' ] = front.tk_pos
         dec[ 'name' ] = read_unique_name( front )
      else:
         # Parameters don't require a name.
         if area != AREA_PARAM:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               front.tk_pos, 'missing name in declaration' )
            bail( front )

      if func:
         tk.test( front, tk.T_PAREN_L )
         tk.read( front )
         f_main.add_scope( front )
         num_param = read_param_list( front, False )
         tk.test( front, tk.T_PAREN_R )
         tk.read( front )
         func = common.func_t()
         func.pos = dec[ 'name_pos' ]
         func.value = dec[ 'value' ]
         func.name = dec[ 'name' ]
         func.min_param = num_param
         func.max_param = num_param
         front.scopes[ 0 ].names[ func.name ] = func
         block = common.block_t()
         front.block = block
         front.func = func
         f_stmt.read_block( front )
         f_main.pop_scope( front )
         front.block = None
         front.func = None
         func.impl = {
            'def' : True,
            'def_params' : True,
            'body' : block,
            'index' : 0,
            'size' : 0
         }
         front.module.funcs.append( func )
         break
      else:
         # Array dimension.
         if front.tk == tk.T_BRACKET_L:
            read_dim( front, dec )
         else:
            dec[ 'dim' ] = []
            dec[ 'dim_implicit' ] = None
         read_init( front, dec )
         if area == AREA_PARAM:
            if dec[ 'name' ]:
               pass
            break
         else:
            finish_var( front, dec )
            if front.tk == tk.T_COMMA:
               tk.read( front )
            else:
               tk.test( front, tk.T_SEMICOLON )
               tk.read( front )
               break

def read_unique_name( front ):
   tk.test( front, tk.T_ID )
   if front.tk_text in front.scope.names:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'name \'%s\' already used', front.tk_text )
      object = front.scope.names[ front.tk_text ]
      pos = None
      if object.node == common.NODE_VAR or \
         object.node == common.NODE_CONSTANT:
         pos = object.pos
      elif object.node == common.NODE_FUNC:
         # These builtin functions are loaded internally by the compiler and
         # have no position of their definition given.
         if object.type != common.FUNC_DED and \
            object.type != common.FUNC_FORMAT:
            pos = object.pos
      if pos:
         diag( front, DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
            'name previously used here' )
      bail( front )
   else:
      name = front.tk_text
      tk.read( front )
      return name

def read_dim( front, dec ):
   # At this time, a local array is not allowed.
   if dec[ 'storage' ] == common.STORAGE_LOCAL:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'array in local scope' )
      bail( front )
   while front.tk == tk.T_BRACKET_L:
      pos = front.tk_pos
      tk.read( front )
      expr = None
      # Implicit size.
      if front.tk == tk.T_BRACKET_R:
         # Only the first dimension can have an implicit size.
         if len( dec[ 'dim' ] ):
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, pos,
               'implicit size in subsequent dimension' )
            bail( front )
         tk.read( front )
      else:
         expr = f_expr.read( front, True )
         tk.test( front, tk.T_BRACKET_R )
         tk.read( front )
         if not expr.folded:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               expr.pos, 'array size not a constant expression' )
            bail( front )
         elif expr.value <= 0:
            diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
               expr.pos, 'invalid array size' )
            bail( front )
      dim = common.dim_t()
      dec[ 'dim' ].append( dim )
      if not expr:
         dec[ 'dim_implicit' ] = dim
      else:
         dim.size = expr.value
   i = len( dec[ 'dim' ] ) - 1
   # For now, each element of the last dimension is 1 integer in size.
   dec[ 'dim' ][ i ].element_size = 1
   while i > 0:
      dec[ 'dim' ][ i - 1 ].element_size = (
         dec[ 'dim' ][ i ].element_size *
         dec[ 'dim' ][ i ].size )
      i -= 1

def read_init( front, dec ):
   if front.tk != tk.T_ASSIGN:
      if dec[ 'dim_implicit' ] and ( (
         dec[ 'storage' ] != common.STORAGE_WORLD and
         dec[ 'storage' ] != common.STORAGE_GLOBAL ) or
         len( dec[ 'dim' ] ) > 1 ):
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'missing initialization' )
         bail( front )
      return
   # At this time, there is no way to initialize at the top scope an array with
   # world or global storage.
   if ( dec[ 'storage' ] == common.STORAGE_WORLD or
      dec[ 'storage' ] == common.STORAGE_GLOBAL ) and \
      len( front.scopes ) == 1:
      diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
         front.tk_pos, 'initialization of variable with %s storage '
         'at top scope', dec[ 'storage_name' ] )
      bail( front )
   tk.read( front )
   if front.tk == tk.T_BRACE_L:
      read_initz( front, dec )
   else:
      if len( dec[ 'dim' ] ):
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'array initialization missing initializer' )
         bail( front )
      expr = f_expr.read( front, True )
      if dec[ 'storage' ] == common.STORAGE_MAP and not expr.folded:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN, expr.pos,
            'initial value not constant' )
         bail( front )
      initial = common.initial_t()
      initial.value = expr.value
      dec[ 'initials' ].append( initial )

def finish_var( front, dec ):
   var = common.var_t()
   var.pos = dec[ 'name_pos' ]
   var.name = dec[ 'name' ]
   var.storage = dec[ 'storage' ]
   var.dim = dec[ 'dim' ]
   if var.dim:
      var.size = var.dim[ 0 ].size * var.dim[ 0 ].element_size
      var.initial = dec[ 'initials' ]
   else:
      var.size = 1
      if dec[ 'initials' ]:
         var.initial = dec[ 'initials' ].pop()
   front.scope.names[ var.name ] = var
   if var.dim:
      front.module.arrays.append( var )
   elif dec[ 'area' ] == AREA_TOP:
      # Variables with initials appear first.
      if var.initial:
         front.module.vars.insert( 0, var )
      else:
         front.module.vars.append( var )
   elif dec[ 'area' ] == AREA_LOCAL:
      var.index = alloc_index( front )
      front.block.stmts.append( var )
   else:
      var.index = alloc_index( front )
      front.dec_for_init.append( var )

def read_param_list( front, is_script ):
   return 0

def read_script( front ):
   tk.test( front, tk.T_SCRIPT )
   script = common.script_t()
   script.pos = front.tk_pos
   tk.read( front )
   # Script number.
   number_pos = None
   if front.tk == tk.T_SHIFT_L:
      tk.read( front )
      # The token between the << and >> tokens must be the digit zero.
      if front.tk == tk.T_LIT_DECIMAL and front.tk_text == '0':
         number_pos = front.tk_pos
         tk.read( front )
         tk.test( front, tk.T_SHIFT_R )
         tk.read( front )
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, 'missing the digit 0' )
         bail( front )
   else:
      front.reading_script_number = True
      expr = f_expr.read( front, True )
      front.reading_script_number = False
      if not expr.folded:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            expr.pos, 'script number not a constant expression' )
         bail( front )
      elif expr.value < SCRIPT_MIN_NUM or expr.value > SCRIPT_MAX_NUM:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            expr.pos, 'script number not between %d and %d', SCRIPT_MIN_NUM,
            SCRIPT_MAX_NUM )
         bail( front )
      elif expr.value == 0:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            expr.pos, 'script number 0 not between << and >>' )
         bail( front )
      else:
         script.number = expr.value
         number_pos = expr.pos
   # There should be no duplicate scripts in the same module.
   for older_script in front.module.scripts:
      if script.number == older_script.number:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            number_pos, 'script number %d already used', script.number )
         diag( front, DIAG_FILE | DIAG_LINE | DIAG_COLUMN, older_script.pos,
            'first script to use number found here' )
         break
   f_main.add_scope( front )
   # Parameter list.
   param_pos = None
   if front.tk == tk.T_PAREN_L:
      param_pos = front.tk_pos
      tk.read( front )
      script.num_param = read_param_list( front, True )
      tk.test( front, tk.T_PAREN_R )
      tk.read( front )
   # Script type.
   types = {
      tk.T_OPEN : common.SCRIPT_TYPE_OPEN,
      tk.T_RESPAWN : common.SCRIPT_TYPE_RESPAWN,
      tk.T_DEATH : common.SCRIPT_TYPE_DEATH,
      tk.T_ENTER : common.SCRIPT_TYPE_ENTER,
      tk.T_PICKUP : common.SCRIPT_TYPE_PICKUP,
      tk.T_BLUE_RETURN : common.SCRIPT_TYPE_BLUE_RETURN,
      tk.T_RED_RETURN : common.SCRIPT_TYPE_RED_RETURN,
      tk.T_WHITE_RETURN : common.SCRIPT_TYPE_WHITE_RETURN,
      tk.T_LIGHTNING : common.SCRIPT_TYPE_LIGHTNING,
      tk.T_DISCONNECT : common.SCRIPT_TYPE_DISCONNECT,
      tk.T_UNLOADING : common.SCRIPT_TYPE_UNLOADING,
      tk.T_RETURN : common.SCRIPT_TYPE_RETURN }
   name = ''
   if front.tk in types:
      script.type = types[ front.tk ]
      name = front.tk_text
      tk.read( front )
   if script.type == common.SCRIPT_TYPE_CLOSED:
      if script.num_param > SCRIPT_MAX_PARAMS:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            param_pos, 'script has over maximum %d parameters',
            SCRIPT_MAX_PARAMS )
   elif script.type == common.SCRIPT_TYPE_DISCONNECT:
      # A disconnect script must have a single parameter. It is the number of
      # the player who disconnected from the server.
      if script.num_param != 1:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            param_pos,
            'disconnect script missing one player-number parameter' )
   else:
      if script.num_param != 0:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            param_pos, 'parameter list specified for %s script', name )
   # Script flags.
   while True:
      flag = common.SCRIPT_FLAG_NET
      if front.tk != tk.T_NET:
         if front.tk == tk.T_CLIENTSIDE:
            flag = common.SCRIPT_FLAG_CLIENTSIDE
         else:
            break
      if not ( script.flags & flag ):
         script.flags |= flag
         tk.read( front )
      else:
         diag( front, DIAG_ERR | DIAG_FILE | DIAG_LINE | DIAG_COLUMN,
            front.tk_pos, '%s flag already set', front.tk_text )
         tk.read( front )
   # Body.
   block = common.block_t()
   block.in_script = True
   front.block = block
   f_stmt.read_block( front )
   front.block = None
   script.body = block
   f_main.pop_scope( front )
   front.module.scripts.append( script )

def read_bfunc_list( front ):
   tk.test( front, tk.T_SPECIAL )
   tk.read( front )
   while True:
      ext = False
      if front.tk == tk.T_MINUS:
         tk.read( front )
         ext = True
      code = f_expr.read_literal( front )
      tk.test( front, tk.T_COLON )
      tk.read( front )
      name_pos = front.tk_pos
      name = read_unique_name( front )
      tk.test( front, tk.T_PAREN_L )
      tk.read( front )
      min_param = 0
      max_param = f_expr.read_literal( front )
      if front.tk == tk.T_COMMA:
         min_param = max_param
         tk.read( front )
         max_param = f_expr.read_literal( front )
      tk.test( front, tk.T_PAREN_R )
      tk.read( front )
      func = common.func_t()
      func.pos = name_pos
      func.value = True
      func.min_param = min_param
      func.max_param = max_param
      front.scopes[ 0 ].names[ name ] = func
      if ext:
         func.type = common.FUNC_EXT
         func.impl[ 'id' ] = code
      else:
         func.type = common.FUNC_ASPEC
         func.impl[ 'id' ] = code
      if front.tk == tk.T_COMMA:
         tk.read( front )
      else:
         tk.test( front, tk.T_SEMICOLON )
         tk.read( front )
         break

def load_ded_format_funcs( front ):
   ded = [
      # Format: name / returns-value / parameter-count / parameter-minimum /
      # opcode / is-latent.
      [ 'delay', False, 1, 1, b_opcode.k_delay, True ],
      [ 'random', True, 2, 2, b_opcode.k_random, False ],
      [ 'thingcount', True, 2, 2, b_opcode.k_thing_count, False ],
      [ 'tagwait', False, 1, 1, b_opcode.k_tag_wait, True ],
      [ 'polywait', False, 1, 1, b_opcode.k_poly_wait, True ],
      [ 'changefloor', False, 2, 2, b_opcode.k_change_floor, False ],
      [ 'changeceiling', False, 2, 2, b_opcode.k_change_ceiling, False ],
      [ 'lineside', True, 0, 0, b_opcode.k_line_side, False ],
      [ 'scriptwait', False, 1, 1, b_opcode.k_script_wait, True ],
      [ 'clearlinespecial', False, 0, 0, b_opcode.k_clear_line_special, False ],
      [ 'playercount', True, 0, 0, b_opcode.k_player_count, False ],
      [ 'gametype', True, 0, 0, b_opcode.k_game_type, False ],
      [ 'gameskill', True, 0, 0, b_opcode.k_game_skill, False ],
      [ 'timer', True, 0, 0, b_opcode.k_timer, False ],
      [ 'sectorsound', False, 2, 2, b_opcode.k_sector_sound, False ],
      [ 'ambientsound', False, 2, 2, b_opcode.k_ambient_sound, False ],
      [ 'soundsequence', False, 1, 1, b_opcode.k_sound_sequence, False ],
      [ 'setlinetexture', False, 4, 4, b_opcode.k_set_line_texture, False ],
      [ 'setlineblocking', False, 2, 2, b_opcode.k_set_line_blocking, False ],
      [ 'setlinespecial', False, 7, 2, b_opcode.k_set_line_special, False ],
      [ 'thingsound', False, 3, 3, b_opcode.k_thing_sound, False ],
      [ 'activatorsound', False, 2, 2, b_opcode.k_activator_sound, False ],
      [ 'localambientsound', False, 2, 2, b_opcode.k_local_ambient_sound,
         False ],
      [ 'setlinemonsterblocking', False, 2, 2,
         b_opcode.k_set_line_monster_blocking, False ],
      [ 'ismultiplayer', True, 0, 0, b_opcode.k_is_multiplayer, False ],
      [ 'playerteam', True, 0, 0, b_opcode.k_player_team, False ],
      [ 'playerhealth', True, 0, 0, b_opcode.k_player_health, False ],
      [ 'playerarmorpoints', True, 0, 0, b_opcode.k_player_armor_points,
         False ],
      [ 'playerfrags', True, 0, 0, b_opcode.k_player_frags, False ],
      [ 'bluecount', True, 0, 0, b_opcode.k_blue_team_count, False ],
      [ 'blueteamcount', True, 0, 0, b_opcode.k_blue_team_count, False ],
      [ 'redcount', True, 0, 0, b_opcode.k_red_team_count, False ],
      [ 'redteamcount', True, 0, 0, b_opcode.k_red_team_count, False ],
      [ 'bluescore', True, 0, 0, b_opcode.k_blue_team_score, False ],
      [ 'blueteamscore', True, 0, 0, b_opcode.k_blue_team_score, False ],
      [ 'redscore', True, 0, 0, b_opcode.k_red_team_score, False ],
      [ 'redteamscore', True, 0, 0, b_opcode.k_red_team_score, False ],
      [ 'isoneflagctf', True, 0, 0, b_opcode.k_is_one_flag_ctf, False ],
      [ 'getinvasionwave', True, 0, 0, b_opcode.k_get_invasion_wave, False ],
      [ 'getinvasionstate', True, 0, 0, b_opcode.k_get_invasion_state, False ],
      [ 'music_change', False, 2, 2, b_opcode.k_music_change, False ],
      [ 'consolecommand', False, 3, 1, b_opcode.k_console_command, False ],
      [ 'singleplayer', True, 0, 0, b_opcode.k_single_player, False ],
      [ 'fixedmul', True, 2, 2, b_opcode.k_fixed_mul, False ],
      [ 'fixeddiv', True, 2, 2, b_opcode.k_fixed_div, False ],
      [ 'setgravity', False, 1, 1, b_opcode.k_set_gravity, False ],
      [ 'setaircontrol', False, 1, 1, b_opcode.k_set_air_control, False ],
      [ 'clearinventory', False, 0, 0, b_opcode.k_clear_inventory, False ],
      [ 'giveinventory', False, 2, 2, b_opcode.k_give_inventory, False ],
      [ 'takeinventory', False, 2, 2, b_opcode.k_take_inventory, False ],
      [ 'checkinventory', True, 1, 1, b_opcode.k_check_inventory, False ],
      [ 'spawn', True, 6, 4, b_opcode.k_spawn, False ],
      [ 'spawnspot', True, 4, 2, b_opcode.k_spawn_spot, False ],
      [ 'setmusic', False, 3, 1, b_opcode.k_set_music, False ],
      [ 'localsetmusic', False, 3, 1, b_opcode.k_local_set_music, False ],
      [ 'setfont', False, 1, 1, b_opcode.k_set_font, False ],
      [ 'setthingspecial', False, 7, 2, b_opcode.k_set_thing_special, False ],
      [ 'fadeto', False, 5, 5, b_opcode.k_fade_to, False ],
      [ 'faderange', False, 9, 9, b_opcode.k_fade_range, False ],
      [ 'cancelfade', False, 0, 0, b_opcode.k_cancel_fade, False ],
      [ 'playmovie', True, 1, 1, b_opcode.k_play_movie, False ],
      [ 'setfloortrigger', False, 8, 3, b_opcode.k_set_floor_trigger, False ],
      [ 'setceilingtrigger', False, 8, 3, b_opcode.k_set_ceiling_trigger,
         False ],
      [ 'getactorx', True, 1, 1, b_opcode.k_get_actor_x, False ],
      [ 'getactory', True, 1, 1, b_opcode.k_get_actor_y, False ],
      [ 'getactorz', True, 1, 1, b_opcode.k_get_actor_z, False ],
      [ 'sin', True, 1, 1, b_opcode.k_sin, False ],
      [ 'cos', True, 1, 1, b_opcode.k_cos, False ],
      [ 'vectorangle', True, 2, 2, b_opcode.k_vector_angle, False ],
      [ 'checkweapon', True, 1, 1, b_opcode.k_check_weapon, False ],
      [ 'setweapon', True, 1, 1, b_opcode.k_set_weapon, False ],
      [ 'setmarineweapon', False, 2, 2, b_opcode.k_set_marine_weapon, False ],
      [ 'setactorproperty', False, 3, 3, b_opcode.k_set_actor_property, False ],
      [ 'getactorproperty', True, 2, 2, b_opcode.k_get_actor_property, False ],
      [ 'playernumber', True, 0, 0, b_opcode.k_player_number, False ],
      [ 'activatortid', True, 0, 0, b_opcode.k_activator_tid, False ],
      [ 'setmarinesprite', False, 2, 2, b_opcode.k_set_marine_sprite, False ],
      [ 'getscreenwidth', True, 0, 0, b_opcode.k_get_screen_width, False ],
      [ 'getscreenheight', True, 0, 0, b_opcode.k_get_screen_height, False ],
      [ 'thing_projectile2', False, 7, 7, b_opcode.k_thing_projectile2, False ],
      [ 'strlen', True, 1, 1, b_opcode.k_strlen, False ],
      [ 'sethudsize', False, 3, 3, b_opcode.k_set_hud_size, False ],
      [ 'getcvar', True, 1, 1, b_opcode.k_get_cvar, False ],
      [ 'setresultvalue', False, 1, 1, b_opcode.k_set_result_value, False ],
      [ 'getlinerowoffset', True, 0, 0, b_opcode.k_get_line_row_offset, False ],
      [ 'getactorfloorz', True, 1, 1, b_opcode.k_get_actor_floor_z, False ],
      [ 'getactorangle', True, 1, 1, b_opcode.k_get_actor_angle, False ],
      [ 'getsectorfloorz', True, 3, 3, b_opcode.k_get_sector_floor_z, False ],
      [ 'getsectorceilingz', True, 3, 3, b_opcode.k_get_sector_ceiling_z,
         False ],
      [ 'getsigilpieces', True, 0, 0, b_opcode.k_get_sigil_pieces, False ],
      [ 'getlevelinfo', True, 1, 1, b_opcode.k_get_level_info, False ],
      [ 'changesky', False, 2, 2, b_opcode.k_change_sky, False ],
      [ 'playeringame', True, 1, 1, b_opcode.k_player_in_game, False ],
      [ 'playerisbot', True, 1, 1, b_opcode.k_player_is_bot, False ],
      [ 'setcameratotexture', False, 3, 3, b_opcode.k_set_camera_to_texture,
         False ],
      [ 'getammocapacity', True, 1, 1, b_opcode.k_get_ammo_capacity, False ],
      [ 'setammocapacity', False, 2, 2, b_opcode.k_set_ammo_capacity, False ],
      [ 'setactorangle', False, 2, 2, b_opcode.k_set_actor_angle, False ],
      [ 'spawnprojectile', False, 7, 7, b_opcode.k_spawn_projectile, False ],
      [ 'getsectorlightlevel', True, 1, 1, b_opcode.k_get_sector_light_level,
         False ],
      [ 'getactorceilingz', True, 1, 1, b_opcode.k_get_actor_ceiling_z, False ],
      [ 'clearactorinventory', False, 1, 1, b_opcode.k_clear_actor_inventory,
         False ],
      [ 'giveactorinventory', False, 3, 3, b_opcode.k_give_actor_inventory,
         False ],
      [ 'takeactorinventory', False, 3, 3, b_opcode.k_take_actor_inventory,
         False ],
      [ 'checkactorinventory', True, 2, 2, b_opcode.k_check_actor_inventory,
         False ],
      [ 'thingcountname', True, 2, 2, b_opcode.k_thing_count_name, False ],
      [ 'spawnspotfacing', True, 3, 2, b_opcode.k_spawn_spot_facing, False ],
      [ 'playerclass', True, 1, 1, b_opcode.k_player_class, False ],
      [ 'getplayerinfo', True, 2, 2, b_opcode.k_get_player_info, False ],
      [ 'changelevel', False, 4, 3, b_opcode.k_change_level, False ],
      [ 'sectordamage', False, 5, 5, b_opcode.k_sector_damage, False ],
      [ 'replacetextures', False, 3, 2, b_opcode.k_replace_textures, False ],
      [ 'getactorpitch', True, 1, 1, b_opcode.k_get_actor_pitch, False ],
      [ 'setactorpitch', False, 2, 2, b_opcode.k_set_actor_pitch, False ],
      [ 'setactorstate', True, 3, 2, b_opcode.k_set_actor_state, False ],
      [ 'thing_damage2', True, 3, 3, b_opcode.k_thing_damage2, False ],
      [ 'useinventory', True, 1, 1, b_opcode.k_use_inventory, False ],
      [ 'useactorinventory', True, 2, 2, b_opcode.k_use_actor_inventory,
         False ],
      [ 'checkactorceilingtexture', True, 2, 2,
         b_opcode.k_check_actor_ceiling_texture, False ],
      [ 'checkactorfloortexture', True, 2, 2,
         b_opcode.k_check_actor_floor_texture, False ],
      [ 'getactorlightlevel', True, 1, 1, b_opcode.k_get_actor_light_level,
         False ],
      [ 'setmugshotstate', False, 1, 1, b_opcode.k_set_mugshot_state, False ],
      [ 'thingcountsector', True, 3, 3, b_opcode.k_thing_count_sector, False ],
      [ 'thingcountnamesector', True, 3, 3, b_opcode.k_thing_count_name_sector,
         False ],
      [ 'checkplayercamera', True, 1, 1, b_opcode.k_check_player_camera,
         False ],
      [ 'morphactor', True, 7, 7, b_opcode.k_morph_actor, False ],
      [ 'unmorphactor', True, 2, 1, b_opcode.k_unmorph_actor, False ],
      [ 'getplayerinput', True, 2, 2, b_opcode.k_get_player_input, False ],
      [ 'classifyactor', True, 1, 1, b_opcode.k_classify_actor, False ] ]
   for template in ded:
      name, value, max_param, min_param, opcode, latent = template
      func = common.func_t()
      func.type = common.FUNC_DED
      func.value = value
      func.min_param = min_param
      func.max_param = max_param
      func.impl = {
         'opcode' : opcode,
         'latent' : latent }
      front.scope.names[ name ] = func
   format = [
      # Format: name / returns-value / parameter-count / parameter-minimum /
      # terminating-opcode.
      # Note: The format items together count as a single parameter.
      [ 'print', False, 1, 1, b_opcode.k_end_print ],
      [ 'printbold', False, 1, 1, b_opcode.k_end_print_bold ],
      [ 'hudmessage', False, 9, 7, b_opcode.k_end_hud_message ],
      [ 'hudmessagebold', False, 9, 7, b_opcode.k_end_hud_message_bold ],
      [ 'log', False, 1, 1, b_opcode.k_end_log ],
      [ 'strparam', True, 1, 1, b_opcode.k_save_string ] ]
   for template in format:
      name, value, max_param, min_param, opcode = template
      func = common.func_t()
      func.type = common.FUNC_FORMAT
      func.value = value
      func.min_param = min_param
      func.max_param = max_param
      func.impl = {
         'opcode' : opcode }
      front.scope.names[ name ] = func