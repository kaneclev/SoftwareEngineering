# We are going to use a shell script to find a one-minimal subset of a given set n which is interesting.
import sys # for retrieving command line arguments
import os # for running commands


# is interesting evaluates whether or not a given set is 'interesting' according to a BASH script.
def is_interesting(subset):
    # cleans the subset passed in and passes it to the os utility that can then run it on the command line
    cleaned_subset = ' '.join(str(i) for i in subset) # join the numbers in the set together with spaces in between (formatting)
    cmd_string = cmd + ' ' + cleaned_subset  # add a space between our command (thru sys args) and the subset we are debugging
    # return the exit code provided by os.system
    return os.system(cmd_string)

# now for the DD algorithm; it returns a set
def delta(subset, req) -> set:
    n = len(subset)
   
    # if there is only one change in the subset, return that change. (base case)
    if n == 1:
        return subset
    
    # two empty sets to build our partitions.
    p1 = set()
    p2 = set()
    # iterate through the subset and add elements to our partitions.
    for i, elem in enumerate(subset):
        if i < n/2:
            p1.add(elem)
        else:
            p2.add(elem) 

    if (is_interesting(req.union(p1)) > 0): # case where req U p1 are interesting
        return delta(p1, req)
    elif (is_interesting(req.union(p2)) > 0): # case where req U p2 are interesting
        return delta(p2, req)
    else: # case where neither are interesting: interference set
        return (delta(p1, req.union(p2)).union(delta(p2, req.union(p1))))


if len(sys.argv) != 3: # if we dont have the correct num of command line arguments (for personal debugging)
    print("Not enough args.")
    exit -1

n = int(sys.argv[1]) # grab n from command line
cmd = sys.argv[2] # grab BASH script
# beginning set 0-n; 'changes'
C = set(range(0, n))
# if we are interesting to start with...
if is_interesting(C) > 0:
    req = set() # beginning empty req set
    interesting_min = delta(C, req) # call delta debugging
    print(sorted(interesting_min)) # return as a sorted list as per spec