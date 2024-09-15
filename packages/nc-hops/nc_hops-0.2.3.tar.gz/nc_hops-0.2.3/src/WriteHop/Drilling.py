from typing import Union


class Drilling:
    def __init__(self, parent):
        self.parent = parent

    def add_tool(self, tool_no: Union[int]) -> None:
        """
        Call drilling tools
        :param tool_no: tool number
        :return: None
        """
        tool_call_string = f"WZB ({tool_no},_VE,_V,_VA,_SD,_ANF,'51')"
        self.parent.commands.append(tool_call_string)

    def call_501(self) -> None:
        """
        Call drilling head 501 - most common drilling tool
        :return: None
        """
        tool_call_string = "WZB (501,_VE,_V,_VA,_SD,_ANF,'51')"
        self.parent.commands.append(tool_call_string)

    def vertical(self,
                 x: Union[int, float, str],
                 y: Union[int, float, str],
                 diameter: Union[int, float, str],
                 depth: Union[int, float, str],
                 cycle: Union[int, float, str]) -> None:
        """
        Vertical drilling method
        :param x: Position X
        :param y: Position Y
        :param diameter: Hole diameter
        :param depth: Hole depth
        :param cycle: Hole cycle- 10, 20, 30 ...
        10=Dowel holes
        20=Through holes,
        30=holes with diameter > 10mm (hinges etc.)
        :return: None
        """
        v_drill_string = f'Bohrung ({x},{y},{diameter}mm,{depth},{cycle},0,0,0,0,0,0,0)'
        self.parent.commands.append(v_drill_string)

    def horizontal(self,
                   x: Union[int, float, str],
                   y: Union[int, float, str],
                   z: Union[int, float, str],
                   diameter: Union[int, float, str],
                   depth: Union[int, float, str],
                   rotation_angle: Union[int, float, str],
                   ) -> None:
        """
        Horizontal drilling macro
        :param x: Position X
        :param y: Position Y
        :param z: Position Z
        :param diameter: Hole diameter
        :param depth: Hole diameter
        :param rotation_angle: Hole rotation angle - 0, 90, 180, 270
        :return:
        """
        h_drill_string = f'HorzB ({x},{y},{z},{diameter},{depth},0,0,{rotation_angle},0,2,0,0)'
        self.parent.commands.append(h_drill_string)

    def dowel(self,
              position: Union[int, float, str],
              z: Union[int, float, str],
              depth: Union[int, float, str],
              diameter: Union[int, float, str],
              side: Union[int, float, str],
              drill_active: Union[int, float, str],
              glue_active: Union[int, float, str],
              dowel_active: Union[int, float, str],
              dowel_length: Union[int, float, str]) -> None:
        """
        Dowel drilling and insertion macro
        :param position: Only can be drilled on the DY so this is the Y position
        :param z: Z position
        :param depth: Depth of the hole
        :param diameter: Diameter of the hole
        :param side: Side - 0=left, 1=right
        :param drill_active: activate drill=1, disable drill=0
        :param glue_active: glue active=1, disable glue=0
        :param dowel_active: dowel insertion active=1, disable=0
        :param dowel_length: The length of the dowel
        :return: None
        """

        hh_dowel_string = f'CALL HH_DowelGr_HY ( VAL ' \
                          f'BIY:={position},' \
                          f'BIIY:=32,' \
                          f'BIIIY:=32,' \
                          f'BIIIIY:=32,' \
                          f'Z:={z},' \
                          f'SPIEGELN:=0,' \
                          f'T:={depth},' \
                          f'D:={diameter}mm,' \
                          f'EBENE:={side},' \
                          f'INKREMENT:=0,' \
                          f'ESY:=3,' \
                          f'ESZ:=2,' \
                          f'USE2:=0,' \
                          f'USE3:=0,' \
                          f'USE4:=0,' \
                          f'BAKTIV:={drill_active},' \
                          f'LAKTIV:={glue_active},' \
                          f'DAKTIV:={dowel_active},' \
                          f'DUEBA:=12,' \
                          f'LEIMZ:=0.5,' \
                          f'DUEBL:={dowel_length},' \
                          f'NUM1:=0,' \
                          f'NUM2:=0,' \
                          f'STR1:=\'\')'
        self.parent.commands.append(hh_dowel_string)
