/* eslint-disable */
var path = require('path');
var ExtractTextPlugin = require('extract-text-webpack-plugin');
var extractCSS = new ExtractTextPlugin('css/main.css');

module.exports = {
  entry: {
    client: './client/app',
  },

  output: {
    path: path.resolve('build'),
    filename: 'static/[name].js',
  },

  module: {
    loaders: [
      {
        test: /\.scss$/,
        exclude: /node_modules/,
        loader: extractCSS.extract(['css-loader']),
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|build)/,
        loader: 'babel-loader',
      },
    ],
  },

  plugins: [
    extractCSS,
  ],
};
