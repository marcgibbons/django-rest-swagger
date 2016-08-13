$(function () {
  hljs.configure({
    highlightSizeThreshold: 5000
  });

  // Pre load translate...
  if(window.SwaggerTranslator) {
    window.SwaggerTranslator.translate();
  }
  var settings = {
    url: window.location.pathname + '?format=openapi',
    dom_id: "swagger-ui-container",
    onComplete: function(swaggerApi, swaggerUi){
      if(typeof initOAuth == "function") {
        initOAuth({
          clientId: "your-client-id",
          clientSecret: "your-client-secret-if-required",
          realm: "your-realms",
          appName: "your-app-name",
          scopeSeparator: ",",
          additionalQueryStringParams: {}
        });
      }

      if(window.SwaggerTranslator) {
        window.SwaggerTranslator.translate();
      }
      addCsrfTokenHeaders();
    },
    onFailure: function(data) {
      log("Unable to Load SwaggerUI");
    },
  };
  $.extend(settings, JSON.parse($('#drs-settings').html()));

  window.swaggerUi = new SwaggerUi(settings);

  window.swaggerUi.load();

  function addCsrfTokenHeaders() {
    var token = $('[name="csrfmiddlewaretoken"]')[0];
    if (!token) {
      return;
    }
    swaggerUi.api.clientAuthorizations.add(
      'csrf_token',
      new SwaggerClient.ApiKeyAuthorization(
        'X-CSRFToken',
        token.value,
        'header'
      )
    );
  }

  function log() {
    if ('console' in window) {
      console.log.apply(console, arguments);
    }
  }
});
