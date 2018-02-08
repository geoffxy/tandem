import logging
import json
import tandem.protocol.editor.messages as em
import tandem.protocol.interagent.messages as im


class InteragentProtocolHandler:
    def __init__(self, std_streams, peer_manager, document):
        self._std_streams = std_streams
        self._peer_manager = peer_manager
        self._document = document
        self._next_editor_sequence = 0

    def handle_message(self, raw_data, sender_address):
        try:
            message = im.deserialize(raw_data)
            if type(message) is im.Hello:
                self._handle_hello(message, sender_address)
            elif type(message) is im.Bye:
                self._handle_bye(message, sender_address)
            elif type(message) is im.RawNewOperations:
                self._handle_new_operations(message, sender_address)
            else:
                logging.debug("Received unknown interagent message.")
        except im.InteragentProtocolMarshalError:
            logging.info("Ignoring invalid interagent protocol message.")
        except:
            logging.exception(
                "Exception when handling interagent protocol message:")
            raise

    def _handle_hello(self, message, sender_address):
        self._peer_manager.register_peer(sender_address)

    def _handle_bye(self, message, sender_address):
        self._peer_manager.remove_peer(sender_address)

    def _handle_new_operations(self, message, sender_address):
        operations_list = json.loads(message.operations_binary.decode("utf-8"))
        self._document.enqueue_remote_operations(operations_list)
        if not self._document.write_request_sent():
            self._std_streams.write_string_message(
                em.serialize(em.WriteRequest(self._next_editor_sequence)),
            )
            self._document.set_write_request_sent(True)
            logging.debug("Sent write request seq: {}".format(self._next_editor_sequence))
            self._next_editor_sequence += 1
