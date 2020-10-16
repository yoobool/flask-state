import 'flask-state/flask-state.css';
import {zh} from 'flask-state/i18n.js';
const flaskState = require('flask-state');
flaskState.init(document.getElementById('test_id'), zh);
flaskState.init();
