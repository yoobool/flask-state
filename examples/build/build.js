const webpack = require('webpack');
const mainConfig = require('./webpack.config');

const developmentBuild = (compiler) => {
    compiler.watch({
        aggregateTimeout: 300,
        ignored: /node_modules/,
        poll: undefined
    }, (err, stats) => {
        if (err) return console.error(err);

        console.log(stats.toString({
            chunks: false,
            colors: true
        }));
    });
};

const build = () => {
    let buildFun = developmentBuild;

    const compiler = webpack([mainConfig]);

    // build
    buildFun(compiler);
};


build();