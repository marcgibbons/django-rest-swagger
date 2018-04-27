import SwaggerUI from 'swagger-ui'
import 'swagger-ui/dist/swagger-ui.css';
import './styles.css'

window.drsSettings.dom_id = '#rest-swagger-ui';
window.drsSettings.spec = window.drsSpec;

window.swagger = SwaggerUI(window.drsSettings);
