/* global Node */
/* global window */
import { ipcRenderer } from 'electron';
import constants from './constants';

const findElement = (node) => {
  let curr = node;
  while (curr != null) {
    if (curr.nodeType === Node.ELEMENT_NODE && (!!curr.id || !!curr.className)) {
      return curr;
    }
    curr = curr.parentNode;
  }
  return null;
};

window.attachHooks = () => {
  window.addEventListener('keyup', (e) => {
    ipcRenderer.sendToHost(constants.RecorderWebView.EventType.KEYUP, e.key);
  });
  window.addEventListener('click', (e) => {
    const el = findElement(e.target);
    if (el == null) return;
    const attributesNodeMap = el.attributes;
    const elementAttributes = {};
    for (let i = 0; i < attributesNodeMap.length; i += 1) {
      elementAttributes[attributesNodeMap[i].name] = attributesNodeMap[i].value;
    }

    const attributes = {
      tagType: el.tagName,
      id: el.id,
      className: el.className,
      text: el.textContent,
      attributes: elementAttributes,
    };
    ipcRenderer.sendToHost(constants.RecorderWebView.EventType.CLICK, attributes);
  });
  ipcRenderer.sendToHost(constants.RecorderWebView.EventType.READY, '--- Event hooks attached ---');
};
