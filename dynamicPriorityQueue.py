class Dynamicqueue():
    #priority should be a tuple in order of most to least important
    def __init__(self):
        self.queue = [[],[]]

    #items added to the queue must begin with a priority and a string
    def enQueue(self, item):
        priority = item[1]

        if not(self.queue): #if queue is empty append to
           self.queue[0].append(item[0])
           self.queue[1].append(priority)
        else: #if not iterate until lower value item found. Then, insert the move
            for index, value in enumerate(self.queue[1]):
                move, value = value
                if priority < value:
                    self.queue[1].insert(index, priority)
                    self.queue[0].insert(index, item[0])
                    return "ITEM ADDED"
                
            #if lowest priority append the move to the end
            self.queue[0].append(item[0])
            self.queue[1].append(priority)
            return "ITEM ADDED"

    #returns and remopves first index 
    def deQueue(self):
        if self.queue:
            item = self.queue[0][0] #gets the move

            self.queue[0] = self.queue[0][1:] #replace the queue with everything to the right
            self.queue[1] = self.queue[1][1:]

            return item

        else:
            return None
    
    def get_moves(self):
        return self.queue[0]
    
    def print_values(self):
        print(f"queue: {self.queue[0]}")
