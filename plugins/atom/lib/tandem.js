'use babel';

import { CompositeDisposable } from 'atom';
import TandemPlugin from './tandemPlugin';
import ConnectView from './connectView';

export default {

  _tandemAgent: null,
  _subscriptions: null,
  _connectPanel: null,

  activate() {
    this._tandemAgent = new TandemPlugin();

    const connectView = new ConnectView(
      this._connectToHost.bind(this),
      () => { this._inputPanel.hide(); },
    );
    this._inputPanel = atom.workspace.addModalPanel({
      item: connectView,
      visible: false,
    });

    this._subscriptions = new CompositeDisposable();
    this._subscriptions.add(atom.commands.add('atom-workspace', {
      'tandem:join-existing-session': () => this._connect(),
    }));
    this._subscriptions.add(atom.commands.add('atom-workspace', {
      'tandem:start-session': () => this._start(),
    }));
    this._subscriptions.add(atom.commands.add('atom-workspace', {
      'tandem:leave-session': () => this._stop(),
    }));
  },

  deactivate() {
    if (this._tandemAgent && this._tandemAgent.isActive()) {
      this._tandemAgent.stop();
    }
    this._subscriptions.dispose();
  },

  _getTextEditor(newEditor) {
    return new Promise((res) => {
      if (newEditor) {
        return res(atom.workspace.open());
      }
      const editor = atom.workspace.getActiveTextEditor();
      if (editor) {
        return res(editor);
      }
      // Open a new text editor if one is not open
      return res(atom.workspace.open());
    });
  },

  _start() {
    this._getTextEditor().then((editor) => {
      this._tandemAgent.start(editor.getBuffer());
    });
  },

  _connect() {
    this._inputPanel.show();
  },

  _connectToHost(input) {
    this._inputPanel.hide();

    const args = input.split(' ');
    const ip = args[0];
    const port = args[1];

    this._getTextEditor(/* newEditor */ true).then((editor) => {
      this._tandemAgent.start(editor.getBuffer(), ip, port);
    });
  },

  _stop() {
    this._tandemAgent.stop();
  },
};
