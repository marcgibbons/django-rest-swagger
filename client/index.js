import SwaggerUI from 'swagger-ui'
import 'swagger-ui/dist/swagger-ui.css';
import './styles.css';

let config = Object.assign(
  {
    dom_id: '#rest-swagger-ui',
    spec: window.drsSpec,
  },
  window.drsSettings
);

const csrfTokenInput = window.document.getElementsByName('csrfmiddlewaretoken');

// If present, set CSRF token to request headers
if (csrfTokenInput.length) {
  const csrfToken = csrfTokenInput[0].value;
  config.requestInterceptor = (req) => {
    req.headers['X-CSRFToken'] = csrfToken;
    if (config.acceptHeaderVersion) {
      req.headers['accept'] += '; version=' + config.acceptHeaderVersion;
    }

    req.headers = Object.assign(req.headers, config.customHeaders);

    return req;
  }
}


window.swagger = SwaggerUI(config);
