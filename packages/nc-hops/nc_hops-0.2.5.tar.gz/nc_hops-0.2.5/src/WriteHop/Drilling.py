from typing import Union


class Drilling:
    def __init__(self, parent):
        self.parent = parent

    def add_tool(self, tool_no: int) -> None:
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
        30=holes with diameter > 10mm (hinges camlocks etc.)
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
              biy: Union[int, float, str] = 32,
              biiy: Union[int, float, str] = 32,
              biiiy: Union[int, float, str] = 32,
              biiiiy: Union[int, float, str] = 32,
              z: Union[int, float, str] = 9,
              spiegeln: Union[int, float, str] = 0,
              t: Union[int, float, str] = -13,
              d: Union[int, float, str] = 8,
              ebene: Union[int, float, str] = 0,
              increment: Union[int, float, str] = 0, 
              esy: Union[int, str] = 3,
              esz: Union[int, str] = 2, 
              use2: Union[int, str] = 0,
              use3: Union[int, str] = 0,
              use4: Union[int, str] = 0,
              baktiv: Union[int, str] = 1,
              laktiv: Union[int, str] = 0,
              daktiv: Union[int, str] = 0,
              dueba: Union[int, str] = 0,
              leimz: Union[int, str, float] = 0.5, 
              duebl: Union[int, str] = 25, 
              num1: Union[int, str] = 0, 
              num2: Union[int, str] = 0, 
              str1: Union[int, str] = '',) -> None:
        """
        Dowel drilling and insertion macro
        :param biy: Only can be drilled on the DY so this is the starting Y position
        :param biiy: Second drill
        :param biiiy: Third drill
        :param biiiiy: Fourth drill
        :param z: Z position
        :param spiegeln: mirror 
        :param t: depth 
        :param d: diameter 
        :param ebene: Side - 0=left, 1=right
        :param increment: Increment
        :param esy:
        :param esz:
        :param use1:
        :param use2:
        :param use3:
        :param use4: 
        :param baktiv: activate drill=1, disable drill=0
        :param laktiv: activate, disable=0
        :param daktiv: activate, disable=0
        :param dueba: The length of the dowel
        :param leitz: 
        :param duebl: 
        :param num1:
        :param num2:
        :param str1:
        :return: None
        """

        hh_dowel_string = f'CALL HH_DowelGr_HY ( VAL ' \
                          f'BIY:={biy},' \
                          f'BIIY:={biiy},' \
                          f'BIIIY:={biiiy},' \
                          f'BIIIIY:={biiiiy},' \
                          f'Z:={z},' \
                          f'SPIEGELN:={spiegeln},' \
                          f'T:={t},' \
                          f'D:={d}mm,' \
                          f'EBENE:={ebene},' \
                          f'INKREMENT:={increment},' \
                          f'ESY:={esy},' \
                          f'ESZ:={esz},' \
                          f'USE2:={use2},' \
                          f'USE3:={use3},' \
                          f'USE4:={use4},' \
                          f'BAKTIV:={baktiv},' \
                          f'LAKTIV:={laktiv},' \
                          f'DAKTIV:={daktiv},' \
                          f'DUEBA:={dueba},' \
                          f'LEIMZ:={leimz},' \
                          f'DUEBL:={duebl},' \
                          f'NUM1:={num1},' \
                          f'NUM2:={num2},' \
                          f'STR1:={str1})'
        self.parent.commands.append(hh_dowel_string)

