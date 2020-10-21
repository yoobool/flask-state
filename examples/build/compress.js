const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const optimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');
module.exports = {
    // umd
    // entry: './examples/static/umd/flask-state.js',
    // output: {
    //     filename: 'flask-state.min.js',
    //     library: 'flaskState',
    //     libraryTarget: 'umd',
    //     path: path.resolve('./examples/compress/umd/')
    // },

    // cjs
    // entry: './examples/static/cjs/flask-state.js',
    // output: {
    //     filename: 'flask-state.min.js',
    //     libraryTarget: "commonjs2",
    //     path: path.resolve('./examples/compress/cjs/')
    // },

    // CSS file
    // entry: './examples/static/css-index.js',
    // output: {
    //     path: path.resolve('./examples/compress/cjs/')
    // },
    // output: {
    //     path: path.resolve('./examples/compress/umd/')
    // },

    mode: 'production',
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
    },
    plugins: [
        new MiniCssExtractPlugin({
            filename: "css/flask-state.min.css",
        }),
        new optimizeCssAssetsPlugin(),
    ]
};