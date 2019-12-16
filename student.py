from teacher import PiggyParent
import sys
import time

class Piggy(PiggyParent):

    '''
    *************
    SYSTEM SETUP
    *************
    '''

    def __init__(self, addr=8, detect=True):
        PiggyParent.__init__(self) # run the parent constructor

        ''' 
        MAGIC NUMBERS <-- where we hard-code our settings
        '''
        self.LEFT_DEFAULT = 100
        self.RIGHT_DEFAULT = 100
        #pro Level        
        self.EXIT_HEADING = 0
        self.SAFE_DIST = 250
        self.MIDPOINT = 1500  # what servo command (1000-2000) is straight forward for your bot?

        self.load_defaults()
        

    def load_defaults(self):
        """Implements the magic numbers defined in constructor"""
        self.set_motor_limits(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_limits(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.set_servo(self.SERVO_1, self.MIDPOINT)
        

    def menu(self):
        """Displays menu dictionary, takes key-input and calls method"""
        ## This is a DICTIONARY, it's a list with custom index values. Python is cool.
        # Please feel free to change the menu and add options.
        print("\n *** MENU ***") 
        menu = {"n": ("Navigate", self.nav),
                "d": ("Dance", self.dance),
                "o": ("Obstacle count", self.obstacle_count),
                "V": ("Veer", self.slither),
                "h": ("Hold Position", self.hold_position),
                "c": ("Calibrate", self.calibrate),
                "q": ("Quit", self.quit)
                }
        # loop and print the menu...
        for key in sorted(menu.keys()):
            print(key + ":" + menu[key][0])
        # store the user's answer
        ans = str.lower(input("Your selection: "))
        # activate the item selected
        menu.get(ans, [None, self.quit])[1]()
    '''
    ****************
    STUDENT PROJECTS
    ****************
    '''
    
    def hold_position(self):
        started_at = self.get_heading()
        while True:
            time.sleep(.5)
            current_angle = self.get_heading()
            if abs(started_at - current_angle) > 30:
                self.turn_to_deg(started_at)
    def dance(self):
        #check to see its safe
        if not self.safe_to_dance():
            print("Not cool. No Dance")
            return #return closes method
        else:
            print("Its safe to dance!")
        # print("I don't know how to dance. \nPlease give my programmer a zero.")
        # HIGHER - ORDERED
        for i in range (3):
            self.cool_dance()
            self.moonwalk()
            self.Runningman()
            self.dab()
            #self.sprinkler()
    def safe_to_dance(self):
        """does a 360 check"""
        for i in range(4):
            for ang in range(1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
                if self.read_distance() < 250:
                    return False
            self.turn_by_deg(90)
        return True
            
    def cool_dance(self):	
        """turn right slowly"""
        print("\n COOL DANCE!!! \n")
        for i in range(3):
            self.turn_by_deg(45)
            self.sleep(1)
            self.back(1)
            time.sleep(1)
            self.fwd(1)
            self.servo(2000)
            time.sleep(.5)
            self.servo(1000)
            time.sleep(.5)
            self.stop()
    
    def Runningman(self):
        print("\n ARE YOU READY FOR RUNNING MAN? \n")
        for i in range(3):
            self.back()
            time.sleep(1)
            self.stop()
            self.turn_by_deg(90)
            self.turn_by_deg(120)
            self.back(left=40)
            time.sleep(1)
            self.stop()

    def moonwalk(self):
        """moonwalk backwards in circle"""
        print("\n Let's moonwalk, baybah! \n")
        for i in range(3):
            self.back()
            time.sleep(.5)
            self.back()
            time.sleep(.5)

    def dab(self):
        """servo back and forth"""
        for i in range (3):
            self.servo(2000)
            time.sleep(1)
            self.stop()
            self.servo(1500)
            time.sleep(1)
            self.stop()
    
    def sprinkler(self):
        """servo does sprinkler"""
        for i in range(4):
            for ang in range(1000, 2001, 100):
                self.servo(ang)
                time.sleep(.1)
            self.turn_by_deg(90)


    def scan(self):
        """Sweep the servo and populate the scan_data dictionary"""
        for angle in range(self.MIDPOINT-450, self.MIDPOINT+450, 250):
            self.servo(angle)
            self.scan_data[angle] = self.read_distance()

    def obstacle_count(self):
        """Does a 360 scan and returns the number of obstacles it sees"""
        pass

    def quick_check(self):
        # three quick checks
        for ang in range(self.MIDPOINT-250, self.MIDPOINT+251,250):
            self.servo(ang)
            if self.read_distance() < self.SAFE_DIST:
                return False
            # if I get to the end, this means I didnt find anything dangerous
        return True

    def turn_to_exit(self):
        start = self.get_heading()
        self.turn_to_deg(self.EXIT_HEADING)
        if not self.quick_check():
            self.turn_to_deg(start)
            return False
        return True
    def slither(self):
        """ practice a smooth veer """
        # write down where we started
        starting_direction = self.get_heading()
        # start driving forward
        self.set_motor_power(self.MOTOR_LEFT, self.LEFT_DEFAULT)
        self.set_motor_power(self.MOTOR_RIGHT, self.RIGHT_DEFAULT)
        self.fwd() 
        # throttle down the left motor
        for power in range(self.LEFT_DEFAULT, 30, -10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.5)
        
        # throttle up the left 
        for power in range(30, self.LEFT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_LEFT, power)
            time.sleep(.1)
        # throttle down the right
        for power in range(self.RIGHT_DEFAULT, 30, -10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.5)
        
        # throttle up the right 
        for power in range(30, self.RIGHT_DEFAULT + 1, 10):
            self.set_motor_power(self.MOTOR_RIGHT, power)
            time.sleep(.1)        
        left_speed = self.LEFT_DEFAULT
        right_speed = self.RIGHT_DEFAULT
        
        # straigten out
        while self.get_heading() != starting_direction:
            # if I need to veer right
            if self.get_heading() < starting_direction:
                right_speed -= 10
            # if I need to veer left
            elif self.get_heading() > starting_direction:
                left_speed -= 10
            self.set_motor_power(self.MOTOR_LEFT, left_speed)
            self.set_motor_power(self.MOTOR_RIGHT, right_speed) 
            time.sleep(.1)



    def nav(self):
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("-------- [ Press CTRL + C to stop me ] --------\n")
        print("-----------! NAVIGATION ACTIVATED !------------\n")
        print("Wait a second. \nI can't navigate the maze at all. Please give my programmer a zero.")
        
        corner_count = 3
        self.EXIT_HEADING = self.get_heading()
        
        while True:    
            self.servo(self.MIDPOINT)
            while self.quick_check():
                corner_count = 0
                self.fwd()
                time.sleep(.01)
            self.stop()
            self.scan()
            # turns out of cornoer if stuck
            corner_count += 1
            if corner_count == 3:
                self.turn_by_deg(90)
            
            #check on exit
            current = self.get_heading()
            self.turn_to_exit()
            if not self.quick_check():
                self.turn_to_deg(current)
            else: continue




            #traversal
            left_total = 0
            left_count = 0
            right_total = 0
            right_count = 0
            for ang, dist in self.scan_data.items():
                if ang < self.MIDPOINT: 
                    right_total += dist
                    right_count += 1
                else:
                    left_total += dist
                    left_count += 1
            left_avg = left_total / left_count
            right_avg = right_total / right_count
            if left_avg > right_avg:            
                self.turn_by_deg(-45)
            else:                
                self.turn_by_deg(45)

        # TODO: Average the right side of the scan dict 
    




###########
## MAIN APP
if __name__ == "__main__":  # only run this loop if this is the main file

    p = Piggy()

    if sys.version_info < (3, 0):
        sys.stdout.write("Sorry, requires Python 3.x\n")
        p.quit()

    try:
        while True:  # app loop
            p.menu()

    except KeyboardInterrupt: # except the program gets interrupted by Ctrl+C on the keyboard.
        p.quit()  
