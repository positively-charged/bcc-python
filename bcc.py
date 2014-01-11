#!/usr/bin/python3.2

import sys
import os
sys.path.append( os.path.dirname( __file__ ) + '/src' )

import f_stmt

f_stmt.compile( sys.argv )