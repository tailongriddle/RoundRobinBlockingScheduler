# RoundRobinBlockingScheduler
Systems II: Simulates round-robin scheduling with blocking with given job lists

Something is weird with the idle mechanism - if it stops because a time slice ends, 
it either doesn't end early enough or it does something weird to the start time for 
the entire program.

Also, since we were instructed to use PriorityQueue, and also instructed to test out 
Question 2 from the lab after doing joblist1, we ran into issues where the queues 
will not run things of the same priority, meaning we had to arbitrarily 
assign the jobs in joblist2 priorities.

We also had to assign A an arbitrarily large number as the blocking interval, 
since a "0" actually means always blocking.

The program does not terminate on joblist2.txt
