const path = require('path');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const optimizeCssAssetsPlugin = require('optimize-css-assets-webpack-plugin');
const TerserPlugin = require('terser-webpack-plugin');

module.exports = [{
    // cjs
    entry: './packages/initial.js',
    output: {
        filename: 'flask-state.min.js',
        libraryTarget: "commonjs2",
        path: path.resolve('./packages/cjs/'),
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
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
}, {
    // umd
    entry: './packages/initial.js',
    output: {
        filename: 'flask-state.min.js',
        library: 'flaskState',
        libraryTarget: 'umd',
        path: path.resolve('./packages/umd/')
    },
    module: {
        rules: [{
            test: /\.js$/,
            exclude: /node_modules/,
            loader: 'babel-loader'
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
}, {
    // css
    entry: './examples/static/css-index.js',
    output: {
        path: path.resolve('./packages/')
    },
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
    plugins: [
        new MiniCssExtractPlugin({
            filename: "flask-state.min.css",
        }),
        new optimizeCssAssetsPlugin(),
    ]
}];