import inspect

def debug(obj):
  callerframerecord = inspect.stack()[1]    # 0 represents this line
                                            # 1 represents line at caller
  frame = callerframerecord[0]
  info = inspect.getframeinfo(frame)
  print "D "+str(info.lineno) +" on " +info.filename
  print "\t-> "+str(obj)
def Main():
  debug("Miau "+str(3))                              # for this line

# Main()