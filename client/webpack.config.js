const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');

const distPath = path.resolve(
  __dirname,
  '../rest_framework_swagger/static/rest_framework_swagger/dist/'
)

module.exports = {
  entry: './index.js',
  output: {
    path: path.resolve(distPath),
    filename: 'django-rest-swagger.bundle.js'
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      }
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: '[name].css',
    })
  ]
};
