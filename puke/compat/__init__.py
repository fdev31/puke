import sys
import pwd, grp
sys.modules['pwd'] = pwd
sys.modules['grp'] = grp