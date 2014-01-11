import struct

import common
import b_walk
import b_pcode as pcode
import b_pcode as obj

STR_ENCRYPTION_CONSTANT = 157135
DEFAULT_SCRIPT_SIZE = 20

class back_t:
   def __init__( self ):
      self.options = None
      self.file = None
      self.packed = bytearray()
      self.packed_code = bytearray()
      self.values = []
      self.node_head = None
      self.node_tail = None
      self.node = None
      self.node_pos = None
      self.nodes = []
      self.module = None
      self.str_table = None
      self.num_args = 0
      self.buffer_head = None
      self.buffer = None
      self.buffer_pos = 0
      self.buffer_pos_max = 0
      self.buffer_size = 0
      #self.node_head = None
      self.node_free = [ None ] * pcode.NODE_TOTAL
      #self.node = None
      self.compress = False
      self.pos_head = None;
      self.pos = None;

def publish( module, str_table, options ):
   back = back_t()
   back.module = module
   back.str_table = str_table
   back.options = options
   pcode.add_buffer( back )
   if options.format == common.FORMAT_LITTLE_E:
      back.compress = True

   '''
   pcode.add_code( back, pcode.ADD_BYTE, 12 )
   pcode.add_code( back, pcode.ADD_BYTE, 12 )
   pcode.add_code( back, pcode.ADD_SHORT, 12 )
   pcode.seek( back )
   pcode.add_node( back, pcode.NODE_CODE )
   pcode.add_node( back, pcode.NODE_POS )
   pcode.add_node( back, pcode.NODE_CODE )

   pos = back.pos_head
   while pos:
      curr = ''
      if pos == back.pos:
         curr = '<current>'
      print( pos, curr )
      node = pos.node_head
      while node:
         curr = ''
         if node == pos.node:
            curr = '<current>'
         print( '  ', node, curr )
         node = node.next
      pos = pos.next
   exit( 0 )'''

   # Reserve header.
   obj.add_int( back, 0 )
   obj.add_int( back, 0 )
   for script in module.scripts:
      script.offset = obj.tell( back )
      b_walk.do_block( back, script.body )
      pcode.add_opc( back, pcode.PC_TERMINATE )
   chunk_pos = obj.tell( back )
   do_sptr( back )
   #do_sflg( back )
   do_strl( back )
   obj.seek( back, 0 )
   obj.add_str( back, 'ACSE' )
   obj.add_int( back, chunk_pos )
   obj.flush( back )

def do_sptr( back ):
   if back.module.scripts:
      obj.add_str( back, 'SPTR' )
      obj.add_int( back, len( back.module.scripts ) * 12 )
      for script in back.module.scripts:
         obj.add_short( back, script.number )
         obj.add_short( back, script.type )
         obj.add_int( back, script.offset )
         obj.add_int( back, script.num_param )

def do_sflg( back ):
   packed = bytearray()
   for script in back.module.scripts:
      if script.flags:
         packed += struct.pack( 'hh', script.number, script.flags )
   if packed:
      back.packed += b'SFLG'
      back.packed += struct.pack( 'i', len( packed ) )
      back.packed += packed

def do_strl( back ):
   if back.str_table:
      start = obj.tell( back )
      obj.add_int( back, 0 )
      obj.add_int( back, 0 )
      # Number-of-strings field:
      # The number is padded with the integer 0 on both sides.
      obj.add_int( back, 0 )
      obj.add_int( back, len( back.str_table ) )
      obj.add_int( back, 0 )
      # Offsets:
      # The offset to the data of a string is relative to the start of the
      # chunk data.
      offset = (
         # Number-of-strings, written above, is 12 bytes.
         12 +
         # Array of offsets to the string data.
         len( back.str_table ) * 4 )
      offset_encrypt = offset
      for str in back.str_table:
         obj.add_int( back, offset )
         # Plus one for the NULL byte.
         offset += len( str ) + 1
      # String data.
      for str in back.str_table:
         obj.add_str( back, str )
         obj.add_str( back, '\0' )
         if back.options.encrypt_str:
            # TODO: Figure out what to do if an overflow occurs.
            key = offset_encrypt * STR_ENCRYPTION_CONSTANT
            i = 0
            while i < len( str ):
               str[ i ] = ( str[ i ] ^ ( key + i // 2 ) ) & 0xFF
               i += 1
         packed += str
      name = b'STRL'
      if back.options.encrypt_str:
         name = b'STRE'
      back.packed += name
      back.packed += struct.pack( 'i', len( packed ) )
      back.packed += packed