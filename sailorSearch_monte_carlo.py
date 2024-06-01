"""
Simulation game for a Coast Guard search and rescue effort. Players will use Bayes' Rule to guide decisions to locate
the sailor as quickly as possible. Will use OpenCV and numpy. Searches for the sailor over 3 contiguous search areas.
Displays a mpa, prints a menu of search choices for the user, randomly chooses a location for the sailor & either reveal
the location if a search locates him/her or do a Bayesian update of the probabilities of finding the sailor for each
area.
"""
import sys
import random
import itertools
import numpy as np
import cv2 as cv

# Part 1 - Constants
# The link of the image of the map used for the game
MAP_FILE = 'cape_python.png'

# Define the 3 search areas (UL = upper left & LR = lower right)
SA1_CORNERS = (130, 265, 180, 315) # (UL-X, UL-Y, LR-X, LR-Y)
SA2_CORNERS = (80, 255, 130, 305)
SA3_CORNERS = (105, 205, 155, 255)

COUNT = 0


# Part 2 - Define the search class, the blueprint of the game
class Search():
    """Bayesian Search & Rescue game with 3 search areas."""
    def __init__(self, name):
        self.name = name
        # The image is grayscale so use cv.IMREAD_COLOR to load the image in color mode.
        self.img = cv.imread(MAP_FILE, cv.IMREAD_COLOR)
        # Exit the program if the MAP_FILE variable does not exist
        if self.img is None:
            print('Could not load map file {}'.format(MAP_FILE), file=sys.stderr)
            sys.exit(1)

        # Assign attributes for the sailor's actual location
        self.area_actual = 0 # Number of the search area
        # Precise x,y location
        self.sailor_actual = [0, 0] # As 'local' coords within search area

        # To work with location coords within a search area create a subarray from the array
        self.sa1 = self.img[SA1_CORNERS[1] : SA1_CORNERS[3],
                            SA1_CORNERS[0] : SA1_CORNERS[2]]
        self.sa2 = self.img[SA2_CORNERS[1] : SA2_CORNERS[3],
                            SA2_CORNERS[0] : SA2_CORNERS[2]]
        self.sa3 = self.img[SA3_CORNERS[1] : SA3_CORNERS[3],
                            SA3_CORNERS[0] : SA3_CORNERS[2]]

        # Set the pre search probs for finding the sailor in each area
        self.p1 = 0.2
        self.p2 = 0.5
        self.p3 = 0.3

        # Placeholder attributes for the SEP
        self.sep1 = 0
        self.sep2 = 0
        self.sep3 = 0

        # Part 3 - Create a method that displays the base map
    def draw_map(self, last_known):
        """Display basemap with scale, last knwon xy location, search areas."""
        # Draw a scale bar
        cv.line(self.img, (20, 370), (70, 370), (0, 0, 0), 2)
        # Annotate the scale bar
        cv.putText(self.img, '0', (8, 370), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))
        cv.putText(self.img, '50 Nautical Miles', (71, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        # Draw a rectangle for the 3 search areas
        cv.rectangle(self.img, (SA1_CORNERS[0], SA1_CORNERS[1]),
                               (SA1_CORNERS[2], SA1_CORNERS[3]), (0, 0, 0), 1)
        # Put the search are number inside the upper-left corner of each rectangle
        cv.putText(self.img, '1',
                   (SA1_CORNERS[0] + 3, SA1_CORNERS[1] + 15),
                   cv.FONT_HERSHEY_PLAIN, 1, 0)
        cv.rectangle(self.img, (SA2_CORNERS[0], SA2_CORNERS[1]),
                               (SA2_CORNERS[2], SA2_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '2',
                   (SA2_CORNERS[0] + 3, SA2_CORNERS[1] + 15),
                   cv.FONT_HERSHEY_PLAIN, 1, 0)
        cv.rectangle(self.img, (SA3_CORNERS[0], SA3_CORNERS[1]),
                               (SA3_CORNERS[2], SA3_CORNERS[3]), (0, 0, 0), 1)
        cv.putText(self.img, '3',
                   (SA3_CORNERS[0] + 3, SA3_CORNERS[1] + 15),
                   cv.FONT_HERSHEY_PLAIN, 1, 0)

        # Place '+' at the sailor's last know location
        cv.putText(self.img, '+', (last_known),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '+ = Last Known Position', (274, 355),
                   cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 255))
        cv.putText(self.img, '* = Actual Position', (275, 370),
                   cv.FONT_HERSHEY_PLAIN, 1, (255, 0, 0))

        # Finish method by showing the bass map
        cv.imshow('Search Area', self.img)
        # Force base map to display in the upper right corner of the monitor
        cv.moveWindow('Search Area', 750, 10)
        # Game menu should appear a half second after the base map
        cv.waitKey(500)

    # Part 4 - Method to randomly choose the sailor's actual location
    def sailor_final_location(self, num_search_areas):
        """Return the actual x, y location of the missing sailor"""
        # Find sailor coordinates, since all search areas are the same size
        self.sailor_actual[0] = np.random.choice(self.sa1.shape[1], 1)
        self.sailor_actual[1] = np.random.choice(self.sa1.shape[0], 1)

        # Choose a search area by using the triangular distribution
        area = int(random.triangular(1, num_search_areas + 1))

        if area == 1:
            # Convert search location to global image
            x = self.sailor_actual[0] + SA1_CORNERS[0]
            y = self.sailor_actual[1] + SA1_CORNERS[1]
            # Update to keep track of the search area
            self.area_actual = 1
        elif area == 2:
            # Convert search location to global image
            x = self.sailor_actual[0] + SA2_CORNERS[0]
            y = self.sailor_actual[1] + SA2_CORNERS[1]
            # Update to keep track of the search area
            self.area_actual = 2
        elif area == 3:
            # Convert search location to global image
            x = self.sailor_actual[0] + SA3_CORNERS[0]
            y = self.sailor_actual[1] + SA3_CORNERS[1]
            # Update to keep track of the search area
            self.area_actual = 3
        return x, y

    # Part 5 - Calculating search effectiveness and conducting the search
    def calc_search_effectiveness(self):
        """Set decimal search effectiveness value per search area [random between .2-.9]"""
        self.sep1 = random.uniform(0.2, 0.9)
        self.sep2 = random.uniform(0.2, 0.9)
        self.sep3 = random.uniform(0.2, 0.9)

    # Necessary parameters are the area to search chosen by player, area sub_array and randomly set SEP value
    def conduct_search(self, area_num, area_array, effectiveness_prob, coords_lst):
        """Return search results and list of searched coordinates"""
        local_y_range = range(area_array.shape[0])
        local_x_range = range(area_array.shape[1])
        # Generate list of all coordinates in the search area
        coords = list(itertools.product(local_x_range, local_y_range))
        coords_not_searched = set()
        # Challenge 1 - Now create new coords list that takes into account any already searched areas
        if len(coords_lst) > 0:
            # Changed the below loop to a while loop to be able to break out when the whole SA has already been searched
            i = 0
            # Search through all values in lists of lists so if area is already search
            while i < len(coords_lst):
                search_coords = [x for x in coords if x not in coords_lst[i]]
                for x in search_coords:
                    coords_not_searched.add(x)
                i = i + 1
                # This is an addition to make sure that when a user has fully searched an area they are aware of that
                if len(coords_not_searched) == 2500:
                    # Here then coords_not_searched is all of the coords so attempt to break out of while loop
                    i = len(coords_lst) + 1
                    print("This implies the whole area has already been searched!")
                    break
        else:
            coords_not_searched = coords
        coords_not_searched = list(coords_not_searched)
        # Shuffle to not keep searchin the same end with every search event
        random.shuffle(coords_not_searched)
        # See if there is any area in the new coords list that would not be searched
        lst_len = int((len(coords) * effectiveness_prob))
        if len(coords_not_searched) - lst_len >= 0:
            # Trim the search area based on the SEP value
            coords_not_searched = coords_not_searched[:lst_len]
        loc_actual = (self.sailor_actual[0], self.sailor_actual[1])
        # Check if the sailor was found or not
        if area_num == self.area_actual and loc_actual in coords_not_searched:
            return 'Found in Area {}.'.format(area_num), coords_not_searched
        else:
            return 'Not Found', coords_not_searched

    # Part 6 - Applying Bayes' Rule and drawing a menu
    def revise_target_probs(self):
        """Update area target probabilities based on search effectiveness"""
        denom = self.p1 * (1 - self.sep1) + self.p2 * (1 - self.sep2) + self.p3 * (1 - self.sep3)
        if denom == 0:
            denom = 0.000000001
        self.p1 *= (1 - self.sep1) / denom
        self.p2 *= (1 - self.sep2) / denom
        self.p3 *= (1 - self.sep3) / denom


def draw_menu(search_num):
    """Print menu of choices for conducting search areas"""
    print('\nSearch {}'.format(search_num))
    print(
        """
        Choose next areas to search:
        0 - Quit
        1 - Search Area 1 twice
        2 - Search Area 2 twice
        3 - Search Area 3 twice
        4 - Search Areas 1 & 2
        5 - Search Areas 1 & 3
        6 - Search Areas 2 & 3
        7 - Start Over
        """
    )


# Challenge 2 - Create simulation to choose options 1-3 based on the highest prob.
def monte_carlo_hp(p1, p2, p3):
    """This function will return the choice of options 1-3 based on the highest probability"""
    if p1 >= p2 and p1 >= p3:
        option_choice = "1"
    elif p2 >= p1 and p2 >= p3:
        option_choice = "2"
    elif p3 >= p1 and p3 >= p2:
        option_choice = "3"
    else:
        option_choice = "BROKEN"
    return option_choice


# Basically same as above method just uses joing probability instead of highest
def monte_carlo_jp(p1, p2, p3):
    """This function returns choice of options 4-6 based on the highest joint probability"""
    # Here make joint probabilities then follow same logic as hp monte carlo above
    p1_p2 = p1 + p2
    p2_p3 = p2 + p3
    p1_p3 = p1 + p3
    if p1_p2 >= p2_p3 and p1_p2 >= p1_p3:
        option_choice = "4"
    elif p1_p3 >= p1_p2 and p1_p3 >= p2_p3:
        option_choice = "5"
    elif p2_p3 >= p1_p2 and p2_p3 >= p1_p3:
        option_choice = "6"
    else:
        option_choice = "BROKEN"
    return option_choice


# Part 7 - Define the main function used to run the program
def main(count, num_searches_hp, num_searches_jp):
    # Set a number of simulations variable for challenge 2 (set to 800 for time and due to recursive method limits)
    NUM_SIMULATIONS = 800
    app = Search('Cape_Python')
    # Display the map
    app.draw_map(last_known=(160, 290))
    sailor_x, sailor_y = app.sailor_final_location(num_search_areas=3)
    sailor_y = int(sailor_y)
    sailor_x = int(sailor_x)
    print("-" * 65)
    print("\nInitial Target (P) Probabilities:")
    print("P1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}".format(app.p1, app.p2, app.p3))
    # Keep track of how many searches have been conducted
    search_num = 1

    # For Challenge 1 add list that should keep track of each of the 3 search areas that have been searched
    lst_coords_1 = []
    lst_coords_2 = []
    lst_coords_3 = []

    # Part 8 - Evaluating the menu choices
    while True:
        # Show the menu and have the user play the game
        app.calc_search_effectiveness()
        draw_menu(search_num)
        #choice = input('Choice: ')

        # Challenge 2 - Here split up the simulation runs so that both can be run in same while loop
        if count <= NUM_SIMULATIONS / 2:
            choice = monte_carlo_hp(app.p1, app.p2, app.p3)
            print('Choice: %s' % choice)
        else:
            choice = monte_carlo_jp(app.p1, app.p2, app.p3)
            print('Choice: %s' % choice)

        # Choose to quit game
        if choice == "0":
            sys.exit()
        # Choices 1-3
        elif choice == "1":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1, lst_coords_1)
            # Append the coords searched to the list
            lst_coords_1.append(coords_1)
            results_2, coords_2 = app.conduct_search(1, app.sa1, app.sep1, lst_coords_1)
            # Append the coords searched to the list
            lst_coords_1.append(coords_2)
            # Determine overall sep for both searches on the same area
            app.sep1 = (len(set(coords_1 + coords_2))) / (len(app.sa1)**2)
            app.sep2 = 0
            app.sep3 = 0
        elif choice == "2":
            results_1, coords_1 = app.conduct_search(2, app.sa2, app.sep2, lst_coords_2)
            # Append the coords searched to the list
            lst_coords_2.append(coords_1)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2, lst_coords_2)
            # Append the coords searched to the list
            lst_coords_2.append(coords_2)
            app.sep1 = 0
            # Determine overall sep for both searches on the same area
            app.sep2 = (len(set(coords_1 + coords_2))) / (len(app.sa2) ** 2)
            app.sep3 = 0
        elif choice == "3":
            results_1, coords_1 = app.conduct_search(3, app.sa3, app.sep3, lst_coords_3)
            # Append the coords searched to the list
            lst_coords_3.append(coords_1)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3, lst_coords_3)
            # Append the coords searched to the list
            lst_coords_3.append(coords_2)
            app.sep1 = 0
            app.sep2 = 0
            # Determine overall sep for both searches on the same area
            app.sep3 = (len(set(coords_1 + coords_2))) / (len(app.sa3) ** 2)
        # Choices 4-6 mean the search teams will search 2 areas so no need to recalculate SEP
        elif choice == "4":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1, lst_coords_1)
            lst_coords_1.append(coords_1)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2, lst_coords_2)
            lst_coords_2.append(coords_2)
            app.sep3 = 0
        elif choice == "5":
            results_1, coords_1 = app.conduct_search(1, app.sa1, app.sep1, lst_coords_1)
            lst_coords_1.append(coords_1)
            results_2, coords_2 = app.conduct_search(3, app.sa3, app.sep3, lst_coords_3)
            lst_coords_3.append(coords_2)
            app.sep2 = 0
        elif choice == "6":
            results_1, coords_1 = app.conduct_search(3, app.sa3, app.sep3, lst_coords_3)
            lst_coords_3.append(coords_1)
            results_2, coords_2 = app.conduct_search(2, app.sa2, app.sep2, lst_coords_2)
            lst_coords_2.append(coords_2)
            app.sep1 = 0
        # Reset game and clear map
        elif choice == "7":
            main(count, num_searches_hp, num_searches_jp)
        # Handle invalid input
        else:
            print('That is not a valid choice.', file=sys.stderr)
            continue

        # Part 9 - Finishing and calling main
        # Use Bayes' Rule to update target probs
        app.revise_target_probs()

        print("\nSearch {} Results 1 = {}".format(search_num, results_1), file=sys.stderr)
        print("\nSearch {} Results 2 = {}".format(search_num, results_2), file=sys.stderr)
        print("Search {} Effectiveness (E):".format(search_num))
        print("E1 = {:.3f}, E2 = {:.3f}, E3 = {:.3f}".format(app.sep1, app.sep2, app.sep3))

        # If both searches fail display the updated probabilities
        if results_1 == "Not Found" and results_2 == "Not Found":
            print("\nNew Target Probabilities (P) for Search {}".format(search_num + 1))
            print("p1 = {:.3f}, P2 = {:.3f}, P3 = {:.3f}".format(app.p1, app.p2, app.p3))
        else:
            cv.circle(app.img, (sailor_x, sailor_y), 3, (255, 0, 0), -1)
            cv.imshow("search Area", app.img)
            # Challenge 2 - Make updates for the simulations
            count += 1
            # First half of the simulations use the highest prob MC while the next half use JP
            if count <= NUM_SIMULATIONS / 2:
                num_searches_hp.append(search_num)
            else:
                num_searches_jp.append(search_num)
            # Commented out for this challenge as no reason to wait while running simulations
            #cv.waitKey(1500)
            # Here once set number of simulations is done output the average number of searches for each method
            if count == NUM_SIMULATIONS:
                #print(num_searches)
                avg_search_hp = sum(num_searches_hp) / len(num_searches_hp)
                avg_search_jp = sum(num_searches_jp) / len(num_searches_jp)
                print("Average search for %d simulations highest prob.: %.3f" % (len(num_searches_hp), avg_search_hp))
                print("Average search for %d simulations joint prob.: %.3f" % (len(num_searches_jp), avg_search_jp))
                sys.exit()
            # Recall the recursive method to continuously run main() until count == NUM_SIMULATIONS
            main(count, num_searches_hp, num_searches_jp)
        search_num += 1

"""Challenges:
    Challenge 1 - Change the program to keep track of which coordinates have been searched in conduct_search() until 
    main() is called to restart the game. [COMPLETE]
    
    Steps made to complete:
        - Added variables to hold the lists of coords returned. 
        - Add that variable as a parameter to conduct_search().
        - Loop though the lists and keep track of the coords not searched in coords_not_searched variable.
        - If coords_not_search >= size of the search area, then the search area has already been completely searched. 
    
    Challenge 2 - Run Monte Carlo Simulation to determine if it is better to a) choose menu item 1-3 based on the 
    highest prob or b) choose items 4-6 based on highest combined target probs. Run each group 10,000 times and output
    & compare their average # of searches. [COMPLETE]
    
    Steps made to complete:
        - Create method to choose options 1-3 based on highest prob. and output average number of searches. 
          [monte_carlo_hp] This method selects what choice is made (for the first 400 simulations) when the answer is
          found record the number of searches in the specific list for hp and call that at the end of the program to 
          get the average number of searches.
        - Same is done wrt to the joint probability issue, just use monte_carlo_jp() & num_searches_jp to keep track of
          choices and number of searches and output average number of searches at end of program. 
        - Consensus after running 3 times is that joint probability works better than highest probability, but not by a 
          very large margin. 
        - Also had to update the check for when all of the search area has been searched to stop re-printing the same 
          output. 
    
    Challenge 3 - Calculate the prob of detection (pod = p * sep) for each search option on the menu and output that on 
    the menu, for searching an area twice pod = 1 - (1- pod)^2 [INCOMPLETE]
"""


# Run main
if __name__ == '__main__':
    # Create count, these arguments need to be given to the main() method since the method is recursive
    count = 0
    # Create lists to contain total number of searches for monte carlo simulations
    num_searches_hp = []
    num_searches_jp = []
    # First call to main() that then runs NUM_SIMULATIONS amount of times (I set to 800)
    main(count, num_searches_hp, num_searches_jp)