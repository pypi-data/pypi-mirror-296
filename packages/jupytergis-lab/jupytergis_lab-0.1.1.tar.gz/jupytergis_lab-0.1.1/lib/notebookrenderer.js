import { WebSocketProvider } from '@jupyter/docprovider';
import { JupyterGISPanel } from '@jupytergis/base';
import { JupyterGISModel } from '@jupytergis/schema';
import { URLExt } from '@jupyterlab/coreutils';
import { ServerConnection } from '@jupyterlab/services';
import { ITranslator, nullTranslator } from '@jupyterlab/translation';
import { MessageLoop } from '@lumino/messaging';
import { Panel, Widget } from '@lumino/widgets';
import { IJupyterYWidgetManager, JupyterYModel } from 'yjs-widgets';
const Y_DOCUMENT_PROVIDER_URL = 'api/collaboration/room';
export const CLASS_NAME = 'jupytergis-notebook-widget';
export class YJupyterGISModel extends JupyterYModel {
}
export class YJupyterGISLuminoWidget extends Panel {
    constructor(options) {
        super();
        this.onResize = () => {
            if (this._jgisWidget) {
                MessageLoop.sendMessage(this._jgisWidget, Widget.ResizeMessage.UnknownSize);
            }
        };
        this.addClass(CLASS_NAME);
        this._jgisWidget = new JupyterGISPanel(options);
        this.addWidget(this._jgisWidget);
    }
}
export const notebookRenderePlugin = {
    id: 'jupytergis:yjswidget-plugin',
    autoStart: true,
    optional: [IJupyterYWidgetManager, ITranslator],
    activate: (app, yWidgetManager, translator) => {
        if (!yWidgetManager) {
            console.error('Missing IJupyterYWidgetManager token!');
            return;
        }
        const labTranslator = translator !== null && translator !== void 0 ? translator : nullTranslator;
        class YJupyterGISModelFactory extends YJupyterGISModel {
            ydocFactory(commMetadata) {
                const { path, format, contentType } = commMetadata;
                this.jupyterGISModel = new JupyterGISModel({});
                const user = app.serviceManager.user;
                if (path && format && contentType) {
                    const server = ServerConnection.makeSettings();
                    const serverUrl = URLExt.join(server.wsUrl, Y_DOCUMENT_PROVIDER_URL);
                    const ywsProvider = new WebSocketProvider({
                        url: serverUrl,
                        path,
                        format,
                        contentType,
                        model: this.jupyterGISModel.sharedModel,
                        user,
                        translator: labTranslator.load('jupyterlab')
                    });
                    this.jupyterGISModel.disposed.connect(() => {
                        ywsProvider.dispose();
                    });
                }
                else {
                    const awareness = this.jupyterGISModel.sharedModel.awareness;
                    const _onUserChanged = (user) => {
                        awareness.setLocalStateField('user', user.identity);
                    };
                    user.ready
                        .then(() => {
                        _onUserChanged(user);
                    })
                        .catch(e => console.error(e));
                    user.userChanged.connect(_onUserChanged, this);
                }
                return this.jupyterGISModel.sharedModel.ydoc;
            }
        }
        class YJupyterGISWidget {
            constructor(yModel, node) {
                this.yModel = yModel;
                this.node = node;
                const widget = new YJupyterGISLuminoWidget({
                    model: yModel.jupyterGISModel
                });
                // Widget.attach(widget, node);
                MessageLoop.sendMessage(widget, Widget.Msg.BeforeAttach);
                node.appendChild(widget.node);
                MessageLoop.sendMessage(widget, Widget.Msg.AfterAttach);
            }
        }
        yWidgetManager.registerWidget('@jupytergis:widget', YJupyterGISModelFactory, YJupyterGISWidget);
    }
};
