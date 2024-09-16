from typing import Union
from .Milling import Milling
from .Drilling import Drilling
from .Machine import Machine
from .Nesting import Nesting
from .Contours import Contours
from .CustomCommands import Custom


class WriteHop:
    def __init__(self,
                 dx: Union[int, str, float] = 600,
                 dy: Union[int, str, float] = 400,
                 dz: Union[int, str, float] = 19,
                 rot: Union[int, str] = 0):
        """
        Parameters
        :param dx: Panel DX
        :param dy: Panel DY
        :param dz: Panel DZ
        :param rot: Panel rotation - 0=0 degrees, 1=90 degrees, 2=180 degrees, 3=270 degrees
        """
        self.commands = []  # Main commands list
        self.vars = {}  # Dictionary for hop VARS section
        self.dx = dx  # Panel length
        self.dy = dy  # Panel width
        self.dz = dz  # Panel thickness
        self.rot = rot  # Panel rotation
        self.machine = Machine(self)  # Machine module - contains methods with machine macros
        self.milling = Milling(self)  # Milling module - contains methods with milling macros
        self.drilling = Drilling(self)  # Drilling module - contains methods with drilling macros
        self.nesting = Nesting(self)  # Nesting module - contains methods with nesting macros
        self.contours = Contours(self)  # Contours module - for drawing contour lines
        self.custom = Custom(self)  # Custom commands

    def init_hop(self, wzgv: str = 'HOLZHER', comment: str = '') -> str:
        init_string = f''';MAKROTYP=0
;INSTVERSION=
;EXEVERSION=7.8.0.2[Hops.exe]
;BILD=
;INFO=
;WZGV={wzgv}
;WZGVCONFIG=
;MASCHINE=HOLZHER
;NCNAME=
;KOMMENTAR={comment}
;DX={self.dx}
;DY={self.dy}
;DZ={self.dz}
;DIALOGDLL=Dialoge.Dll
;DIALOGPROC=StandardFormAnzeigen
;DIALOGKIND=0
;AUTOSCRIPTSTART=1
;BUTTONBILD=
;DIMENSION_UNIT=0
VARS
   DX := {self.dx};*VAR*
   DY := {self.dy};*VAR*
   DZ := {self.dz};*VAR*
'''
        for key, value in self.vars.items():
            init_string += f'   {key} := {value};*VAR*\n'
        return init_string

    def write_to_file(self,
                      file_name: str,
                      wzgv: str = 'HOLZHER',
                      comment: str = ''):
        """
        Write hop
        :param file_name: File name
        :param wzgv: Machine name
        :param comment: Comment
        :return: None
        """
        init_string = self.init_hop(wzgv=wzgv, comment=comment)
        with open(file_name, 'w') as file:
            file.write(init_string
                       + f"START\nFertigteil (DX,DY,DZ,{self.rot},0,0,0,0,'{comment}',0,0,0)\n"
                       + '\n'.join(self.commands))

    def return_file(self,
                    wzgv: str = 'HOLZHER',
                    comment: str = ''):
        """
        Return hop file 
        :param file_name: File name
        :param wzgv: Machine name 
        :param comment: Comment 
        :return: str
        """
        init_string = self.init_hop(wzgv=wzgv, comment=comment)
        hop = init_string + f"START\nFertigteil (DX,DY,DZ,{self.rot},0,0,0,0,'{comment}',0,0,0)\n" + '\n'.join(self.commands) 
        return hop

