from typing import Union


class Machine:
    def __init__(self, parent):
        self.parent = parent

    def park_v7(self,
                park_position: Union[int, str] = 3,
                posx: Union[int, float, str] = 0,
                posy: Union[int, float, str] = 0) -> None:
        """
        Machine park position
        :param park_position: Park Value
        :param posx: X Position
        :param posy: Y Position
        :return: None
        """
        park_string = f'CALL Park_V7 ( VAL MODE:={park_position},POSX:={posx},POSY:={posy})'
        self.parent.commands.append(park_string)

    def standard_park_mode(self) -> None:
        """
        Standard Parking ID
        Needs a variable to work
        Variable to insert when initializing the hop file: ParkID=0
        :return: None
        """
        get_s_router_string = "CALL _UserInterface3DG (REF RESULT:=ParkID VAL INPUTTEXT:='GetParkMode')" \
                              f"\nCALL Park_V7 ( VAL MODE:=ParkID,POSX:=0,POSY:=0)"
        self.parent.commands.append(get_s_router_string)
        self.parent.vars['ParkID'] = 0

    def add_measure_quote(self, x: Union[int, str, float] = 25) -> None:
        """
        Add a measure quote for the Evolution Machine
        :return: None
        """
        measure_string = f'CALL HH_MeaQuote ( VAL X:={x})'
        self.parent.commands.append(measure_string)

