#    Operation method：
#        Create Flask APP import in project Monitor.init_app() method to initialize the plugin configuration;
#        Stay index.html import flask_state.css and flask_state.js ;
#        Locally index.html Select the element binding ID;
#        The remaining configurable parameters are shown below.
#    Be careful：
#        /v0/state/hoststatus, /v0/state/bindid, /v0/state/language三条路由被插件绑定，请不要起用相同路由
#    建议：
#        本插件部分功能模块基于UNIX系统运行


class DefaultConf:
    def __init__(self):
        # Set the ID of the binding element in HTML, or select the suspension ball binding
        # The default value is(False, 'console_machine_status')
        self.ID_NAME = (True, 'console_machine_status')

        # Set plugin language
        self.LANGUAGE = 'Chinese'

        # Enter the database name, address and conf directory or superior directory, the default is 0
        # If the project has a console_host database, it is not created
        # The default value is('console_host', 0)
        self.ADDRESS = ('console_host', 0)

        # Set the interval to record the local state, with a minimum interval of 10 seconds
        # The default value is 60
        self.SECS = 60

    def set_id_name(self, value=None):
        self.ID_NAME = value

    def set_language(self, value=None):
        self.LANGUAGE = value

    def set_address(self, value=None):
        self.ADDRESS = value

    def set_secs(self, value=None):
        self.SECS = value


default_conf_obj = DefaultConf()
