import configparser


class LabelParser:
    def __init__(self, file_path):
        super(LabelParser, self).__init__()
        self.file_path = file_path
        self.lbl = None

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
            with open(self.file_path, 'r', encoding='utf-16') as f:
                self.lbl.read_file(f)  # Use read_file instead of read for file objects

    def label_positions(self) -> list:
        if self.lbl is None:
            self.open_file()  # Open the file if it's not already opened

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
        if self.lbl is None:
            self.open_file()
        return {
            'length': float(self.lbl['Board']['dimx']),
            'width': float(self.lbl['Board']['dimy']),
            'thickness': float(self.lbl['Board']['dimz'])
        }
