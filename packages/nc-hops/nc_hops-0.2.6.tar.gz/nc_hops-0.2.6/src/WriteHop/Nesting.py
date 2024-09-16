from typing import Union


class Nesting:
    def __init__(self, parent):
        self.parent = parent

    def init_nest_part(
            self,
            art_no: Union[str, int] = "''",
            info: Union[str] = "''",
            hh_type: Union[str, int] = "''",
            material: str = "''",
            label_pos_x: Union[int, str] = -1,
            label_pos_y: Union[int, str] = -1,
            order_id: Union[int, str] = "''",
            order_text1: str = "''",
            order_text2: str = "''",
            free_text1: str = "''",
            free_text2: str = "''",
            free_text3: str = "''",
            free_text4: str = "''",
            free_text5: str = "''",
            free_text6: str = "''",
            free_text7: str = "''",
            free_text8: str = "''",
            free_text9: str = "''",
            free_text10: str = "''",
            edge_pic_front_left: str = "''",
            edge_pic_front_right: str = "''",
            edge_pic_back_left: str = "''",
            edge_pic_back_right: str = "''",
            inlay_inside: str = "''",
            inlay_outside: str = "''",
            edge_dim_right: str = "''",
            edge_type_right: Union[str, int] = "''",
            edge_prg_right: str = "''",
            edge_mat_right: str = "''",
            edge_saum_right: Union[str, int, float] = "''",
            edge_add_right: Union[str, int, float] = "''",
            edge_dim_left: str = "''",
            edge_type_left: Union[str, int] = "''",
            edge_prg_left: str = "''",
            edge_mat_left: str = "''",
            edge_saum_left: Union[str, int, float] = "''",
            edge_add_left: Union[str, int, float] = "''",
            edge_dim_back: str = "''",
            edge_type_back: Union[str, int] = "''",
            edge_prg_back: str = "''",
            edge_mat_back: str = "''",
            edge_saum_back: Union[str, int, float] = "''",
            edge_add_back: Union[str, int, float] = "''",
            edge_dim_front: str = "''",
            edge_type_front: Union[str, int] = "''",
            edge_prg_front: str = "''",
            edge_mat_front: str = "''",
            edge_saum_front: Union[str, int, float] = "''",
            edge_add_front: Union[str, int, float] = "''",
            work_mode: Union[str, int] = "''",
            version: Union[str, int] = 1,
            nest_min_quantity: Union[str, int] = 1,
            nest_max_quantity: Union[str, int] = 5,
            nest_priority: Union[str, int] = 0,
            nest_step_angle: Union[str, int] = 90,
            nest_grain_direction: Union[str, int] = 0,
            nest_mirror: Union[str, int] = 0,
            nest_top_bottom_side: Union[str, int] = 0,
            label_id: Union[str, int] = "''",
            comission: Union[str, int] = "''",
            corpus: Union[str, int] = "''",
            bit_pattern: Union[str, int] = "''",
            assigned_machine: str = "''",
            hhdata_object: Union[str, int] = "''",
            object_length: Union[str, int] = "''",
            object_width: Union[str, int] = "''",
            object_depth: Union[str, int] = "''",
            hop_image1: str = "''",
            hop_image2: str = "''",
            hop_image3: str = "''",
            hhdata_id: Union[str, int] = "''",
            inlay: Union[str, int] = "''",
            optimization_status: Union[str, int] = "''",
            count: Union[str, int] = "''") -> None:
        """
        Hops BetterNest Part init string
        :param art_no: Part article number
        :param info: Part info
        :param hh_type: Part type
        :param material: Part Material
        :param label_pos_x: Label position in X
        :param label_pos_y: Label position in Y
        :param order_id: Part Order ID
        :param order_text1: Part order text 1
        :param order_text2: Part order text 2
        :param free_text1: Part free text 1
        :param free_text2: Part free text 2
        :param free_text3: Part free text 3
        :param free_text4: Part free text 4
        :param free_text5: Part free text 5
        :param free_text6: Part free text 6
        :param free_text7: Part free text 7
        :param free_text8: Part free text 8
        :param free_text9: Part free text 9
        :param free_text10: Part free text 10
        :param edge_pic_front_left: Picture of the edge on the front left
        :param edge_pic_front_right: Picture of the edge on the front right
        :param edge_pic_back_left: Picture of the edge on the back left
        :param edge_pic_back_right: Picture of the edge on the back right
        :param inlay_inside: Inlay inside the part
        :param inlay_outside: Inlay outside the part
        :param edge_dim_right: Edge thickness right
        :param edge_type_right: Edge type right
        :param edge_prg_right: Edge program right
        :param edge_mat_right: Edge material right
        :param edge_saum_right: Edge premill right
        :param edge_add_right: Edge additional right
        :param edge_dim_left: Edge thickness
        :param edge_type_left: Edge type left
        :param edge_prg_left: Edge program left
        :param edge_mat_left: Edge material left
        :param edge_saum_left: Edge premill left
        :param edge_add_left: Edge additional left
        :param edge_dim_back: Edge thickness back
        :param edge_type_back: Edge type back
        :param edge_prg_back: Edge program back
        :param edge_mat_back: Edge material back
        :param edge_saum_back: Edge premill back
        :param edge_add_back: Edge additional back
        :param edge_dim_front: Edge thickness front
        :param edge_type_front: Edge type front
        :param edge_prg_front: Edge program front
        :param edge_mat_front: Edge material front
        :param edge_saum_front: Edge premill front
        :param edge_add_front: Edge additional front
        :param work_mode: module work mode- 0, 1
        :param version: Version
        :param nest_min_quantity: Nest minimum quantity
        :param nest_max_quantity: Nest maximum quantity
        :param nest_priority: Nest priority while optimizing
        :param nest_step_angle: Nest step angle
        :param nest_grain_direction: Nest grain direction, 0=ignore, 1=X, 2=Y
        :param nest_mirror: Nest mirroring
        :param nest_top_bottom_side: Nest top or bottom side
        :param label_id: Label id
        :param comission: Commision
        :param corpus: Corpus
        :param bit_pattern: Bit pattern
        :param assigned_machine: Assigned machine
        :param hhdata_object: Object
        :param object_length: Object length
        :param object_width: Object width
        :param object_depth: Object depth
        :param hop_image1: Image 1
        :param hop_image2: Image 2
        :param hop_image3: Image 3
        :param hhdata_id: ID
        :param inlay: Inlay
        :param optimization_status: Part optimization status
        :param count: Part count
        :return: None
        """
        #  Append the needed vars for a nest part
        #  Appending to the vars from the WriteHop init method
        self.parent.vars.update(
            {
                '_hhdata_ArtNo': art_no,
                '_hhdata_Info': info,
                '_hhdata_Type': hh_type,
                '_hhdata_Material': material,
                '_hhdata_LabelPosX': label_pos_x,
                '_hhdata_LabelPosY': label_pos_y,
                '_hhdata_OrderID': order_id,
                '_hhdata_OrderText1': order_text1,
                '_hhdata_OrderText2': order_text2,
                '_hhdata_FreeText1': free_text1,
                '_hhdata_FreeText2': free_text2,
                '_hhdata_FreeText3': free_text3,
                '_hhdata_FreeText4': free_text4,
                '_hhdata_FreeText5': free_text5,
                '_hhdata_FreeText6': free_text6,
                '_hhdata_FreeText7': free_text7,
                '_hhdata_FreeText8': free_text8,
                '_hhdata_FreeText9': free_text9,
                '_hhdata_FreeText10': free_text10,
                '_hhdata_EdgePicFrontLeft': edge_pic_front_left,
                '_hhdata_EdgePicFrontRight': edge_pic_front_right,
                '_hhdata_EdgePicBackLeft': edge_pic_back_left,
                '_hhdata_EdgePicBackRight': edge_pic_back_right,
                '_hhdata_InlayInside': inlay_inside,
                '_hhdata_InlayOutside': inlay_outside,
                '_hhdata_EdgeDimRight': edge_dim_right,
                '_hhdata_EdgeTypRight': edge_type_right,
                '_hhdata_EdgePrgRight': edge_prg_right,
                '_hhdata_EdgeMatRight': edge_mat_right,
                '_hhdata_EdgeSaumRight': edge_saum_right,
                '_hhdata_EdgeAddRight': edge_add_right,
                '_hhdata_EdgeDimLeft': edge_dim_left,
                '_hhdata_EdgeTypLeft': edge_type_left,
                '_hhdata_EdgePrgLeft': edge_prg_left,
                '_hhdata_EdgeMatLeft': edge_mat_left,
                '_hhdata_EdgeSaumLeft': edge_saum_left,
                '_hhdata_EdgeAddLeft': edge_add_left,
                '_hhdata_EdgeDimBack': edge_dim_back,
                '_hhdata_EdgeTypBack': edge_type_back,
                '_hhdata_EdgePrgBack': edge_prg_back,
                '_hhdata_EdgeMatBack': edge_mat_back,
                '_hhdata_EdgeSaumBack': edge_saum_back,
                '_hhdata_EdgeAddBack': edge_add_back,
                '_hhdata_EdgeDimFront': edge_dim_front,
                '_hhdata_EdgeTypFront': edge_type_front,
                '_hhdata_EdgePrgFront': edge_prg_front,
                '_hhdata_EdgeMatFront': edge_mat_front,
                '_hhdata_EdgeSaumFront': edge_saum_front,
                '_hhdata_EdgeAddFront': edge_add_front,
                '_hhdata_WorkMode': work_mode,
                '_hhdata_Version': version,
                '_hhdata_NestQuantityMin': nest_min_quantity,
                '_hhdata_NestQuantityMax': nest_max_quantity,
                '_hhdata_NestPriority': nest_priority,
                '_hhdata_NestStepAngle': nest_step_angle,
                '_hhdata_NestGrainDirection': nest_grain_direction,
                '_hhdata_NestMirror': nest_mirror,
                '_hhdata_NestTopBottomSide': nest_top_bottom_side,
                '_hhdata_LabelID': label_id,
                '_hhdata_Commission': comission,
                '_hhdata_Corpus': corpus,
                '_hhdata_BitPattern': bit_pattern,
                '_hhdata_AssignedMachine': assigned_machine,
                '_hhdata_Object': hhdata_object,
                '_hhdata_ObjectLength': object_length,
                '_hhdata_ObjectWidth': object_width,
                '_hhdata_ObjectDepth': object_depth,
                '_hhdata_HopImage1': hop_image1,
                '_hhdata_HopImage2': hop_image2,
                '_hhdata_HopImage3': hop_image3,
                '_hhdata_Id': hhdata_id,
                '_hhdata_Inlay': inlay,
                '_hhdata_OptimizationStatus': optimization_status,
                '_hhdata_Count': count
            }
        )

        self.hh_mark_label()  # call HH_MarkLabel()
        self.trennen_inen_aussen()  # call TrennenInnenAussen()

    def hh_mark_label(self) -> None:
        """
        String for the HH_MarkLabel
        Needed for nest parts
        """
        mark_label_string =\
            'CALL HH_MarkLabel ( VAL POSX:=_hhdata_LabelPosX,POSY:=_hhdata_LabelPosY,ANGLE:=0,LASER:=0)'
        self.parent.commands.append(mark_label_string)

    def trennen_inen_aussen(self) -> None:
        """
        String was in the sample file. Will be updated on what this string means.
        """
        brennen_inen_string =\
            'CALL BN_TrennerInnenAussen ()'
        self.parent.commands.append(brennen_inen_string)

    def nest_contour(self) -> None:
        """
        Nest contour string for nest parts
        """
        nest_contour_string = \
            'CALL BN_NestKontur ()'
        self.parent.commands.append(nest_contour_string)

    def klein_format(self,
                     first_depth: Union[str, int, float] = 1.5,
                     milling_steps: Union[str, int, float] = 2,
                     final_depth: Union[str, int, float] = 0.45,
                     overlap: Union[str, int, float] = 0) -> None:
        """
        Hops macro Klein_Format
        Macro looks at the DX and DY of the part and decides if the part should be formatted as a small
        part or as a normal-sized part
        Small parts are being formatted at least twice when they are smaller than 200mm or if their area is
        smaller than 300mm2

        :param first_depth: The first depth when there are multiple formatting steps
        :param milling_steps: The number of milling steps when formatting the part
        :param final_depth: The final depth of the cut
        :param overlap: Overlap
        :return: None
        """

        klein_format = f"CALL HH_KLEIN_FORMAT ( VAL SCHRUPP_TIEFE:={first_depth}," \
                       f"SCHRUPP_STEPS:={milling_steps}," \
                       f"SCHLICHT_TIEFE:=-{final_depth}," \
                       f"UEBERLAPPUNG:={overlap})"
        self.parent.commands.append(klein_format)
        self.nest_contour()  # call NestKontur()

