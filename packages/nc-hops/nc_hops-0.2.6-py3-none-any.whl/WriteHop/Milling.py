import random
from typing import Union, List


class Milling:
    def __init__(self, parent):
        self.parent = parent

    def comment(self, comment: Union[str]) -> None:
        """
        Group a milling process by giving it a comment
        :param comment: String
        :return: None
        """
        mill_comment = f';$F${comment}'
        self.parent.commands.append(mill_comment)

    def get_standard_router_id(self) -> None:
        """
        Get tool ID that's been defined as Standard for milling in Hops
        If there's a standard milling tool it needs to be called through VARS
        Add a variable called ToolID and set the value to 0
        Like the following - ToolID := 0;
        :return: None
        """
        get_s_router_string =\
            "CALL _UserInterface3DG (REF RESULT:=StandardToolID VAL INPUTTEXT:='GetStandardRouterID')" \
            "\nWZF (_Router_Standard_ID,_VE,_V,_VA,_SD,_ANF,'1')"

        self.parent.commands.append(get_s_router_string)
        self.parent.vars['StandardToolID'] = 0

    def get_special_router_id(self) -> None:
        """
        Get tool ID that's been defined as Special for milling in Hops
        If there's a standard milling tool it needs to be called through VARS
        Add a variable called ToolID and set the value to 0
        Like the following - ToolID := 0;
        :return: None
        """
        get_special_router_string =\
            "CALL _UserInterface3DG (REF RESULT:=SpecialToolID VAL INPUTTEXT:='GetSpecialRouterID')" \
            "\nWZF (_Router_Special_ID,_VE,_V,_VA,_SD,_ANF,'1')"

        self.parent.commands.append(get_special_router_string)
        self.parent.vars['SpecialToolID'] = 0

    def rectangle_pocket(self,
                         x_center: Union[int, float, str] = 300,
                         y_center: Union[int, float, str] = 200,
                         pocket_length: Union[int, float, str] = 300,
                         pocket_height: Union[int, float, str] = 200,
                         radius: Union[int, float, str] = 0,
                         winkel: Union[int, float, str] = '0.0',
                         depth: Union[int, float, str] = 0,
                         zustellung: Union[int, float, str] = '0.0',
                         ab: Union[int, float, str] = 1,
                         abf: Union[int, float, str] = '_ANF',
                         interpol: Union[int, float, str] = 1,
                         umkehren: Union[int, float, str] = 0,
                         esxy: Union[int, float, str] = 1,
                         esmd: Union[int, float, str] = 0,
                         laser: Union[int, str] = 0) -> None:
        """
        Rectangular pocketing macro
        :param x_center: Pocket center in X
        :param y_center: Pocket center in Y
        :param pocket_length: Pocket length
        :param pocket_height: Pocket height/width
        :param radius: Pocket radius
        :param depth: Pocket depth
        :param zustellung: Zustellung
        :param winkel: angle
        :param ab: AB
        :param abf: ABF
        :param interpol: interpolation
        :param umkehren: umkehren
        :param esxy: coordinate position
        :param esmd: esmd
        :param laser: laser on off
        :return: None
        """
        pocket_string = f'CALL _RechteckTasche_V5' \
                        f' ( VAL X_MITTE:={x_center},' \
                        f'Y_MITTE:={y_center},' \
                        f'TASCHENLAENGE:={pocket_length},' \
                        f'TASCHENBREITE:={pocket_height},' \
                        f'RADIUS:={radius},' \
                        f'WINKEL:={winkel},' \
                        f'TIEFE:={depth},' \
                        f'ZUSTELLUNG:={zustellung},' \
                        f'AB:={ab},' \
                        f'ABF:={abf},' \
                        f'INTERPOL:={interpol},' \
                        f'UMKEHREN:={umkehren},' \
                        f'ESXY:={esxy},' \
                        f'ESMD:={esmd},' \
                        f'LASER:={laser})'
        self.parent.commands.append(pocket_string)

    def rectangle_ramp(self,
                       x_center: Union[int, float, str] = 0,
                       y_center: Union[int, float, str] = 0,
                       ramp_length: Union[int, float, str] = 300,
                       ramp_height: Union[int, float, str] = 300,
                       ramp_radius: Union[int, float, str] = 0,
                       winkel: Union[int, float, str] = 0,
                       depth: Union[int, float, str] = 0,
                       zutiefe: Union[int, float, str] = '_AT_MAXDEPTH',
                       ramp_correction: Union[int, float, str] = 0,
                       ab: Union[int, str] = 0,
                       aufmass: Union[int, str] = 0,
                       anf: Union[int, str] = '_ANF',
                       abf: Union[int, str] = '_ANF',
                       umkehren: Union[int, str] = 0,
                       rampe: Union[int, str] = 0,
                       rampenlaenge: Union[int, str] = 0,
                       quadrant: Union[int, str] = 1,
                       interpol: Union[int, str] = 0,
                       esxy: Union[int, str] = 9,
                       esmd: Union[int, str] = 0,
                       laser: Union[int, str] = 0
                       ) -> None:
        """
        Rectangle ramp - Rectangle cut through macro
        :param x_center: Ramp center in X
        :param y_center: Ramp center in Y
        :param ramp_length: Ramp length
        :param ramp_height: Ramp height/width
        :param ramp_radius: Ramp radius if there should be one
        :param winkel: Angle if there is any
        :param depth: Ramp depth
        :param zutiefe: Max depth
        :param ramp_correction: Ramp correction 0=Center, 1=Outside, 2=Inside
        :param ab:
        :param aufmass:
        :param anf:
        :param abf:
        :param umkehren:
        :param rampe:
        :param rampenlaenge:
        :param quadrant:
        :param interpol:
        :param esxy: Side - global xy position
        :param esmd:
        :param laser:
        :return: None
        """
        ramp_string = f"CALL _Rechteck_V7" \
                      f" ( VAL X_MITTE:={x_center}," \
                      f"Y_MITTE:={y_center}," \
                      f"LAENGE:={ramp_length}," \
                      f"BREITE:={ramp_height}," \
                      f"RADIUS:={ramp_radius}," \
                      f"WINKEL:={winkel}," \
                      f"TIEFE:={depth}," \
                      f"ZUTIEFE:={zutiefe}," \
                      f"RADIUSKORREKTUR:={ramp_correction}," \
                      f"AB:={ab}," \
                      f"AUFMASS:={aufmass}," \
                      f"ANF:={anf}," \
                      f"ABF:={abf}," \
                      f"UMKEHREN:={umkehren}," \
                      f"RAMPE:={rampe}," \
                      f"RAMPENLAENGE:={rampenlaenge}," \
                      f"QUADRANT:={quadrant}," \
                      f"INTERPOL:={interpol}," \
                      f"ESXY:={esxy}," \
                      f"ESMD:={esmd}," \
                      f"LASER:={laser})"
        self.parent.commands.append(ramp_string)

    def vertical_line(self,
                      x: Union[int, float, str],
                      z: Union[int, float, str]) -> None:
        """
        Quick method for a vertical milling path
        :param x: Position X
        :param z: Z/Depth
        :return: None
        """
        self.start_point(x, 0, z)
        self.g_one(x, self.parent.dy, 0)
        self.end_point()

    def horizontal_line(self,
                        y: Union[int, float, str],
                        z: Union[int, float, str]) -> None:
        """
        Quick method for a horizontal milling path
        :param y: Position Y
        :param z: Z/Depth
        :return: None
        """
        self.start_point(0, y, z)
        self.g_one(self.parent.dx, y, 0)
        self.end_point()

    def add_tool(self, tool_no: Union[int, str]) -> None:
        """
        :param tool_no: add a milling tool number before milling
        :return: None
        """
        tool_string = f"WZF ({tool_no},_VE,_V,_VA,_SD,_ANF,'1')"
        self.parent.commands.append(tool_string)

    def start_point(self,
                    x: Union[int, float, str],
                    y: Union[int, float, str],
                    z: Union[int, float, str]) -> None:
        """
        Add a start point to a milling path
        Must have a tool chosen before initiation
        :param x: X Position
        :param y: Y Position
        :param z: Z Position
        :return: None
        """
        sp_string = f"SP ({x},{y},{z},0,1,_ANF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)"
        self.parent.commands.append(sp_string)

    def end_point(self) -> None:
        """
        Linear lead out End point.
        If there shouldn't be a lead out the first parameter of the EP function should be 0
        0=No lead out
        1=Linear lead out
        2=Radial lead out
        :return: None
        """
        ep_string = "EP (1,_ANF,0)"
        self.parent.commands.append(ep_string)

    def g_one(self,
              x: Union[int, float, str],
              y: Union[int, float, str],
              z: Union[int, float, str]) -> None:
        """
        G01 shouldn't be used before making a start point
        An end point is expected after the last line in the milling path
        :param x: X Position
        :param y: Y Position
        :param z: Z Position
        :return: None
        """
        g_one_string = f"G01 ({x},{y},{z},0,0,2)"
        self.parent.commands.append(g_one_string)

    def vert_varied_depths(self,
                           x: Union[int, float, str],
                           depths: List[Union[int, float]]) -> None:
        """
        Vertical line with multiple depths
        :param x: Position X
        :param depths: desired depths- must be values in a list with at least 2 values
        :return:
        """
        num_depths = len(depths)
        dy_segments = [self.parent.dy * (i / (num_depths - 1)) for i in range(num_depths)]
        # Construct the command string
        self.comment('Kanelura')
        vertical_line_string = (
            f"SP ({x},0,{depths[0]},0,1,_ANF,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0)")

        for i in range(1, num_depths):
            vertical_line_string += f"\nG01 ({x},{dy_segments[i]},{depths[i]},0,0,2)"

        vertical_line_string += "\nEP (1,_ANF,0)"
        self.parent.commands.append(vertical_line_string)

    def execute_pocket_outlines_v5(
            self,
            name: str = '',
            aa: Union[int, str] = 0,
            overlap: Union[int, str] = 67,
            mode: Union[int, str] = 0,
            angle: Union[int, str, float] = 0,
            depth: Union[int, str, float] = 0,
            esmd: Union[int, str] = 0,
            number: Union[int, str] = 0,
            maxz: Union[int, str, float] = '_AT_MAXDEPTH',
            rd: Union[int, str] = 0,
            fliegendeintauchen: Union[int, str] = 0,
            maxeintauchlaenge: Union[int, str, float] = 20) -> None:
        """
        Pocketing for contours. NAMEN- name is the name of the first dot (KB) in the contour that needs to be
        pocketed.
        Returns None, appends the command to the commands list in the WriteHop.py file.
        """

        pocket_string = f"CALL _ExecutePocket_V5 ( VAL " \
                        f"NAMEN:='{name}'," \
                        f"AA:={aa}," \
                        f"UEBERLAPPUNG:={overlap}," \
                        f"MODE:={mode}," \
                        f"ANGLE:={angle}," \
                        f"TIEFE:={depth}," \
                        f"ESMD:={esmd}," \
                        f"ANZAHL:={number}," \
                        f"MAXZ:={maxz}," \
                        f"RD:={rd}," \
                        f"FLIEGENDEINTAUCHEN:={fliegendeintauchen}," \
                        f"MAXEINTAUCHLAENGE:={maxeintauchlaenge})"
        self.parent.commands.append(pocket_string)

    @staticmethod
    def generate_positions(dx: Union[int],
                           min_dist: Union[int],
                           num_lines: Union[int],
                           line_width: Union[int]) -> List[int]:
        """
        TESTING
        Generate non-overlapping positions for vertical lines along the dx dimension.

        :param dx: INT-The length of the x-dimension.
        :param min_dist: The minimum distance between lines.
        :param num_lines: The number of lines to generate.
        :param line_width: The width of the lines (the milling tool diameter).

        :return: List[int]: A list of x-coordinates for the lines.
        """
        max_attempts = 500  # Setting a limit to avoid infinite loops
        positions = []
        for _ in range(num_lines):
            for _ in range(max_attempts):
                # Randomly select a position
                new_pos = random.randint(line_width, dx - line_width)
                # Check if it is at a safe distance from all existing positions
                if all(abs(new_pos - pos) >= min_dist + line_width for pos in positions):
                    positions.append(new_pos)
                    break
        return positions

