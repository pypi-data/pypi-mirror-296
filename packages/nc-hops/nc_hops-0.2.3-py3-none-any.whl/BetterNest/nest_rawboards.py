from typing import Union


def create_nest_raw_board(
        makrotyp: Union[int, str] = 0,
        instver: Union[int, str] = '',
        exe_version: Union[int, str] = '7.8.0.2[Hops.exe]',
        bild: str = '',
        info: str = '',
        wzgv: str = '7507D_196',
        wzgv_config: str = '',
        machine: str = 'NestPP',
        ncname: str = '',
        kommentar: str = '',
        dx: Union[int, str, float] = '',
        dy: Union[int, str, float] = '',
        dz: Union[int, str, float] = '',
        dialogdll: str = 'Dialoge.Dll',
        dialogproc: str = 'StandardFormAnzeigen',
        dialogkind: Union[int, str] = 0,
        autoscript_start: Union[int, str] = 1,
        button_bild: Union[int, str] = '',
        dimension_unit: Union[int, str] = 0,
        hh_type: Union[int, str] = '',
        hh_info: str = '',
        hh_art_no: Union[int, str] = '',
        hh_label_pos_x: Union[int, str, float] = -1,
        hh_label_pos_y: Union[int, str, float] = -1,
        hh_free_text1: str = '',
        hh_free_text2: str = '',
        hh_free_text3: str = '',
        hh_free_text4: str = '',
        hh_free_text5: str = '',
        hh_free_text6: str = '',
        hh_free_text7: str = '',
        hh_free_text8: str = '',
        hh_free_text9: str = '',
        hh_free_text10: str = '',
        hh_order_id: Union[int, str] = '',
        hh_order_text1: str = '',
        hh_order_text2: str = '',
        hh_material: str = '',
        hh_storage_id: Union[int, str] = '',
        hh_nest_quantity: Union[int, str] = 1,
        hh_nest_edge_spacing: Union[int, str, float] = 25,
        hh_nest_grain_direction: Union[int, str] = 0,
        hh_nest_orientation: Union[int, str] = 0,
        hh_nest_turn_axis: Union[int, str] = 0,
        hh_nest_rest_id: Union[int, str] = '',
        hh_nest_compact_kind: Union[int, str] = 0,
        hh_work_mode: Union[int, str] = '',
        hh_version: Union[int, str] = 1,
        output_path: str = ''
):
    """
    Nest Raw Board(Rohteil) file generation
    Files to store quantity of material, the preffered way to optimize a certain board etc.
    Raw boards can be rest parts or standard board material
    there's a Rest ID for the rests and storage ID for standard materials
    wzgv is set to 7507D_196 by default, change it to your machine name to avoid problems in BetterNest
    When calling the function, initialize only the things you need.
    and then finally to save the file: output_path='your_raw_board.hop'
    """
    new_raw_board = f""";MAKROTYP={makrotyp}
;INSTVERSION={instver}
;EXEVERSION={exe_version}
;BILD={bild}
;INFO={info}
;WZGV={wzgv}
;WZGVCONFIG={wzgv_config}
;MASCHINE={machine}
;NCNAME={ncname}
;KOMMENTAR={kommentar}
;DX={dx}
;DY={dy}
;DZ={dz}
;DIALOGDLL={dialogdll}
;DIALOGPROC={dialogproc}
;DIALOGKIND={dialogkind}
;AUTOSCRIPTSTART={autoscript_start}
;BUTTONBILD={button_bild}
;DIMENSION_UNIT={dimension_unit}
VARS
   DX := {dx};*VAR*
   DY := {dy};*VAR*
   DZ := {dz};
   _hhdata_Type := '{hh_type}';Part Type / Werkstücktypbezeichnung
   _hhdata_Info := '{hh_info}';Part information / Werkstückinformation
   _hhdata_ArtNo := '{hh_art_no}';Articel number / Artikelnummer
   _hhdata_LabelPosX := {hh_label_pos_x};Label position X / Etikettenposition X
   _hhdata_LabelPosY := {hh_label_pos_y};Label position Y / Etikettenposition Y
   _hhdata_FreeText1 := '{hh_free_text1}';Free text 1 / Freier Text 1
   _hhdata_FreeText2 := '{hh_free_text2}';Free text 2 / Freier Text 2
   _hhdata_FreeText3 := '{hh_free_text3}';Free text 3 / Freier Text 3
   _hhdata_FreeText4 := '{hh_free_text4}';Free text 4 / Freier Text 4
   _hhdata_FreeText5 := '{hh_free_text5}';Free text 5 / Freier Text 5
   _hhdata_FreeText6 := '{hh_free_text6}';Free text 6 / Freier Text 6
   _hhdata_FreeText7 := '{hh_free_text7}';Free text 7 / Freier Text 7
   _hhdata_FreeText8 := '{hh_free_text8}';Free text 8 / Freier Text 8
   _hhdata_FreeText9 := '{hh_free_text9}';Free text 9 / Freier Text 9
   _hhdata_FreeText10 := '{hh_free_text10}';Free text 10 / Freier Text 10
   _hhdata_OrderID := '{hh_order_id}';Order ID / Auftrags-ID
   _hhdata_OrderText1 := '{hh_order_text1}';Free order text 1 / Freier Auftragstext 1
   _hhdata_OrderText2 := '{hh_order_text2}';Free order text 2 / Freier Auftragstext 2
   _hhdata_Material := '{hh_material}';Part material / Materialbezeichnung
   _hhdata_StorageID := '{hh_storage_id}';Storage ID / Lagerbezeichnung
   _hhdata_NestQuantity := {hh_nest_quantity};Quantity / Anzahl
   _hhdata_NestEdgeSpacing := {hh_nest_edge_spacing};Edge spacing / Randabstand
   _hhdata_NestGrainDirection := {hh_nest_grain_direction};Grain direction / Faserrichtung
   _hhdata_NestOrientation := {hh_nest_orientation};Orientation / Orientierung
   _hhdata_NestTurnAxis := {hh_nest_turn_axis};TurnAxis / WendenUmAchse
   _hhdata_NestRestID := '{hh_nest_rest_id}';Rest ID / Rest ID
   _hhdata_NestCompactKind := {hh_nest_compact_kind};Komprimiermode / Komprimiermode
   _hhdata_WorkMode := '{hh_work_mode}';module work mode / Modulmodus
   _hhdata_Version := '{hh_version}';Version / Version
START
Fertigteil (DX,DY,DZ,0,0,0,0,0,'{kommentar}',0,0,0)"""

    with open(output_path, 'w') as wf:
        wf.write(new_raw_board)
