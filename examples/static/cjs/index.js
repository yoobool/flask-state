'use strict';


if (process.env.NODE_ENV === 'production') {
    module.exports = require('./flask-state.min.js');
} else {
    module.exports = require('./flask-state.js');
}