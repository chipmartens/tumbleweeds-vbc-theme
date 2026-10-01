/*global require*/
// Same shape as the mode40 theme: gulp 4 + gulp-sass, compiled CSS is committed.
const gulp = require('gulp');
const plumber = require('gulp-plumber');
const sass = require('gulp-sass')(require('sass'));
const prefix = require('gulp-autoprefixer');
const rename = require('gulp-rename');

gulp.task('sass', function () {
	return gulp.src('./src/scss/app.scss')
		.pipe(plumber())
		.pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
		.pipe(prefix())
		.pipe(rename({ suffix: '.min' }))
		.pipe(gulp.dest('assets/css'));
});

gulp.task('watch', function () {
	gulp.watch('./src/scss/**/*.scss', gulp.series('sass'));
});

gulp.task('default', gulp.series('sass'));
