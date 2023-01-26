import datetime
import io
import json
import time
import uuid
from random import randint
import os
import traceback
import random
import logging
import csv

min_s = os.getenv("RAND_MIN_MS")
max_s = os.getenv("RAND_MAX_MS")
IC_IMG_DIR = os.getenv("IMAGE_FOLDER")


def build_dict_from_list_of_dicts_by_key(list_obj: list, key_name: str) -> dict:
    """Возвращает новый словарь с ключами по одному из атрибутов итемсов"""
    result = dict()
    for item in list_obj:
        result[item[key_name]] = item
    return result


def log(msg, *args, end=None) -> str:
    if args is not None:
        msg = msg % args
    final_msg = str(datetime.datetime.now()) + '\t' + msg
    if end is not None:
        print(final_msg, end=end)
    else:
        print(final_msg)
    return final_msg


def get_unique_items_by_keys_from_list(src_list, keys: list) -> set:
    """
    Stringed!
    :param src_list:
    :param keys:
    :return:
    """
    result = set()
    for r in src_list:
        new_item = list()
        for k in keys:
            new_item.append(str(r[k]))
        result.add('\t'.join(new_item))
    return result


def init_dir(*dirs) -> str:
    result = os.path.join(*dirs)
    os.makedirs(result, exist_ok=True)
    return result


def log_r(msg, *args) -> str:
    if args is not None:
        msg = msg % args
    final_msg = str(datetime.datetime.now()) + '\t' + msg
    print('\r', final_msg, end="", flush=True)
    return final_msg


def screenshot(driver, shots_path=None, mode="FALSE", msg=""):
    if mode == "TRUE":
        try:
            if msg != "":
                msg += "_"
            driver.save_screenshot(
                shots_path + "/" + msg + str(datetime.datetime.now()).replace(" ", "_").replace(".", "") + ".png")
        except Exception as e:
            print(e)


def sleep():
    rr = randint(int(min_s), int(max_s)) / 1000
    time.sleep(rr)


def append_to_csv(file_path, message):
    with open(file_path, "a") as log_file:
        log_file.write(message + "\r\n")


def init_text_file(filepath) -> str:
    with open(filepath, 'a') as f:
        f.write('')
    return filepath


def append_to_csv_py(file_path, message: list):
    with open(file_path, "a+", newline='') as log_file:
        csv_writer = csv.writer(log_file, delimiter=';')
        csv_writer.writerow(message)


def get_list_from_csv(file, delimiter=';') -> list:
    result = list()
    with open(file, 'r') as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        for r in csv_reader:
            result.append(r)
    return result


def read_csv_py(file, encoding=None, delimiter=";") -> list:
    data = list()
    with open(file, 'r', encoding=encoding) as f:
        csv_reader = csv.reader(f, delimiter=delimiter)
        for r in csv_reader:
            data.append(r)
    return data


def read_txt(file, encoding='utf-8'):
    with open(file, 'r', encoding=encoding) as f:
        data = f.read()
    return data


def add_last_slash(src) -> str:
    if src[-1] != '/':
        src = src + '/'
    return src


def remove_first_slash(src) -> str:
    if src[0] == '/':
        src = src[1::]
    return src


def reverse_str(src) -> str:
    return src[::-1]


def write_list_to_csv(file, data: list, delimiter=';'):
    with open(file, 'w') as f:
        csv_writer = csv.writer(f, delimiter=delimiter)
        for r in range(len(data)):
            csv_writer.writerow([data[r]])


def clear_file(file):
    with open(file, 'w') as f:
        f.write("")


def write_into_file(filepath, content):
    with open(filepath, 'w') as f:
        f.write(content)


def write_json_file(filepath, obj):
    with open(filepath, 'w') as f:
        json.dump(obj, f, ensure_ascii=False, indent=4, sort_keys=True)


def get_dict_from_list_by_key_val(src_list, key, value, default=''):
    """Отдаёт item из списка по значению определённого атрибута этого итема"""
    for item in src_list:
        if item[key] == value:
            return item
    return default


def generate_uuid():
    return str(uuid.uuid4())


def read_tsv(file) -> list:
    content = list()
    with open(file, 'r') as f:
        for line in f:
            if line[0] == "#":
                continue
            row = line.strip()
            cells = row.split("\t")
            content.append(cells)
    return content


def exception_handler(e):
    logging.exception(log(str(e)))
    traceback.print_exc()


def exception_handler_2(log_file):
    with open(log_file, 'a') as f:
        traceback.print_exc()
        traceback.print_exc(file=f)


def read_json_file(filepath):
    with open(filepath, 'r') as fj:
        return json.load(fj)


def get_today_date() -> str:
    """2021-03-31"""
    return str(datetime.date.today())


def get_chunks_of_list(list_obj: list, chunk_amount: int) -> list:
    """Разбить список на части"""
    result = list()
    counter = 0
    cur_chunk = list()
    for item in list_obj:
        cur_chunk.append(item)
        counter += 1
        if counter >= chunk_amount:
            result.append(cur_chunk)
            cur_chunk = list()
            counter = 0
    if len(cur_chunk) != 0:
        result.append(cur_chunk)
    return result


def create_file_name_by_now(ext, additional=''):
    hsh = random.getrandbits(32)
    return datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S-%f") + "_%08x" % hsh + f'__{additional}.{ext}'


def substract_lists(a: list, b: list) -> list:
    return [i for i in a if i not in b]


def get_list_from_requests_files(f):
    """
    Достаёт список из значений первого столбца из файла
    """
    stream = io.StringIO(f.stream.read().decode("UTF8"), newline=None)
    return [row[0] for row in csv.reader(stream)]


def concat_dict_values_by_list_of_keys(dict_obj: dict, column_list: list):
    result = ''
    for column in column_list:
        result += str(dict_obj[column])
    return result


def if_str_is_none_set_empty_str(val: str, default='') -> str:
    if val is None:
        return default
    return val


def init_dicts_branch(root_dict: dict, keys_hierarchy: tuple, value=None, overwrite=False):
    """modifying function"""

    last_key_index = len(keys_hierarchy) - 1
    cur_key_index = 0
    cur_level = root_dict

    def next_level():
        nonlocal cur_level, cur_key_index
        cur_level = cur_level[key]
        cur_key_index += 1

    for key in keys_hierarchy:
        if key not in cur_level:
            if cur_key_index == last_key_index:
                cur_level[key] = value
            else:
                cur_level[key] = dict()
                next_level()
        else:
            if cur_key_index == last_key_index:
                if overwrite:
                    cur_level[key] = value
            else:
                next_level()


def get_value_by_path_safely(root_dict: dict, path_of_keys: tuple, default_keys: tuple, default_value=None):
    """Функция пытается получить значение из многомерного словаря по заданному пути ключей.
    Если на пути попадается несуществующий ключ, то пытается применить ключи из кортеджа default_keys, использует
    первую удачную попытку. Если все попытки доступа безуспешны - возвращает значение по-умолчанию"""
    cur_dict_level = root_dict
    for key in path_of_keys:
        if key in cur_dict_level:
            cur_dict_level = cur_dict_level[key]
        else:
            for def_key in default_keys:
                if def_key in cur_dict_level:
                    cur_dict_level = cur_dict_level[def_key]
                    break
            else:
                return default_value
    return cur_dict_level


def get_str_cortege(item_list: list) -> str:
    return ",".join(["'" + sku + "'" for sku in item_list])


def delete_items_from_dict_by_keys_list(obj: dict, keys_list: list):
    """Удаляет итемы из словаря по списку ключей"""
    for key in keys_list:
        obj.pop(key, None)


def extend_dict(main_dict: dict, additional_dict: dict):
    """Мутирующая функция, изменяет main_dict, добавляя в него итемы из additional_dict"""
    for k, v in additional_dict.items():
        main_dict[k] = v


def wait_in_seconds(seconds: int):
    print(f'Waiting {seconds} seconds...')
    time.sleep(seconds)


if __name__ == '__main__':
   pass
