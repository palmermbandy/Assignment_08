#------------------------------------------#
# Title: CD_Inventory.py
# Desc: Assignnment 08 - Working with classes
# Change Log: (Who, When, What)
# DBiesinger, 2020-Jan-01, Created file
# DBiesinger, 2020-Jan-01, added pseudocode to complete assignment 08
# PBandy, 2020-Sep-02, Added __init__ to CD class
# PBandy, 2020-Sep-02, Added code to FileIO class
# PBandy, 2020-Sep-02, Added DataProcessor class
# PBandy, 2020-Sep-02, Added code to IO class
# PBandy, 2020-Sep-02, Added getters/setters to CD class
# PBandy, 2020-Sep-02, Added main script body
#------------------------------------------#

from os import path
import pickle
import sys

# -- DATA -- #
str_choice = '' # User input
list_of_cds = []  # list of dicts to hold data
dict_row = {}  # dict of data row
str_file_name = 'CDInventory.dat'  # binary data storage file
obj_file = None  # file object

class CD(object):
    """Stores data about a CD:

    properties:
        - cd_id: (int) with CD ID
        - cd_title: (string) with the title of the CD
        - cd_artist: (string) with the artist of the CD
    methods:
        - None.
    """
    def __init__(self, cd_id = 0, cd_title = None, cd_artist = None):
        self.cd_id = cd_id
        self.cd_title = cd_title
        self.cd_artist = cd_artist

    # Create cd_id getter property
    @property
    def cd_id(self):
        return int(self.__cd_id)

    # Create cd_id setter property
    @cd_id.setter
    def cd_id(self, value):
        if value == None:
            self.__cd_id = value
        elif type(value) != int:
            try:
                self.__cd_id = int(value)
            except Exception as e:
                print('cd_id must be convertable to an int\n', e)
        else:
            self.__cd_id = value

    # Create cd_title getter property
    @property
    def cd_title(self):
        return self.__cd_title

    # Create cd_title setter property
    @cd_title.setter
    def cd_title(self, value):
        if value == None:
            self.__cd_title = value
        elif value == '':
            raise Exception('cd_title cannot be an empty string')
        else:
            self.__cd_title = value

    # Create cd_artist getter property
    @property
    def cd_artist(self):
        return self.__cd_artist

    # Create cd_artist setter property
    @cd_artist.setter
    def cd_artist(self, value):
        if value == None:
            self.__cd_artist = value
        elif value == '':
            raise Exception('cd_artist cannot be an empty string')
        else:
            self.__cd_artist = value


# -- PROCESSING -- #
class FileIO:
    """Processes data to and from file:

    properties:
        - None.

    methods:
        - save_inventory(file_name, table): -> None
        - load_inventory(file_name, table): -> (a list of CD objects)

    """
    # Code to process data from a file
    @staticmethod
    def load_inventory(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            - file_name (string): name of file used to read the data from
            - table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            - table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        """
        # Clear out existing data and load file data anew
        if table:
            table = []

        try:
            with open(file_name, 'rb') as obj_file:
                table = pickle.load(obj_file)
            return table
        except FileNotFoundError as e:
            print(f'No file named {file_name} was found.\n', e)
        except EOFError:
            table = []
            return table

    # Code to process data to a file
    @staticmethod
    def save_inventory(file_name, table):
        """Function to write data from a list of dictionaries to a file

        Reads in data from 2D table (list of dicts) identified by 'table' argument.

        Args:
            - file_name (string): name of file to which to write the data
            - table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            - None.
        """
        try:
            with open(file_name, 'wb') as obj_file:
                pickle.dump(table, obj_file)
        except PermissionError as e:
            print('Insufficient permissions to write to file:\n', e)
        except IOError as e:
            print('Error writing to file:\n', e)

    @staticmethod
    def initiate_cd_inventory():
        """ Function to create the CDInventory.dat file if it doesn't exist.

        Args: 
            - None

        Returns: 
            - None
        """
        if not path.exists(str_file_name):
            obj_file = open(str_file_name, 'wb')
            obj_file.close()


class DataProcessor:
    """Class to process CD data in memory.

    properties:
        - None.
    methods:
        - append_row_to_table(cd_object, list_of_cds): -> None
        - delete_row_from_table(list_of_cds, id_to_delete): -> None
        - generate_new_id(list_of_cds): -> generated_id (str)
    """
    @staticmethod
    def append_row_to_table(cd_object, list_of_cds):
        """Function to append a dictionary to a list

        Args:
            - cd_object (): 
            - list_of_cds (list): A list of dicts that represents a collection of rows of CD data
        
        Returns:
            - None.
        """
        dict_row = {'id' : cd_object.cd_id, 'title' : cd_object.cd_title, 'artist' : cd_object.cd_artist}
        list_of_cds.append(dict_row)

    @staticmethod
    def delete_row_from_table(list_of_cds, id_to_delete):
        """Function to delete a row by ID from the in-memory table

        Args: 
            - list_of_cds (list): A list of dicts that represents a collection of rows of CD data
            - id_to_delete (string): The numerical ID that represents the row of CD data to delete
        
        Returns: 
            - None.
        """
        
        # There shouldn't be any duplicate entries in the file unless it has been
        # modified outside of this program, which I am not trying to handle at this stage
        # of the program, so this delete function will not delete duplicates reliably.
        for count, row in enumerate(list_of_cds):
            if str(row['id']) == str(id_to_delete):
                del list_of_cds[count]
                print('Deleted ID #{}'.format(id_to_delete))
                break

    @staticmethod
    def generate_new_id(list_of_cds):
        """Function to automatically generate a new ID for CD entries.
        Prevents duplicate IDs to enable simpler processing when deleting entries.
        This only prevents duplicates and therefore assumes there are no existing duplicates.

        Args:
            - list_of_cds (list): A list of dicts that represents a collection of rows of CD data

        Returns: 
            - generated_id (string): A newly generated, unique ID
        """
        current_ids = []
        # Check if there's anything in list_of_cdse
        if list_of_cds:
            # If there are values in list_of_cds, iterate through them
            for row in list_of_cds:
                # We're only interested in the ID of each row here. Let's store it in a variable.
                row_id = int(row['id'])
                # Now append each ID into a list of 'current_ids'
                current_ids.append(row_id)
            # Once we have the list of current_ids, let's grab the max ID
            max_id = max(current_ids)
            # ...and add 1 to the max_id to get our next ID.
            generated_id = max_id + 1
        # If list_of_cds was empty, we can just start with '1' as the ID.
        else: 
            generated_id = 1
        return generated_id

# -- PRESENTATION (Input/Output) -- #
class IO:
    """Class for handling Input / Output

    properties:
        - None.

    methods:
        - print_menu(): -> None
        - menu_choice(): -> choice (str)
        - show_inventory(table): -> None
        - ask_user_for_input(): -> str_title (str), str_artist (str)
        - request_id_to_delete(): -> id_to_delete (str)
    """

    # Code to show menu to user
    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            - None.

        Returns:
            - None.
        """
        print('Menu\n\n[l] Load Inventory from File\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] Delete CD from Inventory\n[s] Save Inventory to File\n[x] Exit\n')

    # Code to captures user's choice
    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            - None.

        Returns:
            - choice (string): a lower case string of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    # Code to display the current data on screen
    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            - table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            - None.

        """
        print()
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        try:
            if table:
                for row in table:
                    print('{}\t{} (by: {})'.format(*row.values()))
        except Exception as e:
            print('Error: ', e)
        print('======================================')
        print()

    # Code to get CD data from user
    @staticmethod
    def ask_user_for_input():
        """Function to ask user for inputs, validate them, and return them.

        Args: 
            - None

        Returns: 
            - str_title (string): The Title of the CD
            - str_artist (string): The Artist of the CD
        """
        invalidCharacters = ['"',',']
        try:
            str_title = input('What is the CD\'s title? ').strip()
            for i in str_title:
                if i in invalidCharacters:
                    raise ValueError
            str_artist = input('What is the Artist\'s name? ').strip()
            for i in str_artist:
                if i in invalidCharacters:
                    raise ValueError
            return str_title, str_artist
        except KeyboardInterrupt as e:
            print('Program Manually Exited', e)
        except ValueError as e:
            print('The following characters are not allowed: {}{}'.format(invalidCharacters[0], invalidCharacters[1]))
            print(e)
            sys.exit()

    @staticmethod
    def request_id_to_delete():
        """Function to ask user which CD ID to delete. It also validates
        whether the ID is valid for deletion by confirming that it is an integer.

        Args:
            - None

        Returns:
            - id_to_delete (string): The ID of the CD to delete.
        """
        try:
            # Nested conversion to int validates the input is an integer.
            id_to_delete = int(input('Which ID would you like to delete? ').strip())
            # But I prefer that this be a string, so convert it back
            id_to_delete = str(id_to_delete)
            return id_to_delete
        # If input is not an integer, catch and handle the ValueError
        except ValueError as e:
            print('Uh-oh! Please enter an integer for the ID.\n', e)
            input('Press [ENTER] to return to menu:')

# -- Main Body of Script -- #

# Load data from file into a list of CD objects on script start
FileIO.initiate_cd_inventory()
list_of_cds = FileIO.load_inventory(str_file_name, list_of_cds)

# Instantiate CD object
cd_data = CD()

while True:
    # Display Menu to user and store user input
    IO.print_menu()
    str_choice = IO.menu_choice()

    # Let user exit program
    if str_choice == 'x':
        break
    if str_choice == 'l':
        # Let user load inventory from file
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('Type \'yes\' to continue and reload from file. Otherwise, reload will be canceled: ')
        if strYesNo.lower().strip() == 'yes':
            print('Reloading...')
            list_of_cds = FileIO.load_inventory(str_file_name, list_of_cds)
            IO.show_inventory(list_of_cds)
        else:
            input('Canceling... Inventory data not reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(list_of_cds)
        continue
    # Let user add data to the inventory
    elif str_choice == 'a':
        # Using this ensures that executing this block will always add a unique ID,
        # so we don't need to ask the user for one
        
        cd_data.cd_id = DataProcessor.generate_new_id(list_of_cds)
        
        cd_data.cd_title, cd_data.cd_artist = IO.ask_user_for_input()
        
        # 3.3.2 Add item to the table
        DataProcessor.append_row_to_table(cd_data, list_of_cds)
        print()
        IO.show_inventory(list_of_cds)
        print()
        continue
    # Show user current inventory
    elif str_choice == 'i':
        IO.show_inventory(list_of_cds)
        continue
    # Let user save inventory to file
    elif str_choice == 's':
        IO.show_inventory(list_of_cds)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            FileIO.save_inventory(str_file_name, list_of_cds)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue
    elif str_choice == 'd':
        # Display Inventory to user
        IO.show_inventory(list_of_cds)
        # Ask user which ID to remove
        strIdDel = IO.request_id_to_delete()
        # Search through the table and delete CD
        DataProcessor.delete_row_from_table(list_of_cds, strIdDel)
        IO.show_inventory(list_of_cds)
        continue

