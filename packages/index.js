'use strict';


if (process.env.NODE_ENV === 'production') {
    module.exports = require('./cjs/flask-state.min.js');
} else {
    module.exports = require('./cjs/flask-state.js');
}