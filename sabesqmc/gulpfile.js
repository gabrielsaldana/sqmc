'use strict';

var gulp = require('gulp'),
  pjson = require('./package.json'),
  sass = require('gulp-sass'),
  autoprefixer = require('gulp-autoprefixer'),
  cssnano = require('gulp-cssnano'),
  rename = require('gulp-rename'),
  plumber = require('gulp-plumber'),
  pixrem = require('gulp-pixrem'),
  uglify = require('gulp-uglify'),
  exec = require('child_process').exec,
  runSequence = require('run-sequence'),
  browserSync = require('browser-sync').create(),
  reload = browserSync.reload;

// Relative paths function
var pathsConfig = function() {
  //this.app = "./" + ('sabesqmc');

  return {
    app: './',
    templates: './templates',
    css: './static/css',
    sass: './static/sass',
    fonts: './static/fonts',
    images: './static/images',
    js: './static/js'
  };
};

var paths = pathsConfig();

////////////////////////////////
//          Tasks             //
////////////////////////////////

// Styles autoprefixing and minification
gulp.task('styles', function() {
  return gulp.src(paths.sass + '/styles.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(plumber()) // Checks for errors
    .pipe(autoprefixer({
      browsers: ['last 2 version']
    })) // Adds vendor prefixes
    .pipe(pixrem()) // add fallbacks for rem units
    .pipe(gulp.dest(paths.css))
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(cssnano()) // Minifies the result
    .pipe(gulp.dest(paths.css));
});

// Javascript minification
gulp.task('scripts', function() {
  return gulp.src(paths.js + '/project.js')
    .pipe(plumber()) // Checks for errors
    .pipe(uglify()) // Minifies the js
    .pipe(rename({
      suffix: '.min'
    }))
    .pipe(gulp.dest(paths.js));
});

// Run django server
gulp.task('runServer', function() {
  exec('python manage.py runserver', function(err, stdout, stderr) {
    console.log(stdout);
    console.log(stderr);
  });
});

// Browser sync server for live reload
gulp.task('browserSync', function() {
  browserSync.init(
    [paths.css + '/*.css', paths.js + '*.js', paths.templates + '*.html'], {
      proxy: 'localhost:8000'
    });
});

// Default task
gulp.task('default', function() {
  runSequence(['styles'], 'runServer', 'browserSync');
});

////////////////////////////////
//          Watch             //
////////////////////////////////

// Watch
gulp.task('watch', ['default'], function() {
  gulp.watch(paths.sass + '/*.scss', ['styles']);
  gulp.watch(paths.js + '/*.js', ['scripts']).on('change', reload);
  gulp.watch(paths.images + '/*', ['imgCompression']);
  gulp.watch(paths.templates + '/*.html').on('change', reload);
  gulp.watch(paths.templates + '/**/*.html').on('change', reload);
});