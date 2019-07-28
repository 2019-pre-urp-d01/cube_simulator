import logging

def LoadCfg(file_loc = "setting.config"):
    setup_file = open(file_loc, 'r')

    parsing_mode = 0
    cell_function = ["Input", "One", "Not", "Or", "And", "Output"]              # Plane 역할
    cell_bit_place_value = [[1, 2, 4, 8, 16, 32, 64, 128]] *6                   # Bit Cell 기본 자릿값

    while True:                                                                 # break 전까지 계속 반복
        line = setup_file.readline()                                            # 파일을 한 줄씩 읽기
        if not line: break                                                      # 마지막 줄이 아닐 때 끝냄
        line = line.replace("\n", "")                                           # 개행기 삭제
        line = line.replace(" ", "")                                            # 공백 삭제
        if line == "": continue                                                 # 비어 있는 줄 스킵
        if line[0] == "*": continue                                             # *로 시작하는 줄은 주석으로 처리
        if line[0] == "#": parsing_mode += 1; continue                          # #로 시작하는 줄은 섹션 구분

        if parsing_mode == 1:                                                   # Plane Actions 섹션
            if   line.split('=')[0] == "0":                                     # 0번 Plane의 동작을
                cell_function[0] = line.split('=')[1]                           # cell_function[0]에 저장
            elif line.split('=')[0] == "1":                                     # 1번 Plane의 동작을
                cell_function[1] = line.split('=')[1]                           # cell_function[0]에 저장
            elif line.split('=')[0] == "2":                                     # 2번 Plane의 동작을
                cell_function[2] = line.split('=')[1]                           # cell_function[0]에 저장
            elif line.split('=')[0] == "3":                                     # 3번 Plane의 동작을
                cell_function[3] = line.split('=')[1]                           # cell_function[0]에 저장
            elif line.split('=')[0] == "4":                                     # 4번 Plane의 동작을
                cell_function[4] = line.split('=')[1]                           # cell_function[0]에 저장
            elif line.split('=')[0] == "5":                                     # 5번 Plane의 동작을
                cell_function[5] = line.split('=')[1]                           # cell_function[0]에 저장
            else:                                                               # 다른 Plane 번호가 0일 때
                logging.error("Plane Number can only be 0, 1, 2, 3, 4, or 5.")  # 오류 처리 (Logging)
                return None                                                     # 반환값 없음

        if parsing_mode == 2:                                                   # Place Value 섹션
            if   line.split('=')[0] == "0":                                     # 0번 Plane
                for i in range(8): cell_bit_place_value[0][i] = int(line.split('=')[1].split(',')[i])
            elif line.split('=')[0] == "1":                                     # 1번 Plane
                for i in range(8): cell_bit_place_value[1][i] = int(line.split('=')[1].split(',')[i])
            elif line.split('=')[0] == "2":                                     # 2번 Plane
                for i in range(8): cell_bit_place_value[2][i] = int(line.split('=')[1].split(',')[i])
            elif line.split('=')[0] == "3":                                     # 3번 Plane
                for i in range(8): cell_bit_place_value[3][i] = int(line.split('=')[1].split(',')[i])
            elif line.split('=')[0] == "4":                                     # 4번 Plane
                for i in range(8): cell_bit_place_value[4][i] = int(line.split('=')[1].split(',')[i])
            elif line.split('=')[0] == "5":                                     # 5번 Plane
                for i in range(8): cell_bit_place_value[5][i] = int(line.split('=')[1].split(',')[i])
            else:                                                               # 그 외의 경우
                logging.error("Plane Number can only be 0, 1, 2, 3, 4, or 5.")  # 오류 처리 (Logging)
                return None                                                     # 반환값 없음

    setup_file.close()

    return cell_function, cell_bit_place_value
