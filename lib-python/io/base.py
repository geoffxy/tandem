from threading import Thread
from tandem.shared.utils.proxy import ProxyUtils


class InterfaceDataBase(object):
    def __init__(self, data):
        self._data = data

    def get_data(self):
        return self._data

    def is_empty(self):
        return self._data is None


class InterfaceBase(object):
    data_class = InterfaceDataBase

    def __init__(self, incoming_data_handler, proxies=[]):
        self._incoming_data_handler = incoming_data_handler
        self._reader = Thread(target=self._read_data)
        self._proxies = proxies

    def start(self):
        self._reader.start()

    def stop(self):
        self._reader.join()

    def generate_io_data(self, *args, **kwargs):
        new_args, new_kwargs = ProxyUtils.run(
            self._proxies,
            'pre_generate_io_data',
            (args, kwargs),
        )
        return self._generate_io_data(*new_args, **new_kwargs)

    def write_io_data(self, io_data):
        return self._write_io_data(io_data)

    def _generate_io_data(self, *args, **kwargs):
        return InterfaceDataBase(*args, **kwargs)

    def _write_io_data(self, io_data):
        raise

    def _read_data(self):
        raise

    def _received_data(self, *args, **kwargs):
        def retrieve_io_data():
            new_args, new_kwargs = ProxyUtils.run(
                self._proxies,
                'on_retrieve_io_data',
                (args, kwargs),
            )
            return self.data_class(*new_args, **new_kwargs)

        self._incoming_data_handler(retrieve_io_data)
