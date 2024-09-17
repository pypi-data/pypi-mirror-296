import {
    JupyterFrontEnd,
    JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
    IEditorLanguageRegistry
} from '@jupyterlab/codemirror';

import {esl} from './esl';

/**
 * Initialization data for the jupyterlab-esl extension.
 */
const plugin: JupyterFrontEndPlugin<void> = {
    id: 'jupyterlab-esl:plugin',
    description: 'ESL support for jupyterlab',
    autoStart: true,
    requires: [IEditorLanguageRegistry],
    activate: (app: JupyterFrontEnd, registry: IEditorLanguageRegistry) => {
        console.log('JupyterLab extension jupyterlab-esl is activated!');

        registry.addLanguage({
            name: 'ESL',
            mime: 'text/esl',
            extensions: ['esl'],
            support: esl()
        });
    }
};

export default plugin;
