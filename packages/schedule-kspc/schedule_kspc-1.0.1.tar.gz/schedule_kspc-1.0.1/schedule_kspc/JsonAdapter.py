from json import dump, load


def _is_data_dict(data: dict):
    if isinstance(data, dict):
        return True
    return False


def _is_data_list(data: list):
    if isinstance(data, list):
        return True
    return False


class JsonAdapter:
    _filename: str

    def __init__(self, filename: str):
        self._filename: str = filename

    @property
    def filename(self):
        return self._filename

    def write(self, data: dict, **kw) -> bool:
        """
        Write dump in json file
        :param data:
        :param kw:
        :return bool:
        """
        if _is_data_dict(data):
            with open(self._filename, 'w', encoding='utf-8') as file:
                dump(data, file, **kw)
            return True
        return False

    def append(self, data: dict, **kw) -> bool:
        """
        Append dump in json file
        :param data: dict
        :param kw:
        :return bool:
        """
        if _is_data_dict(data):
            with open(self._filename, 'r+', encoding='utf-8') as file:
                json_load: dict = load(fp=file)
                json_load.update(data)
                self.write(json_load, **kw)
            return True
        return False

    def append_to_key(self, data: any, key: str = None, **kw):
        if key is not None:
            with open(self._filename, 'r+', encoding='utf-8') as file:
                json_load: dict = load(fp=file)
                if key not in json_load:
                    return False

                value = json_load[key]

                if list == type(value):
                    value.append(data)

                if dict == type(value):
                    value.update(data)

                self.write(json_load, **kw)
            return True
        return False

    def read(self) -> dict:
        """
        Read json file
        :return dict:
        """
        with open(self._filename, 'r', encoding='utf-8') as file:
            return load(fp=file)
