import sys
from s2python.communication.s2_connection import S2Connection
sys.modules['s2python.s2_connection'] = sys.modules.get('s2python.communication.s2_connection', None)
