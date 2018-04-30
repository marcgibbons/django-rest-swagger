const express = require('express');
const proxy = require('http-proxy-middleware');
const webpack = require('webpack');
const webpackDevMiddleware = require('webpack-dev-middleware');

const app = express();
const config = require('./webpack.config.js');
const compiler = webpack(config);

// Tell express to use the webpack-dev-middleware and use the webpack.config.js
// configuration file as a base.
app.use(
  webpackDevMiddleware(
    compiler, {
      publicPath: config.output.publicPath
    }
  ),
  proxy(
    [
      '!/static/rest_framework_swagger/bundles/**',
    ],
    {
      target: 'http://localhost:8000',  // Assumes Django is running on 8000
    }
  )
);

// Serve the files on port 3000.
app.listen(3000, function () {
  console.log('Example app listening on port 3000!\n');
});
