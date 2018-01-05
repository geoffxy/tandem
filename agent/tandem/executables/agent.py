import logging
from tandem.io.std_streams import StdStreams
from tandem.protocol.editor.handler import EditorProtocolHandler
from concurrent.futures import ThreadPoolExecutor


class TandemAgent:
    def __init__(self):
        self._std_streams = StdStreams(self._on_std_input)
        self._editor_protocol = EditorProtocolHandler(self._std_streams)
        self._main_executor = ThreadPoolExecutor(max_workers=1)

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.stop()

    def start(self):
        self._std_streams.start()
        logging.info("Tandem Agent has started")

    def stop(self):
        self._std_streams.stop()
        self._main_executor.shutdown()
        logging.info("Tandem Agent has shut down")

    def _on_std_input(self, data):
        # Called by _std_streams after receiving a new message from the plugin
        self._main_executor.submit(self._editor_protocol.handle_message, data)
