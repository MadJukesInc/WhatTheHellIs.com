from flask_assets import Bundle

common_css = Bundle(
    'semantic/dist/semantic.css',
    'global.css',
    'bower_components/jqcloud2/dist/jqcloud.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    'bower_components/jquery/dist/jquery.js',
    'bower_components/jqcloud2/dist/jqcloud.js',
    'cloud.js',
    'semantic/dist/semantic.js',
    output='public/js/common.js'
)
