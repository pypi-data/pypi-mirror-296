from typing import Union


class Contours:
    def __init__(self, parent):
        self.parent = parent

    def contour_kb(self,
                   name: str = '',
                   comment: str = '',
                   x: Union[int, str, float] = 0,
                   y: Union[int, str, float] = 0,
                   z: Union[int, str, float] = 0,
                   comment2: str = '',
                   side: Union[int, str] = 1,
                   additional: Union[int, str] = 0) -> None:
        """
        KB - Contour start point
        :param name: Contour name
        :param comment: Contour comment
        :param x: X Position of the line
        :param y: Y Position of the line
        :param z: Z Position of the line
        :param comment2: Contour comment
        :param side: Side (0 point of the piece/board)
        :param additional: Not sure what this is
        :return: None
        """

        csp_string = f"KB ('{name}','{comment}',{x},{y},{z},'{comment2}',{side},{additional})"
        self.parent.commands.append(csp_string)

    def g01(self,
            name: str = '',
            x: Union[int, str, float] = 0,
            y: Union[int, str, float] = 0,
            z: Union[int, str, float] = 0,
            comment: str = '',
            side: Union[int, str] = 1,
            additional: Union[int, str] = 2) -> None:
        """
        KG01 - Draw a contour line
        :param name: Name of the line/contour
        :param x: X Position of the line
        :param y: Y Position of the line
        :param z: Z Position of the line
        :param comment: Contour comment
        :param side: Side (0 point of the piece/board)
        :param additional: Not sure what this is
        :return: None
        """

        g01_string = f"KG01 ('{name}',{x},{y},{z},'{comment}',{side},{additional})"
        self.parent.commands.append(g01_string)

