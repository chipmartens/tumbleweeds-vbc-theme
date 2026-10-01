/*global require*/
// Same shape as the mode40 theme: gulp 4 + gulp-sass + webpack-stream. Compiled CSS and JS are committed.
require('dotenv').config();

const gulp = require('gulp');
const webpackStream = require('webpack-stream');
const plumber = require('gulp-plumber');
const notify = require('gulp-notify');
const sass = require('gulp-sass')(require('sass'));
const prefix = require('gulp-autoprefixer');
const sourcemaps = require('gulp-sourcemaps');
const rename = require('gulp-rename');
const imagemin = require('gulp-imagemin');
const browserSync = require('browser-sync').create();

// Get proxy URL from environment variable or use default
const proxyUrl = process.env.PROXY_URL || 'http://tumbleweeds.local/';

//error notification settings for plumber
var plumberErrorHandler = {
    errorHandler: notify.onError({
        title: 'Gulp Error',
        message: '<%= error.message %>'
    })
};

var sassOptions = {
    outputStyle: 'compressed'
};

gulp.task('sass', function() {
    return gulp.src(['./src/scss/app.scss', './src/scss/editor-style.scss'])
        .pipe(plumber(plumberErrorHandler))
        .pipe(sourcemaps.init())
        .pipe(sass(sassOptions))
        .pipe(prefix())
        .pipe(rename({ suffix: '.min' }))
        .pipe(sourcemaps.write('.'))
        .pipe(gulp.dest('assets/css'));
});

gulp.task('webpack', function() {
    return gulp.src('./src/js/entry.js')
        .pipe(plumber(plumberErrorHandler))
        .pipe(webpackStream(require('./webpack.config.js')))
        .pipe(gulp.dest('dist/js'));
});

gulp.task('img', function() {
    return gulp.src('./src/img/*.{png,jpg,gif,svg}')
        .pipe(plumber(plumberErrorHandler))
        .pipe(imagemin([
            imagemin.mozjpeg({ progressive: true }),
            imagemin.optipng({ optimizationLevel: 5 }),
            imagemin.svgo({
                plugins: [
                    { cleanupIDs: false },
                    { removeViewBox: false },
                    { convertPathData: false }
                ]
            }),
        ]))
        .pipe(gulp.dest('assets/img'));
});

gulp.task('build', gulp.series('sass', 'webpack', 'img'));

gulp.task('watch', function() {
    // browsersync listen
    browserSync.init({
        proxy: proxyUrl,
        port: 3000,
        open: false,
        notify: false,
        online: false,
        ui: false,
        logLevel: 'silent'
    });
    // Watch SCSS changes.
    gulp.watch('./src/scss/**/*.scss', gulp.series('sass')).on('change', browserSync.reload);
    // Watch js changes.
    gulp.watch('./src/js/**/*.js', gulp.series('webpack')).on('change', browserSync.reload);
    // Watch image changes.
    gulp.watch('./src/img/*.{png,jpg,gif,svg}', gulp.series('img')).on('change', browserSync.reload);
});

gulp.task('default', gulp.series('sass', 'webpack', 'img', 'watch'));
