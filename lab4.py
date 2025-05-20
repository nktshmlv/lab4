# Изменение для создания конфликта из оригинального репозитория

import csv
import os


class Call:
    def __init__(self, number, phone, reason, resolved):
        self.__dict__['_data'] = {}
        self.number = int(number)
        self.phone = phone
        self.reason = reason
        self.resolved = resolved

    def __setattr__(self, key, value):
        if key == 'number':
            self._data['№'] = int(value)
        elif key == 'phone':
            self._data['телефон'] = value
        elif key == 'reason':
            self._data['причина обращения'] = value
        elif key == 'resolved':
            self._data['решена проблема'] = value
        else:
            raise AttributeError(f"Недопустимый атрибут: {key}")

    def __getattr__(self, item):
        mapping = {
            'number': '№',
            'phone': 'телефон',
            'reason': 'причина обращения',
            'resolved': 'решена проблема'
        }
        if item in mapping:
            return self._data[mapping[item]]
        raise AttributeError(f"Нет такого атрибута: {item}")

    def __repr__(self):
        return f"Звонок({self.number}, {self.phone}, {self.reason}, {self.resolved})"

    def to_dict(self):
        return self._data


class CallLog:
    def __init__(self, filepath):
        self.filepath = filepath
        self.calls = []
        self._index = 0
        if os.path.exists(filepath):
            self.load_from_file()

    def __getitem__(self, index):
        return self.calls[index]

    def __iter__(self):
        self._index = 0
        return self

    def __next__(self):
        if self._index >= len(self.calls):
            raise StopIteration
        call = self.calls[self._index]
        self._index += 1
        return call

    def add_call(self, call: Call):
        self.calls.append(call)

    def load_from_file(self):
        with open(self.filepath, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                call = Call(
                    number=row['№'],
                    phone=row['телефон'],
                    reason=row['причина обращения'],
                    resolved=row['решена проблема']
                )
                self.calls.append(call)

    def save_to_file(self):
        with open(self.filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=['№', 'телефон', 'причина обращения', 'решена проблема'], delimiter=';')
            writer.writeheader()
            writer.writerows(call.to_dict() for call in self.calls)

    def sort_by_reason(self):
        return sorted(self.calls, key=lambda c: c.reason)

    def sort_by_number(self):
        return sorted(self.calls, key=lambda c: c.number)

    def unresolved_calls(self):
        return (call for call in self.calls if call.resolved.lower() == 'нет')

    def next_number(self):
        if not self.calls:
            return 1
        return max(call.number for call in self.calls) + 1

    @staticmethod
    def count_files_in_directory(path):
        try:
            return len([name for name in os.listdir(path) if os.path.isfile(os.path.join(path, name))])
        except FileNotFoundError:
            print("Указанная директория не найдена.")
            return 0


if __name__ == '__main__':
    path = input("Введите путь к директории: ")
    print(f"Количество файлов в директории: {CallLog.count_files_in_directory(path)}")

    filename = os.path.join(path, 'data.csv')
    log = CallLog(filename)

    print("\nСортировка по причине обращения:")
    for call in log.sort_by_reason():
        print(call)

    print("\nСортировка по номеру:")
    for call in log.sort_by_number():
        print(call)

    print("\nНерешённые проблемы:")
    for call in log.unresolved_calls():
        print(call)

    if input("\nДобавить новые данные? (да/нет): ").lower() == 'да':
        while True:
            phone = input("\nТелефон (или 'стоп'): ")
            if phone.lower() == 'стоп':
                break
            reason = input("Причина обращения: ")
            resolved = input("Решена проблема (да/нет): ")

            new_call = Call(
                number=log.next_number(),
                phone=phone,
                reason=reason,
                resolved=resolved
            )
            log.add_call(new_call)

        log.save_to_file()
        print("Новые данные сохранены.")

# второй коммит

# feature-2

# feature-1