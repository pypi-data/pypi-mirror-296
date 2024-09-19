import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { requestAPI } from './handler';

import { IStatusBar } from '@jupyterlab/statusbar';

import { Widget } from '@lumino/widgets';

const RED_TEXT = 'jl-server-timer-red';

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab-server-timer:plugin',
  description:
    'A JupyterLab extension that displays the remaining server run time in the status bar.',
  autoStart: true,
  requires: [IStatusBar],
  activate: (app: JupyterFrontEnd, statusBar: IStatusBar) => {
    console.log('JupyterLab extension jupyterlab-server-timer is activated!');
    requestAPI<any>('get-life-span')
      .then(data => {
        const divNode = document.createElement('div');
        const spanNode = document.createElement('span');
        divNode.appendChild(spanNode);

        // Figure out later how to do this cleaner.
        spanNode.classList.add('jp-StatusBar-TextItem');

        function update_text() {
          // Time stamp is always in UTC.
          const now = new Date();
          const timestamp = (now.getTime() / 1000) | 0;
          let remain = (data['end-time'] - timestamp) | 0;
          if (remain < 0) {
            remain = 0;
          }

          // Build time string as HH:MM.
          remain = remain / 60;
          let hours = ((remain / 60) | 0).toString();
          if (hours.length < 2) {
            hours = '0' + hours;
          }
          let minutes = (remain % 60 | 0).toString();
          if (minutes.length < 2) {
            minutes = '0' + minutes;
          }
          const time = '<b>' + hours + ':' + minutes + '</b>';

          let text = 'Time until server terminates: ' + time;
          if (remain < 15) {
            text = '<b>SERVER TERMINATES ANY MOMENT NOW - SAVE YOUR WORK!</b>';
          }

          // Red and blinking text to catch attention.
          if (remain < 120) {
            if (remain % 2 === 0) {
              spanNode.classList.add(RED_TEXT);
            } else {
              spanNode.classList.remove(RED_TEXT);
            }
          } else if (remain < 300) {
            spanNode.classList.add(RED_TEXT);
          }
          spanNode.innerHTML = text;
        }

        // Update every second.
        setInterval(() => {
          update_text();
        }, 1000);

        // First update.
        update_text();

        const statusWidget = new Widget({ node: divNode });

        statusBar.registerStatusItem('lab-status', {
          align: 'middle',
          item: statusWidget
        });
      })
      .catch(reason => {
        console.error(
          `The jupyterlab_server_timer server extension appears to be missing.\n${reason}`
        );
      });
  }
};

export default plugin;
