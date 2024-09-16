from typing import Union


class Custom:
    def __init__(self, parent):
        self.parent = parent

    def ekran(
            self,
            distance: Union[int, str, float] = 70,
            pocket_tool: Union[int, str] = 50,
            ramp_tool: Union[int, str] = 2,
            depth: Union[int, str, float] = -3.5) -> None:
        """
        Custom front for further testing.
        Custom pocketing, with custom overlap and custom tool movement
        Using contours to draw the pocket rectangle and then calling the freeform pocket macro
        :param distance: - int str or float
        :param pocket_tool: tool for pocketing
        :param ramp_tool: tool for cleaning the remaining radius
        :param depth: pocket and ramp depth
        :return: None
        """
        self.parent.vars['distance'] = distance
        self.parent.milling.comment('Ekran_Fronta_Pocket')

        # Start point of the contour
        self.parent.contours.contour_kb(
            name='Ekran',
            comment='Pocket',
            x='distance',
            y='distance',
            z=0,
            comment2='',
            side=1,
            additional=0
        )
        # First contour line
        self.parent.contours.g01(
            name='1',
            x='distance',
            y='distance',
            z=0,
            comment='Pocket',
            side=3,
            additional=2
        )
        # Second contour line
        self.parent.contours.g01(
            name='2',
            x='distance',
            y='distance',
            z=0,
            comment='Pocket',
            side=5,
            additional=2
        )
        # Third contour line
        self.parent.contours.g01(
            name='3',
            x='distance',
            y='distance',
            z=0,
            comment='Pocket',
            side=7,
            additional=2
        )
        # Fourth contour line
        self.parent.contours.g01(
            name='4',
            x='distance',
            y='distance',
            z=0,
            comment='Pocket',
            side=1,
            additional=2
        )
        # Select pocketing tool
        self.parent.milling.add_tool(pocket_tool)
        # Pocket
        self.parent.milling.execute_pocket_outlines_v5(
            name='Ekran',
            aa=0,
            overlap=67,
            mode=2,
            angle=0,
            depth=depth,
            maxz='_AT_MAXDEPTH',
            rd=0,
            fliegendeintauchen=0,
            maxeintauchlaenge=20,
        )
        self.parent.milling.comment('Ekran_Fronta_Ramp')
        # Select ramp tool
        self.parent.milling.add_tool(ramp_tool)
        # Ramp 1
        self.parent.milling.rectangle_ramp(
            x_center=0,
            y_center=0,
            ramp_length=f'dx-(distance*2)',
            ramp_height=f'dy-(distance*2)',
            ramp_radius=0,
            depth=depth,
            ramp_correction=2,
            esxy=9
        )
        # Ramp 2
        self.parent.milling.rectangle_ramp(
            x_center=0,
            y_center=0,
            ramp_length=f'dx-(distance*2)-3',
            ramp_height=f'dy-(distance*2)-3',
            ramp_radius=0,
            depth=depth,
            ramp_correction=2,
            esxy=9
        )

    def standard_tool_klein_format(self,
                                   first_depth: Union[int, str, float] = 1.5,
                                   milling_steps: Union[int, str] = 2,
                                   final_depth: Union[int, str, float] = 0.20,
                                   overlap: Union[int, str, float] = 0) -> None:
        """
        A custom command that gets the standard router ID from Hops, and cuts the nest part with
        the Klein Format macro made specifically for nesting.
        Standard tool is intended for chipboard now.
        :param first_depth: The first depth if the piece is small.
        :param milling_steps: The number of milling steps if the piece is small
        :param final_depth: the final depth of the cut.
        :param overlap: overlap
        :return: None
        """
        self.parent.milling.comment('Klein_Format')
        self.parent.milling.get_standard_router_id()  # Call standard tool
        self.parent.nesting.klein_format(  # The Klein Format macro
            first_depth=first_depth,
            milling_steps=milling_steps,
            final_depth=final_depth,
            overlap=overlap
        )

    def special_tool_klein_format(self,
                                  first_depth: Union[int, str, float] = 1.5,
                                  milling_steps: Union[int, str] = 2,
                                  final_depth: Union[int, str, float] = 0.456,
                                  overlap: Union[int, str, float] = 0) -> None:
        """
        A custom command that gets the special router ID from Hops, and cuts the nest part with
        the Klein Format macro made specifically for nesting.
        Special tool is the MDF cut tool in my case
        :param first_depth: The first depth if the piece is small.
        :param milling_steps: The number of milling steps if the piece is small
        :param final_depth: the final depth of the cut.
        :param overlap: overlap
        :return: None
        """
        self.parent.milling.comment('Klein_Format')
        self.parent.milling.get_special_router_id()  # Call standard tool
        self.parent.nesting.klein_format(  # The Klein Format macro
            first_depth=first_depth,
            milling_steps=milling_steps,
            final_depth=final_depth,
            overlap=overlap
        )

