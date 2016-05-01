/* eslint-disable */
var path = require('path');
// var ExtractTextPlugin = require('extract-text-webpack-plugin');
// var extractCSS = new ExtractTextPlugin('css/main.css');

module.exports = {
  entry: {
    client: './client/app',
  },

  output: {
    path: path.resolve('static'),
    filename: '[name].js',
  },

  module: {
    loaders: [
      {
        test: /\.css$/,
        loader: 'style-loader!css-loader',
        // loader: extractCSS.extract(['css-loader']),
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|build)/,
        loader: 'babel-loader',
      },
    ],
  },
  // plugins: [
  //   extractCSS,
  // ],
};
