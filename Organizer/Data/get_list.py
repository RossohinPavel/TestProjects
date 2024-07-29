import os
import re


def simple_list(pap_to_list) -> tuple:
    list_t_a_h = []
    for root, dirs, files in os.walk(pap_to_list):
        for file in files:
            abs_path = os.path.join(root, file)
            list_t_a_h.append(os.path.relpath(abs_path, pap_to_list))
    return tuple(list_t_a_h)


def new_ex_list(dir_to_list) -> tuple:
    file_list = []
    patterns = (r'\d+__\d+\.jpg', r'cover_\d+\.jpg', r'\d+__\d+-\d+_pcs\.jpg', r'cover_\d+-\d+_pcs\.jpg')
    for ex in os.listdir(dir_to_list):
        if re.fullmatch(r'\d\d\d', ex) or re.fullmatch(r'\d\d\d-\d+_pcs', ex):
            pic_list = []
            for file in os.listdir(f"{dir_to_list}/{ex}"):
                for p in patterns:
                    if re.fullmatch(p, file):
                        pic_list.append(file)
                        break
            if pic_list:
                pic_list.insert(0, ex)
                file_list.append(tuple(pic_list))
    return tuple(file_list)
