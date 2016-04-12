import inspect
import os
def debug(obj):
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  f = info.filename.split(os.sep)
  print "D "+str(info.lineno) +" on " +f[len(f)-1]
  print "\t-> "+str(obj)
def Main():
  debug("Miau "+str(3))                              # for this line

# Main()