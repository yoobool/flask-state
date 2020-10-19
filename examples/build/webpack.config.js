const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const optimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
const BundleAnalyzerPlugin = require('webpack-bundle-analyzer').BundleAnalyzerPlugin
module.exports = {
    // umd
    // entry: './examples/static/umd/flask-state.js',
    // output: {
    //     filename: 'flask-state.min.js',
    //     library: 'flaskState',
    //     libraryTarget: 'umd',
    //     path: path.resolve('./examples/static/', 'dist')
    // },

    // cjs
    // entry: './examples/static/cjs/flask-state.js',
    // output: {
    //     filename: 'flask-state.min.js',
    //     libraryTarget: "commonjs2",
    //     path: path.resolve('./examples/static/', 'dist')
    // },

    // entry
    entry: './examples/static/entry/index.js',
    output: {
        filename: 'flask-state.min.js',
        path: path.resolve('./examples/static/', 'dist')
    },
    mode: 'development',
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
        }, {
            test: /\.css$/,
            use: [
                {
                    loader: MiniCssExtractPlugin.loader,
                    options: {
                        publicPath: '../'
                    }
                }, 'css-loader']
        }
        ],
    },
    optimization: {
        minimizer: [new TerserPlugin({
            terserOptions: {
                output: {
                    comments: false,
                },
                compress: {
                    pure_funcs: ["console.log"]
                },
            },
            extractComments: false
        })],
        splitChunks: {
            chunks: 'all',
            name: false,
        },
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename: '../../templates/index.html',
            template: './examples/static/entry/index.html',
        }),
        new MiniCssExtractPlugin({
            filename: "css/flask-state.css",
            chunkFilename: 'css/[name].[contenthash:8].chunk.css',
        }),
        new optimizeCssAssetsPlugin(),
    ]
};