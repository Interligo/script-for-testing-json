'''
Необходимо написать скрипт, который сможет найти максимальное количество ошибок структуры и данных в первой папке.
Примечание: часть ошибок может быть связано с JSON схемой, может с самими данными и ключами для них.
В результате работы скрипта, надо показать какие файлы не валидны, какие там ошибки и для каждой ошибки на
человеко-понятном языке указать как данные исправить.
Вывод скрипта положить в файл (логом или html таблицей), который сможет прочитать не разработчик.
'''

import os
import json
import logging


logger = logging.getLogger('root')
log_filename = os.path.join(os.path.dirname(__file__), 'script_result.txt')
logging.basicConfig(filename=log_filename, filemode='w', format='%(message)s')
logger.setLevel(logging.INFO)


def get_folder_path(dir_name: str) -> str:
    work_folder_path = os.path.join(os.getcwd(), dir_name)
    return work_folder_path


def testing_files(schema_folder, json_folder):
    schema_folder_path = get_folder_path(schema_folder)
    json_folder_path = get_folder_path(json_folder)

    list_schema_files = os.listdir(schema_folder_path)
    list_json_files = os.listdir(json_folder_path)

    logger.info('Анализ файлов запущен.\n')

    for schema_file in list_schema_files:
        name_event, file_extension = schema_file.split('.')

        for json_file in list_json_files:
            with open(os.path.join(json_folder_path, json_file), 'r') as opend_json_file:
                data_from_json = json.load(opend_json_file)

            try:
                if name_event == data_from_json['event']:
                    with open(os.path.join(schema_folder_path, schema_file), 'r') as opend_schema_file:
                        data_from_schema = json.load(opend_schema_file)

                    amount_of_requirements = len(data_from_schema['required'])
                    current_compliance = 0

                    for data in data_from_schema['required']:
                        if data in data_from_json['data']:
                            for value in data_from_json['data']:
                                if data_from_json['data'][value] is None:
                                    logger.info(f'Ошибка! В файле "{json_file}" обнаружено пустое поле "{value}".')
                                    logger.info(f'Для устранения ошибки необходимо заполнить поле "{value}".\n')
                                else:
                                    current_compliance += 1
                                    continue

                        if current_compliance == amount_of_requirements:
                            logger.info(f'Успешно! Файл "{json_file}" соответствует схеме "{name_event}".\n')

                        else:
                            logger.info(f'Ошибка! Файл "{json_file}" нарушает схему "{name_event}" - поле "{data}" '
                                        f'не обнаружено!')
                            logger.info(f'Для устранения ошибки необходимо добавить поле "{data}".\n')
                            break

            except TypeError:
                logger.info(f'Ошибка! Файл "{json_file}" пуст. Невозможно провести сравнение.')
                logger.info(f'Для устранения ошибки необходимо загрузить "{json_file}" с данными.\n')
            except KeyError:
                logger.info(f'Ошибка! Ни одна из предложенных схем не соответствует файлу "{json_file}".')
                logger.info(f'Для устранения ошибки необходимо загрузить схему для сравнения с данным файлом.\n')

    print('Обработка всех файлов завершена. Пожалуйста, откройте файл "script_result" для получения результатов.')
    logger.info('Обработка всех файлов завершена.')


if __name__ == '__main__':
    print('Спасибо, что решили воспользоваться данным скриптом.')
    print('Пожалуйста, создайте папку и поместите в неё скрипт. Поместите папки с данными в эту же папку.')
    print('Сейчас Вам будет предложено ввести названия папок, содержащих данные для проведения анализа.')

    schema_folder = (input('Введите название папки, содержащей схемы: '))
    json_folder = (input('Введите название папки, содержащей файлы json: '))

    testing_files(schema_folder, json_folder)

    input()
