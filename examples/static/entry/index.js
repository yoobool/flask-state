import {init} from '../cjs';
import '../cjs/flask-state.css';
import {zh} from '../cjs/i18n.js';
init(null);
init({dom:document.getElementById('test_id'), lang:zh});

