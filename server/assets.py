from flask_assets import Bundle

common_css = Bundle(
    'css/main.css',
    filters='cssmin',
    output='public/css/common.css'
)

common_js = Bundle(
    'js/vendor/jquery.min.js',
    Bundle(
        'js/main.js',
        filters='jsmin'
    ),
    output='public/js/common.js'
)
