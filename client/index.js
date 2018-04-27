import SwaggerUI from 'swagger-ui'
import 'swagger-ui/dist/swagger-ui.css';
import './styles.css'


window.drsSettings.dom_id = '#rest-swagger-ui';
window.drsSettings.spec = window.drsSpec;
const csrfTokenInput = window.document.getElementsByName('csrfmiddlewaretoken');

// If present, set CSRF token to request headers
if (csrfTokenInput.length) {
  const csrfToken = csrfTokenInput[0].value;
  window.drsSettings.requestInterceptor = (req) => {
    req.headers['X-CSRFToken'] = csrfToken;
    return req;
  }
}

window.swagger = SwaggerUI(window.drsSettings);
