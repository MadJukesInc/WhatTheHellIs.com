var
    gulp = require('gulp-help')( require('gulp') ),
    build = require('./server/static/semantic/tasks/rtl/build')
;

gulp.task('default', false, [
    'watch'
]);
gulp.task('build', 'Builds semantic sources', build);