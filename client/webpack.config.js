const CleanWebpackPlugin = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const path = require('path');
const webpack = require('webpack');
const devMode = process.env.NODE_ENV === 'dev';

const distPath = path.resolve(
  __dirname,
  '../rest_framework_swagger/static/rest_framework_swagger/bundles/'
)

module.exports = {
  entry: {
    app: './index.js',
  },
  output: {
    path: distPath,
    filename: '[name].bundle.js',
    publicPath: '/static/rest_framework_swagger/bundles/',
  },
  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader'
        ]
      },
      {
        test: /\.(js|jsx)$/,
        exclude: /node_modules/,
        use: {
          loader: 'babel-loader'
        }
      }
    ]
  },
  plugins: [
    new CleanWebpackPlugin(
      distPath, {
        root: path.resolve(__dirname, '../')
      }
    ),
    new MiniCssExtractPlugin({
      filename: '[name].bundle.css',
    })
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
