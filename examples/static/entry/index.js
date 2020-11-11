import {init} from '../';
import '../../../packages/flask-state.css';
import {en, ja, zh} from '../../../packages/i18n';
init();
init({dom:document.getElementById('test_id'), lang:zh});

