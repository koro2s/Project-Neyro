import argparse
from deepface import DeepFace
import json


def load_mood_playlist_mapping(filename='mood_playlist_mapping_soundcloud.json'):
    """
    Загружает JSON-словарь, связывающий эмоции с плейлистами SoundCloud.

    :param filename: Путь к JSON-файлу с данными (по умолчанию 'mood_playlist_mapping_soundcloud.json').
    :return: Словарь с данными из файла или пустой словарь в случае ошибки.
    """
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            data = json.load(file)  # Считываем содержимое JSON-файла
        return data  # Возвращаем загруженные данные
    except FileNotFoundError:
        print(f"[!] Файл {filename} не найден. Проверьте путь.")  # Обработка отсутствия файла
        return {}
    except json.JSONDecodeError:
        print("[!] Ошибка декодирования JSON. Проверьте формат файла.")  # Обработка ошибок чтения JSON
        return {}


def get_playlist_link(emotion, playlist_mapping):
    """
    Возвращает ссылку на плейлист на основе эмоции.

    :param emotion: Словарь с данными о эмоциях.
    :param playlist_mapping: Словарь, связывающий эмоции с плейлистами.
    :return: Ссылка на плейлист, соответствующий доминирующей эмоции.
    """
    dominant_emotion = extract_dominant_emotion(emotion)  # Получаем доминирующую эмоцию
    return find_playlist(dominant_emotion, playlist_mapping)  # Получаем ссылку на плейлист


def extract_dominant_emotion(emotion):
    """
    Извлекает доминирующую эмоцию из результата анализа.

    :param emotion: Словарь с данными о эмоциях.
    :return: Строка с доминирующей эмоцией или 'neutral', если эмоция отсутствует.
    """
    return emotion.get('dominant_emotion', 'neutral')  # Если эмоция отсутствует, возвращаем 'neutral'


def find_playlist(dominant_emotion, playlist_mapping):
    """
    Ищет ссылку на плейлист по переданной эмоции.

    :param dominant_emotion: Строка с доминирующей эмоцией.
    :param playlist_mapping: Словарь, связывающий эмоции с плейлистами.
    :return: Ссылка на плейлист или ссылка на плейлист по умолчанию, если не найдено.
    """
    playlist_link = playlist_mapping.get(dominant_emotion)  # Пытаемся найти плейлист
    if not playlist_link:
        playlist_link = "https://soundcloud.com/search?q=default playlist"  # Значение по умолчанию
    return playlist_link


def print_analysis_result(result_dict):
    """
    Выводит данные анализа лица.

    :param result_dict: Словарь с результатами анализа лица.
    """
    print_age_info(result_dict.get('age'))  # Выводим возраст
    print_gender_info(result_dict.get('gender'))  # Выводим пол
    print_race_info(result_dict.get('race', {}))  # Выводим расы
    print_emotion_info(result_dict.get('emotion', {}))  # Выводим эмоции


def print_age_info(age):
    """
    Выводит информацию о возрасте.

    :param age: Возраст человека.
    """
    print(f"[+] Возраст: {age}")


def print_gender_info(gender):
    """
    Выводит информацию о поле.

    :param gender: Пол человека.
    """
    print(f"[+] Пол: {gender}")


def print_race_info(race_dict):
    """
    Выводит информацию о расах.

    :param race_dict: Словарь с данными о расах и их процентах.
    """
    print("[+] Раса:")
    for race, percentage in race_dict.items():
        print(f"{race} - {round(percentage, 2)}%")


def print_emotion_info(emotion_dict):
    """
    Выводит информацию об эмоциях.

    :param emotion_dict: Словарь с данными о эмоциях и их процентах.
    """
    print("[+] Эмоции:")
    for emotion, percentage in emotion_dict.items():
        print(f"{emotion} - {round(percentage, 2)}%")


def face_analyse(image_path):
    """
    Выполняет анализ лица и связывает эмоции с плейлистами.

    :param image_path: Путь к изображению для анализа.
    """
    try:
        # Анализ изображения с помощью DeepFace
        result = DeepFace.analyze(img_path=image_path, actions=['emotion', 'age', 'gender', 'race'])

        # Если результат - список, берем первый элемент
        result_dict = process_analysis_result(result)

        # Сохраняем результат анализа в файл
        save_analysis_result(result_dict, 'face_analyse.json')

        # Выводим данные анализа
        print_analysis_result(result_dict)

        # Загрузка данных соответствия эмоций и плейлистов
        playlist_mapping = load_mood_playlist_mapping()

        # Получаем и выводим плейлист
        dominant_emotion = extract_dominant_emotion(result_dict)
        playlist_link = find_playlist(dominant_emotion, playlist_mapping)
        print(f"Ссылка на плейлист для текущей эмоции ({dominant_emotion}): {playlist_link}")

    except FileNotFoundError as fnf_error:
        print(f"[!] Ошибка: файл не найден - {fnf_error}")
    except json.JSONDecodeError as json_error:
        print(f"[!] Ошибка: некорректный JSON - {json_error}")
    except Exception as ex:
        print(f"[!] Произошла ошибка: {ex}")


def process_analysis_result(result):
    """
    Обрабатывает результат анализа, чтобы извлечь словарь.

    :param result: Результат анализа, который может быть списком или словарем.
    :return: Словарь с результатами анализа.
    """
    return result[0] if isinstance(result, list) else result


def save_analysis_result(result_dict, filename):
    """
    Сохраняет результат анализа в JSON-файл.

    :param result_dict: Словарь с результатами анализа для сохранения.
    :param filename: Путь к файлу для сохранения результата.
    """
    try:
        with open(filename, 'w', encoding='utf-8') as file:
            json.dump(result_dict, file, indent=4, ensure_ascii=False)
    except Exception as ex:
        print(f"[!] Ошибка при сохранении файла: {ex}")


def main():
    """
    Запускает процесс анализа лица.
    """
    parser = argparse.ArgumentParser(description="Анализ изображения лица и подбор плейлиста по эмоции.")
    parser.add_argument("image_path", help="Путь к изображению для анализа")  # Путь к изображению
    args = parser.parse_args()  # Обрабатываем аргументы командной строки

    # Выполняем анализ лица
    face_analyse(args.image_path)


if __name__ == '__main__':
    main()

