# import statements
import sys
from queue import PriorityQueue 

class Process():
    #initialize process object
    def __init__(self, name, priority, arrival_time, total_time, block_interval):
        self.name = name
        self.priority = priority
        self.arrival_time = arrival_time
        self.total_time = total_time
        self.block_interval = block_interval

        self.remaining_time = total_time
        self.next_block = block_interval
        self.block_left = 0    
        self.status = "READY"    
        
    

def roundRobin(inputFile, timeSlice, blockDuration):
    processes = []
    arrivalQ = PriorityQueue() # when a process enters the system, put it here
    blockedQ = PriorityQueue() # when a process is blocked, put it here
    readyQ = PriorityQueue() # when a process is ready
    isIdle = 0
    wasIdle = 0
    averageTime = 0
    idleTime = 0
    idleStart = 0
    
    simulationTime = 0 # simulation time starting at 0
 
    # create processes
    with open(inputFile, "r") as jobs:
        for process in jobs:
            name, priority, arrival_time, total_time, block_interval = process.split()
            processes.append(Process(name, int(priority), int(arrival_time), int(total_time), int(block_interval)))
    
    #print(processes)
    
    while len(processes) != 0: # while processes not empty
        # instantiate time slice
        start = simulationTime
        end = simulationTime + timeSlice
        processName = ""
        status_code = ""
        
        
        for x in processes: # when a process enters the system, it is put in arrival queue
            if x.arrival_time == simulationTime:
                #print(x.name) #debug
                arrivalQ.put((-abs(x.priority), x)) 

            if x.status == "BLOCKED" and x.block_left == 0:
                x.next_block = x.block_interval
                x.status = "READY"
                isIdle = 0
                removedPriority, removedX = blockedQ.get()
                if removedX in processes:
                        readyQ.put((-abs(removedPriority), removedX))
                
        while not arrivalQ.empty(): # add any processes that have arrived since to ready q
            priority, process = arrivalQ.get()
            #print(process.name) #debug
            readyQ.put((-abs(priority), process))
        if not readyQ.empty():  
            priority, running = readyQ.get() # pull next process off the ready queue
             
            processName = running.name
            #print(processName) #debug  
            isIdle = 0
            #print("NOT IDLE") #debug
        else:
            isIdle = 1
            #print("IDLE") #debug
        #print(running.name, simulationTime) #debug
        
       # start time slice
       
        while simulationTime < end:
            
            for x in processes: # when a process enters the system, it is put in arrival queue
                if ((x.arrival_time == simulationTime) & (x != running)):
                    #print(x.name) #debug
                    isIdle = 0
                    arrivalQ.put((-abs(x.priority), x)) 
                if x.block_left != 0:
                    #print(x.block_left)
                    x.block_left -= 1
                elif x.status == "BLOCKED":
                    x.next_block = x.block_interval
                    x.status = "READY"
                    isIdle = 0
                    removedPriority, removedX = blockedQ.get()
                    #print(removedPriority)
                    #print(removedX.name) #debug
                    if removedX in processes:
                        readyQ.put((-abs(removedPriority), removedX))
            while not arrivalQ.empty(): # add any processes that have arrived since to ready q
                priority2, process2 = arrivalQ.get() 
                #print(process2.name) #debug
                readyQ.put((-abs(priority2), process2))
            
            if wasIdle == 1 and isIdle == 0:    
                idleName = "(IDLE)" # print IDLE 
                idleCode = "I"     
                wasIdle = 0
                
                toPrint = [str(idleStart), idleName, str(idleTime), idleCode]
                print("\t".join(toPrint))
                break
                
            # if idleTime + idleStart < end:
 
            if wasIdle == 0 and isIdle == 1:
                processName = "(IDLE)" # print IDLE 
                status_code = "I" 
                wasIdle = 1
                idleTime = 0
                idleStart = simulationTime
                
            if wasIdle == 1 and isIdle == 1:
                processName = "(IDLE)" # print IDLE 
                status_code = "I" 
                idleTime += 1
                
                if idleTime + idleStart + 3 >= end:                                         
                    break
            
            if isIdle == 0:                    

                if running.next_block != 0 and running.status == "READY": # if processing
                    running.remaining_time -= 1
                    running.next_block -= 1   

                    status_code = "P"

                    #print(running.next_block) #debug
                
                if running.next_block == 0 and running.status != "BLOCKED": # if it is time to block and not already blocked
                    running.block_left = blockDuration
                    blockedQ.put((-abs(running.priority), running))
                    #print("BLOCKING") #debug
                    
                    running.status = "BLOCKED"

                    status_code = "B"
                    simulationTime += 1
                    break
                    #processes.remove(running)     
                
            simulationTime += 1 # increment time by 1
        
        
        if running.remaining_time == 0 and running in processes:
            status_code = "T"
            averageTime += simulationTime
            #print(running.name)
            processes.remove(running)     
        elif running.status == "READY" and running in processes: 
            #print(running.name)
            isIdle = 0
            readyQ.put((-abs(running.priority), running))

        if processName != "(IDLE)":
            timePassed = simulationTime - start
            toPrint = [str(start), processName, str(timePassed), status_code]
            print("\t".join(toPrint)) 

    print("Average turnaround: ", averageTime / 3)    
             
        
        

        
        
def main():
    # total arguments 
    n = len(sys.argv) 
    if n != 4:
        print("Error: Needs 4 arguments!") # error if incorrect input
        sys.exit(1) # code to exit
        
    # arguments
    input_file = sys.argv[1] # first argument - input file name
    time_slice = int(sys.argv[2]) # second argument - decimal integer length of time sclice for round-robin scheduler
    block_duration = int(sys.argv[3]) # third argument - deciaml integer time length that a process is unavailable to run after it blocks
    
    
    # python3 scheduler.py joblist1.txt 10 20
    print("timeSlice:", time_slice, "   blockDuration:", block_duration)
    roundRobin(input_file, time_slice, block_duration)
    

    
    
    
# run
main()
