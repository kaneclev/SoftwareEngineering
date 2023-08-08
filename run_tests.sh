#!/bin/bash
# Take a given program to run as a command line argument.
prog=$1 
inFile=tests/inputs/* # path correctly follows to directory.
outFile=tests/outputs/* # path correctly follows to directory
testNum=0 #counter for the output (TEST {testNum}: PASS/FAIL)



# The loop is going to occur within tests/inputs.
# We use the -v flag in order to "rank based on numerical value"
# This is important because we want the tests to pass/fail SEQUENTIALLY.
for i in $(ls -v tests/inputs/)
do
# Program output is listed to a var progOut. It runs the $prog var with the current input file.
# We use timeout to catch cases where the program will run indefinitely.
# In our case, 1 second is enough to catch infinitely looping programs.
progOut=$(timeout 1s $prog "tests/inputs/$i")

# We need to first check cases where $?, or the last executed command, returns 124, which is the exit code
# for a timed out program. So, the last command will return 124 if the progOut ran for more than 1s,
# because we set 1s to be the runtime limit before we return the command as a 124 case.
# -eq is a comparison checker; sees if the left arg is equal to the right.
if [ $? -eq 124 ]
then # then we say it was a failure. Print as per spec, increment the test we are on, and continue the loop.
echo "TEST $testNum: FAIL"
((testNum++))
continue
fi

# This is important; our expected output. We look in the outputs directory, grab the basename of our curr file $i
# Then we add the extension .output so that the path to the desired output file is complete.
# cat is used to read the contents of the file to our cariable "expected."
expected=$(cat "tests/outputs/$(basename "$i" .input).output")
if [ "$progOut" == "$expected" ] # equal condition; does the program output equal our expected output??
then # if yes, then great, we say the test case passed.
echo "TEST $testNum: PASS"
else # otherwise the results are not equal. this test didn't pass.
echo "TEST $testNum: FAIL"
fi # end of if statement
((testNum++)) #finally, increment our testNum variable to keep in order.
done

