import {init} from '../../../packages';
import '../../../packages/flask-state.css';
import {zh} from '../../../packages/i18n';
init(null);
init({dom:document.getElementById('test_id'), lang:zh});

