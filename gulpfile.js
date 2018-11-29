const gulp = require('gulp');
const browserSync = require('browser-sync').create();
const sass = require('gulp-sass');

// Compile SASS

gulp.task('sass', function(){
	return gulp.src(['static/scss/*.scss'])
		.pipe(sass())
		.pipe(gulp.dest('static/css'))
		.pipe(browserSync.stream());
});

// Watch and Serve
gulp.task('serve',['sass'],function(){
	browserSync.init({
		server: './templates'
	});
	gulp.watch(['static/scss/*.scss'], ['sass']);
	gulp.watch(['static/*.html']).on('change', browserSync.reload);
});

// Default
gulp.task('default', ['serve']);