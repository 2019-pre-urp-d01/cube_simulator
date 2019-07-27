import logging

def LoadCfg(file_loc = "setting.config"):
    setup_file = open(file_loc, 'r')

    parsing_mode = 0
    cell_function_dict  = {0:"x", 1:"x", 2:"x", 3:"x", 4:"x", 5:"x"}
    cell_bit_up_dict    = {"u0":[1,0], "u1":[2,0], "u2":[4,0], "u3":[8,0], "u4":[16,0], "u5":[32,0], "u6":[64,0], "u7":[128,0]}
    cell_bit_front_dict = {"f0":[1,0], "f1":[2,0], "f2":[4,0], "f3":[8,0], "f4":[16,0], "f5":[32,0], "f6":[64,0], "f7":[128,0]}
    cell_bit_right_dict = {"r0":[1,0], "r1":[2,0], "r2":[4,0], "r3":[8,0], "r4":[16,0], "r5":[32,0], "r6":[64,0], "r7":[128,0]}
    cell_bit_left_dict  = {"l0":[1,0], "l1":[2,0], "l2":[4,0], "l3":[8,0], "l4":[16,0], "l5":[32,0], "l6":[64,0], "l7":[128,0]}
    cell_bit_back_dict  = {"b0":[1,0], "b1":[2,0], "b2":[4,0], "b3":[8,0], "b4":[16,0], "b5":[32,0], "b6":[64,0], "b7":[128,0]}
    cell_bit_down_dict  = {"d0":[1,0], "d1":[2,0], "d2":[4,0], "d3":[8,0], "d4":[16,0], "d5":[32,0], "d6":[64,0], "d7":[128,0]}

    while True:
        line = setup_file.readline()
        if not line: break
        line = line.replace("\n", "")
        line = line.replace(" ", "")
        if line == "": continue
        if line[0] == "#": parsing_mode += 1; continue
        if line[0] == "*": continue

        if parsing_mode == 1:
            if   line.split('=')[0] == "0":
                cell_function_dict[0] = line.split('=')[1]
            elif line.split('=')[0] == "1":
                cell_function_dict[1] = line.split('=')[1]
            elif line.split('=')[0] == "2":
                cell_function_dict[2] = line.split('=')[1]
            elif line.split('=')[0] == "3":
                cell_function_dict[3] = line.split('=')[1]
            elif line.split('=')[0] == "4":
                cell_function_dict[4] = line.split('=')[1]
            elif line.split('=')[0] == "5":
                cell_function_dict[5] = line.split('=')[1]
            else:
                logging.error("Plane Number can only be 0, 1, 2, 3, 4, or 5.")
                return None

        if parsing_mode == 2:
            if   line.split('=')[0] == "0":
                cell_bit_up_dict["u0"][0] = line.split('=')[1].split(',')[0]
                cell_bit_up_dict["u1"][0] = line.split('=')[1].split(',')[1]
                cell_bit_up_dict["u2"][0] = line.split('=')[1].split(',')[2]
                cell_bit_up_dict["u3"][0] = line.split('=')[1].split(',')[3]
                cell_bit_up_dict["u4"][0] = line.split('=')[1].split(',')[4]
                cell_bit_up_dict["u5"][0] = line.split('=')[1].split(',')[5]
                cell_bit_up_dict["u6"][0] = line.split('=')[1].split(',')[6]
                cell_bit_up_dict["u7"][0] = line.split('=')[1].split(',')[7]
            elif line.split('=')[0] == "1":
                cell_bit_front_dict["f0"][0] = line.split('=')[1].split(',')[0]
                cell_bit_front_dict["f1"][0] = line.split('=')[1].split(',')[1]
                cell_bit_front_dict["f2"][0] = line.split('=')[1].split(',')[2]
                cell_bit_front_dict["f3"][0] = line.split('=')[1].split(',')[3]
                cell_bit_front_dict["f4"][0] = line.split('=')[1].split(',')[4]
                cell_bit_front_dict["f5"][0] = line.split('=')[1].split(',')[5]
                cell_bit_front_dict["f6"][0] = line.split('=')[1].split(',')[6]
                cell_bit_front_dict["f7"][0] = line.split('=')[1].split(',')[7]
            elif line.split('=')[0] == "2":
                cell_bit_right_dict["r0"][0] = line.split('=')[1].split(',')[0]
                cell_bit_right_dict["r1"][0] = line.split('=')[1].split(',')[1]
                cell_bit_right_dict["r2"][0] = line.split('=')[1].split(',')[2]
                cell_bit_right_dict["r3"][0] = line.split('=')[1].split(',')[3]
                cell_bit_right_dict["r4"][0] = line.split('=')[1].split(',')[4]
                cell_bit_right_dict["r5"][0] = line.split('=')[1].split(',')[5]
                cell_bit_right_dict["r6"][0] = line.split('=')[1].split(',')[6]
                cell_bit_right_dict["r7"][0] = line.split('=')[1].split(',')[7]
            elif line.split('=')[0] == "3":
                cell_bit_left_dict["l0"][0] = line.split('=')[1].split(',')[0]
                cell_bit_left_dict["l1"][0] = line.split('=')[1].split(',')[1]
                cell_bit_left_dict["l2"][0] = line.split('=')[1].split(',')[2]
                cell_bit_left_dict["l3"][0] = line.split('=')[1].split(',')[3]
                cell_bit_left_dict["l4"][0] = line.split('=')[1].split(',')[4]
                cell_bit_left_dict["l5"][0] = line.split('=')[1].split(',')[5]
                cell_bit_left_dict["l6"][0] = line.split('=')[1].split(',')[6]
                cell_bit_left_dict["l7"][0] = line.split('=')[1].split(',')[7]
            elif line.split('=')[0] == "4":
                cell_bit_back_dict["b0"][0] = line.split('=')[1].split(',')[0]
                cell_bit_back_dict["b1"][0] = line.split('=')[1].split(',')[1]
                cell_bit_back_dict["b2"][0] = line.split('=')[1].split(',')[2]
                cell_bit_back_dict["b3"][0] = line.split('=')[1].split(',')[3]
                cell_bit_back_dict["b4"][0] = line.split('=')[1].split(',')[4]
                cell_bit_back_dict["b5"][0] = line.split('=')[1].split(',')[5]
                cell_bit_back_dict["b6"][0] = line.split('=')[1].split(',')[6]
                cell_bit_back_dict["b7"][0] = line.split('=')[1].split(',')[7]
            elif line.split('=')[0] == "5":
                cell_bit_down_dict["d0"][0] = line.split('=')[1].split(',')[0]
                cell_bit_down_dict["d1"][0] = line.split('=')[1].split(',')[1]
                cell_bit_down_dict["d2"][0] = line.split('=')[1].split(',')[2]
                cell_bit_down_dict["d3"][0] = line.split('=')[1].split(',')[3]
                cell_bit_down_dict["d4"][0] = line.split('=')[1].split(',')[4]
                cell_bit_down_dict["d5"][0] = line.split('=')[1].split(',')[5]
                cell_bit_down_dict["d6"][0] = line.split('=')[1].split(',')[6]
                cell_bit_down_dict["d7"][0] = line.split('=')[1].split(',')[7]
            else:
                logging.error("Plane Number can only be 0, 1, 2, 3, 4, or 5.")
                return None

    setup_file.close()

    return cell_function_dict, cell_bit_up_dict, cell_bit_front_dict, cell_bit_right_dict, cell_bit_left_dict, cell_bit_back_dict, cell_bit_down_dict
