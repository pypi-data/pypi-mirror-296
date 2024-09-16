import smbclient
import os
import chardet


class ExtractHopProcessing:
    def __init__(self,
                 server: str = '192.168.100.57',
                 username: str = 'test',
                 password: str = 'test',
                 path_to_file: str = ''):
        self.server = server
        self.username = username
        self.password = password
        self.path_to_file = os.path.join(server, path_to_file)
        self._register_session()
        self.opened_file = self.open_file()
    
    def _register_session(self):
        self.session = smbclient.register_session(
                server=self.server,
                username=self.username,
                password=self.password
                )
        return self.session

    def detect_encoding(self) -> str:
        """
        Detect the file encoding using chardet
        :return: Detected encoding as a string
        """
        with open(self.path_to_file, 'rb') as hfile:
            raw_data = hfile.read()
            result = chardet.detect(raw_data)
            encoding = result['encoding']
            return encoding

    def open_file(self) -> list:
        """
        Open the file for reading using the detected encoding
        :return: List of lines from the file
        """
        encoding = self.detect_encoding()
        with open(self.path_to_file, 'r', encoding=encoding) as hfile:
            contents = hfile.readlines()
            return contents

    def get_processing(self) -> list:
        """
        Returns a list of all the steps in processing after the line START
        :return: list
        """
        contents = self.opened_file
        processing = []

        for i, line in enumerate(contents):
            stripped_line = line.strip()
            if stripped_line == 'START':  # Target lines are after START
                i += 1  # Skip START
                for processing_steps in contents[i:]:  # Target lines - contents[i:]
                    step = processing_steps.strip().lower()
                    if step.startswith('fertigteil') or \
                            step.startswith('call hh_park') \
                            or step.startswith('call hh_meaquote')\
                            or step.startswith('call park_v7'):  # Various lines that are not relevant
                        continue  # continue looping if the condition is met
                    processing.append(processing_steps.strip())  # Append to the initialized list
        return processing

    def get_vars(self) -> dict:
        """
        Gets all the VARS inside the hop file
        :return: Returns a dictionary of values - {VAR: VALUE}
        """
        contents = self.opened_file  # Open the file
        var = {}  # Empty dictionary

        for i, line in enumerate(contents):
            stripped_line = line.strip()
            if stripped_line == 'VARS':  # If the line is VARS
                i += 1  # Skip one line - the line "VARS"
                for var_line in contents[i:]:  # contents[i:] are the target lines
                    if var_line.strip() == 'START':  # Stop when we get to the START string
                        break
                    split_string = var_line.strip().split(':=')  # Strip and get rid of whitespace
                    var_value = split_string[-1].split(';')[0]  # Value of the variable
                    var_name = split_string[0]  # Name of the variable
                    var.update({var_name[0:-1]: var_value[1:]})  # Update the initialized dictionary with keys and values
        return var

    def get_comments(self) -> dict:
        """
        Gets all the comments inside the hop file
        :return:  Dictionary {comment: value}
        """
        contents = self.opened_file  # Open file
        comments = {}  # for storing the VARS
        for i, line in enumerate(contents):
            stripped_line = line.strip()
            if stripped_line.startswith(';'):  # Comments start with a semicolon
                comment = stripped_line.replace(';', '').split('=')
                comments.update({comment[0]: comment[1]})
        return comments

    def vertical_drills(self) -> list:
        """
        Looks for vertical drills and converts coordinates to float or int.
        :return: List of values
        """
        processing = self.get_processing()
        vertical_drills = []
        for process in processing:
            if str(process).lower().startswith('bohrung'):
                process_remove_mm = process.replace('mm', '')
                process_split = process_remove_mm.split('(')
                coordinates = process_split[1]
                values = coordinates.strip('()').split(',')
                converted_values = [float(value) if '.' in value else int(value) for value in values]
                vertical_drills.append(converted_values)
        return vertical_drills

    def horizontal_drills(self) -> list:
        """
        Looks for horizontal drills and converts coordinates to float or int.
        :return: List of values
        """
        processing = self.get_processing()
        horizontal_drills = []
        for process in processing:
            if str(process).lower().startswith('horzb'):
                process_split = process.split('(')
                coordinates = process_split[1]
                values = coordinates.strip('()').split(',')
                converted_values = [float(value) if '.' in value else int(value) for value in values]
                horizontal_drills.append(converted_values)
        return horizontal_drills

    def all_drillings(self) -> dict:
        """
        All drills within the file.
        :return: dictionary - {vertical drills: list of drills, horizontal drills: list of drills}
        """
        vertical = self.vertical_drills()
        horizontal = self.horizontal_drills()
        return {'vertical': vertical, 'horizontal': horizontal}

    def drill_count(self) -> dict:
        """
        Method for getting the number of vertical and horizontal holes
        :return: a dictionary {vertical drills: number of holes, horizontal drills: number of holes}
        """
        get_drills = self.all_drillings()
        vcount = len(get_drills['vertical'])
        hcount = len(get_drills['horizontal'])
        return {'vcount': vcount, 'hcount': hcount}

    def sawing(self) -> list:
        """
        Looks for the sawing macro and converts coordinates to float or int.
        :return: List of values
        """
        processing = self.get_processing()
        sawing_list = []  # initiate empty list
        for process in processing:
            if str(process).lower().startswith('saegen'):  # Look for sawing macro
                process_split = process.split('(')  # first split
                coordinates = process_split[1]
                values = coordinates.strip('()').split(',')  # split into a list and strip () from str
                converted_values = [float(value) if '.' in value else int(value) for value in values]  # str to number
                sawing_list.append(converted_values)
        return sawing_list

    def sawing_length(self) -> float:
        """
        :return: float - sawing length in X
        """
        sawing = self.sawing()
        length = 0
        for saw in sawing:
            length_saw = saw[3] - saw[0]  # X2 - X1
            length += length_saw  # increment length - if there is more than one sawing process
        return length  # return incremented length

    def processes_as_dict(self) -> dict:
        """
        Get all tools, their numbers and their commands
        :return: Dictionary {Tool_Type: {Tool_Number: 0, Tool_Processes: []}}
        """
        content = self.get_processing()
        tool_processes = {}
        current_tool = None

        for line in content:
            line = line.strip()
            if line.lower().startswith('wz'):
                split_line = line.split('(')  # Start of a new tool's processes
                current_tool = split_line[0].strip()
                tool_number = split_line[1].split(',')[0]  # Extract the tool number
                tool_processes[current_tool] = {'tool_no': tool_number, 'processing': []}
            elif current_tool and not line.lower().startswith('wz'):
                # Current line is a process of the current tool
                tool_processes[current_tool]['processing'].append(line)
            elif line.lower().startswith('wz'):
                # Next tool change encountered, reset current_tool
                current_tool = None
        return tool_processes

    def milling_processes(self) -> list[dict]: 
        """
        Get milling processes in a structured list.
        The list will look like this -> 
        [
            {
                'tool_no': int, 
                'milling': [
                    {'sp': [int, float, str], 'process': [{[str]: [list]}], 'ep': [int, float, str]},
                    {'sp': [int, float, str], 'process': [{[str]: [list]}], 'ep': [int, float, str]},
                    ...
                ]
            }
        ]

        :return: A list of dictionaries
        """

        # Get all the processing as lines
        content = self.get_processing() 

        # A dictionary to store tool processes by tool number
        tools_dict = {}

        # A variable to track the current tool number
        current_tool_no = None

        # A flag to indicate if we're processing a milling line
        milling_line = False
        for line in content: 

            # Strip the lines 
            line = line.strip()

            # If we have hit a wzf (new tool)
            if line.lower().startswith('wzf'): 
                # Get the tool number
                current_tool_no = int(line.split('(')[1][0:-1].split(',')[0])

                # Initialize the tool entry if it doesn't exist
                if current_tool_no not in tools_dict:
                    tools_dict[current_tool_no] = {'tool_no': current_tool_no, 'milling': []}

            # If we hit a start point (SP)
            if line.lower().startswith('sp'): 
                # Initialize a new milling process
                new_process = {'sp': [], 'process': [], 'ep': []}

                # Parse the SP line and add to the new process
                for m in line.split('(')[1][0:-1].split(','):
                    try:
                        if '.' in m:
                            new_process['sp'].append(float(m))
                        else:
                            new_process['sp'].append(int(m))
                    except ValueError:
                        new_process['sp'].append(m)  # Keep as string if it can't be converted

                # Set the milling_line flag to true
                milling_line = True

            # If we hit a G01 process line and we're inside a milling line
            elif milling_line and line.lower().startswith('g01'):
                # Parse the G01 line and add to the process
                process_name = line.split('(')[0]
                process_values = []
                for pr in line.split('(')[1][0:-1].split(','):
                    try:
                        if '.' in pr:
                            process_values.append(float(pr))
                        else:
                            process_values.append(int(pr))
                    except ValueError:
                        process_values.append(pr)  # Keep as string if it can't be converted

                # Append the process to the new process list
                new_process['process'].append({process_name: process_values})  # type: ignore

            # If we hit an end point (EP)
            elif milling_line and line.lower().startswith('ep'):
                # Parse the EP line and add to the new process
                for eep in line.split('(')[1][0:-1].split(','):
                    try:
                        if '.' in eep:
                            new_process['ep'].append(float(eep))  # type: ignore
                        else:
                            new_process['ep'].append(int(eep))  # type: ignore
                    except ValueError:
                        new_process['ep'].append(eep)  # type: ignore - Keep as string if it can't be converted

                # Append the completed milling process to the tool's milling list
                tools_dict[current_tool_no]['milling'].append(new_process)  # type: ignore

                # Reset the milling_line flag
                milling_line = False

        # Convert the dictionary back to a list of processes
        tool_processes = list(tools_dict.values())

        # Return the list with the values
        return tool_processes

