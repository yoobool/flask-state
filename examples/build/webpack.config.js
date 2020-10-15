const path = require('path');
const HtmlWebpackPlugin = require('html-webpack-plugin');
module.exports = {
    entry: './examples/static/entry/index.js',
    output: {
        filename: 'flask-state.js',
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
            use: ['style-loader', 'css-loader']
        }
        ],
    },
    plugins: [
        new HtmlWebpackPlugin({
            filename:'../../templates/index.html',
            template:'./examples/static/entry/index.html',
        })
    ]
};