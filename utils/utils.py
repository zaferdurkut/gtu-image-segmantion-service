import os, time

def FindPaths(directory,stipe):
    """""
     
     Arguments:
         directory {str} -- taranmak istenen ust dizin
         stipe {str} -- taranan uzanti
     
     Returns:
        path_list {list} -- path list for stipe
    """
    if stipe.islower():
        stipe_u = stipe.upper()
    else:
        stipe_u = stipe.lower()

    if directory:
        path_list = []
        for root, subdirectory, files in os.walk(directory):
            for f in files:
                if f.endswith(stipe) or f.endswith(stipe_u):
                    path_list.append(os.path.join(root,f))

        return path_list
    else:
       return None

def timerfunc(func):
    """
    A timer decorator
    """
    def function_timer(*args, **kwargs):
        """
        A nested function for timing other functions
        """
        start = time.time()
        value = func(*args, **kwargs)
        end = time.time()
        runtime = end - start
        msg = "The runtime for {func} took {time} seconds to complete"
        print(msg.format(func=func.__name__,
                         time=runtime))
        return value
    return function_timer
 