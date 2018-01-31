import os
import sys
from threading import Event
import neovim

plugin_location = os.path.dirname(os.path.abspath(__file__))
if plugin_location not in sys.path:
    sys.path.insert(0, plugin_location)

import tandem_lib.tandem_plugin as plugin
import tandem_lib.agent.tandem.protocol.editor.messages as m


@neovim.plugin
class TandemNeovimPlugin(object):
    def __init__(self, vim):
        self._vim = vim
        self._tandem = plugin.TandemPlugin(
            vim=vim,
            message_handler=self._handle_message,
        )
        self._text_applied = Event()
        self._message = None

    @neovim.command("Tandem", nargs="*", sync=True)
    def start(self, args):
        host_ip = args[0] if len(args) >= 1 else None
        port = args[1] if len(args) >= 2 else None
        self._tandem.start(host_ip, port)

    @neovim.command("TandemStop", nargs="*", sync=True)
    def stop(self, args):
        self._tandem.stop(invoked_from_autocmd=False)

    @neovim.autocmd("VimLeave", sync=True)
    def on_vim_leave(self):
        self._tandem.stop(invoked_from_autocmd=True)

    @neovim.autocmd("TextChanged", sync=False)
    def on_text_changed(self):
        if not plugin.is_active:
            return
        self._tandem.check_buffer()

    @neovim.autocmd("TextChangedI", sync=False)
    def on_text_changed_i(self):
        if not plugin.is_active:
            return
        self._tandem.check_buffer()

    @neovim.function("TandemHandleWriteRequest", sync=True)
    def tandem_handle_write_request(self, args):
        try:
            self._tandem.handle_write_request(message=self._message)
        finally:
            self._vim.async_call(lambda: self._text_applied.set())

    def _handle_message(self, message):
        if isinstance(message, m.WriteRequest):
            self._message = message
            self._text_applied.clear()
            self._vim.async_call(
                lambda: self._vim.funcs.TandemHandleWriteRequest(async=True),
            )
            self._text_applied.wait()
