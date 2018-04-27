const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const webpack = require('webpack');

const distPath = path.resolve(
  __dirname,
  '../rest_framework_swagger/static/rest_framework_swagger/dist/'
)

module.exports = {
  entry: {
    app: './index.js',
  },
  output: {
    path: distPath,
    filename: '[name].bundle.js'
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
      filename: '[name].bundle.css',
    }),
  ],
  optimization: {
    splitChunks: {
      cacheGroups: {
         commons: {
           test: /[\\/]node_modules[\\/]/,
           name: "vendors",
           chunks: "all"
         }
      }
    }
  }
};
