import configparser
import smbclient


class LabelParser:
    def __init__(self, server, username, password, file_path):
        super(LabelParser, self).__init__()
        self.server = server 
        self.username = username 
        self.password = password 
        self._register_session()

        self.file_path = file_path
        self.lbl = None

    def _register_session(self) -> None: 
        session = smbclient.register_session(
            server=self.server, 
            username=self.username, 
            password=self.password,
        )

    def open_file(self) -> None:
        """
        Open the file for reading
        Parse it with configparser
        And store it into self.lbl
        Keys are the following:
        ['Global'] = Path to .hop, .lbl and .ups files - For the Nest board
        ['Board'] = Contains information about the Nest board (dimensions, material name... etc.)
        ['Part_#'] = Contains Part information
        ['Rest_#'] = Contains Rest boards information
        """
        if self.lbl is None:
            # Initialize the ConfigParser
            self.lbl = configparser.ConfigParser()
            # Open the file with the correct encoding
            with smbclient.open_file(self.file_path, 'r', encoding='utf-16') as f:
                self.lbl.read_file(f)  # Use read_file instead of read for file objects

    def label_positions(self) -> list:
        self.open_file()

        coordinates_list = []  # A list for storing coordinates
        for key, value in self.lbl.items():
            if key.lower().startswith('part'):
                coordinates_list.append(
                    (
                        int(value['centerposx']),  # Label center position in X
                        int(value['centerposy']),  # Label center position Y
                        int(value['freetext9'].split(',')[1])
                    )
                )
        return coordinates_list

    def board_dimensions(self) -> dict:
        """
        Return board dimensions as float values inside a dictionary
        """
        self.open_file()
        return {
            'length': float(self.lbl['Board']['dimx']),
            'width': float(self.lbl['Board']['dimy']),
            'thickness': float(self.lbl['Board']['dimz'])
        }
    
    def board(self) -> dict: 
        """
        Return the entire board tag
        """
        self.open_file()

        return self.lbl['Board']

    def rest_plates(self) -> dict[str, dict[str, str]]: 
        """
        Return rest plates details from the lbl file 
        :return: dict -> dict[str, dict[str, str]]
        example:  
        {
            Rest_1: {
                syslabelid: 1, 
                name: 'R'
                .
                .
                .
                material: SomeMaterial
            }
        }
        """
        self.open_file()  # Open file if it's not opened

        rests = {}  # Dict to store items
        for key, value in self.lbl.items(): 
            if key.lower().startswith('rest'):  # If they key starts with 'rests' 
                rests[key] = dict(value)  # Rest_1: {rest_keys: rest_values}
        return rests  # Return rests and their values

