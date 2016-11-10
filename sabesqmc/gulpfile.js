'use strict';

// Fix for gulp-autoprefixer requiring Promise
// https://github.com/postcss/postcss-nested/issues/30
require('es6-promise').polyfill();

var gulp = require('gulp'),
  pjson = require('./package.json'),
  mainBowerFiles = require("main-bower-files"),
  inject = require('gulp-inject'),
  sass = require('gulp-sass'),
  customizeBootstrap = require('gulp-customize-bootstrap'),
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
// gulp.task('styles', function() {
//   return gulp.src('./bower_components/bootstrap/scss/bootstrap.scss')
//     .pipe(customizeBootstrap(paths.sass + '/*.scss'))
//     .pipe(sass().on('error', sass.logError))
//     .pipe(plumber()) // Checks for errors
//     .pipe(autoprefixer({
//       browsers: ['last 2 version']
//     })) // Adds vendor prefixes
//     .pipe(pixrem()) // add fallbacks for rem units
//     .pipe(gulp.dest(paths.css));
//     // .pipe(rename({
//     //   suffix: '.min'
//     // }))
//     // .pipe(cssnano()) // Minifies the result
//     // .pipe(gulp.dest(paths.css));
// });

gulp.task('styles', function () {
  return gulp.src(paths.sass + '/*.scss')
    .pipe(sass({
      includePaths:['./static/bower_components/bootstrap/scss/']
    }).on('error', sass.logError))
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

gulp.task('html', function(){
  return gulp.src(paths.templates + '/*.html')
    .pipe(inject(gulp.src(
      mainBowerFiles(), {read: false}),{name: 'bower'}))
    .pipe(inject(gulp.src(paths.css + '/*.css', {read: false})))
    .pipe(gulp.dest(paths.templates));
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
    [paths.css + '/*.css', paths.js + '/*.js', paths.templates + '/*.html'], {
      proxy: 'localhost:8000'
    });
});

// Default task
gulp.task('default', function() {
  runSequence(['html', 'styles'], 'runServer', 'browserSync');
});

////////////////////////////////
//          Watch             //
////////////////////////////////

// Watch
gulp.task('watch', ['default'], function() {
  gulp.watch(paths.sass + '/*.scss', ['styles']);
  gulp.watch(paths.js + '/*.js', ['scripts']).on('change', reload);
  gulp.watch(paths.images + '/*', ['imgCompression']);
  gulp.watch(paths.templates + '/*.html', ['html']).on('change', reload);
});
