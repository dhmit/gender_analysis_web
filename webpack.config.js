const path = require('path');
const webpack = require('webpack');
const BundleTracker = require('webpack-bundle-tracker');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const ESLintPlugin = require('eslint-webpack-plugin');

module.exports = {
    context: __dirname,
    entry: {
        index: './frontend/index'
    },
    output: {
        path: path.resolve('./assets/bundles/'),
        publicPath: 'http://localhost:3000/static/',
        filename: '[name].bundle.js'
    },
    plugins: [
        new BundleTracker({filename: './webpack-stats.json'}),
        new MiniCssExtractPlugin({ filename: "[name].bundle.css" }),
        new ESLintPlugin(),
    ],
    devServer: {
        port: 3000,
        headers: {
          'Access-Control-Allow-Origin': '*'
        },
        compress: true,
        hot: true
    },
    module: {
        rules: [
          { test: /\.scss$/, use: ["style-loader", "css-loader", "sass-loader"]},
          { test: /\.js|.jsx$/, exclude: /node_modules/, use: "babel-loader"},
        ]
      },
}