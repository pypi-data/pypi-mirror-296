from ReadHop import ExtractHopProcessing


def get_processing(file: str) -> dict:
    """
    Get all processing into one dictionary using ExtractHopProcessing class and its method processes_as_dict()
    Returns a dictionary with the following keys:
    vertical - for vertical(Bohrung) drills
    horizontal - for horizontal(HorzB) drills
    all_nut - for all saw grooving macros used
    all_saw - for all sawing macros used (very different from grooving macros)
    all_milling - for all the milling processes in the file.
    :param file: file path
    :return: dictionary
    """
    hop_file = ExtractHopProcessing(file)
    all_v_bohrungs = []  # list for all the vertical drill info
    all_h_bohrungs = []  # list for all the horizontal drill info
    all_n_saw = []  # list for all the grooving info
    all_s_saw = []  # list for all the sawing info
    all_mill_lists = []  # list for all milling info

    for key, values in hop_file.processes_as_dict().items():
        if key == 'WZB':  # WZB indicates drilling tool call

            for bohrung in values['processing']:
                if bohrung.lower().startswith('bohrung'):  # to lower since hops is not key sensitive
                    b_split = bohrung.lower().split('bohrung')
                    coordinates = b_split[1].strip().replace('mm', '').replace(')', '').replace('(', '').split(',')
                    # Convert all values to float or int
                    vertical_converted_values\
                        = [float(value) if '.' in value else int(value) for value in coordinates]
                    all_v_bohrungs.append(vertical_converted_values)  # append to its list

                if bohrung.lower().startswith('horzb'):
                    h_split = bohrung.lower().split('horzb')  # to lower since hops is not key sensitive
                    h_coordinates = h_split[1].strip().replace('(', '').replace(')', '').split(',')
                    # Convert all values to float or int
                    horizontal_converted_values\
                        = [float(value) if '.' in value else int(value) for value in h_coordinates]
                    all_h_bohrungs.append(horizontal_converted_values)  # append to its list

        if key == 'WZS':
            for saw in values['processing']:
                if saw.lower().startswith('call _nuten'):
                    s_split = saw.lower().split('call _nuten_x_v5')
                    all_n_saw.append(s_split)
                if saw.lower().startswith('call _saege'):
                    saw_split = saw.lower().split('call _saege_x_v7')
                    all_s_saw.append(saw_split)

        if key == 'WZF':
            mill_list = {}  # Current sublist
            processing = False  # Flag to indicate if we are within an SP-EP block

            for milling in values['processing']:
                if milling.startswith('SP'):
                    processing = True  # Ran into SP, the flag is now True

                    if values['tool_no'] not in mill_list:  # if there's no tool number in the dictionary
                        mill_list['tool_no'] = values['tool_no']  # Add tool number to the dictionary
                    mill_list['sp'] = milling

                elif milling.startswith('EP'):
                    if processing:
                        mill_list['ep'] = milling
                        all_mill_lists.append(mill_list)  # Add the completed sublist to the main list
                        processing = False  # Reached the end of a milling path, flag is now False again
                elif processing:
                    if 'processing' not in mill_list:
                        mill_list['processing'] = []
                    split = milling.strip().replace(')', '').split('(')
                    process\
                        = {split[0]: [float(value) if '.' in value else int(value) for value in split[1].split(',')]}
                    mill_list['processing'].append(process)  # Add items to the current sublist

    return {
        'vertical': all_v_bohrungs,
        'horizontal': all_h_bohrungs,
        'all_nut': all_n_saw,
        'all_saw': all_s_saw,
        'all_milling': all_mill_lists
    }

