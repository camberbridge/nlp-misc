// このデモの参考: https://qiita.com/yoshizaki_kkgk/items/da9711c26e71522ad289

// http://kimizuka.hatenablog.com/entry/2016/11/09/095622
"use strict";

// Electron側の初期設定
const electron = require('electron');
const app = electron.app;
const BrowserWindow = electron.BrowserWindow;
let mainWindow;

// アプリを閉じた時にquit
app.on('window-all-closed', function() {
  app.quit();
});

// アプリ起動後の処理
app.on('ready', function() {
  var subpy = require('child_process').spawn('python',['./hello.py']);
  var rq = require('request-promise');
  var mainAddr = 'http://localhost:5000';

  var openWindow = function() {
    mainWindow = new BrowserWindow({width: 1400, height: 850 });
    mainWindow.loadURL(mainAddr);

    // 終了処理
    mainWindow.on('closed', function() {
      mainWindow = null;
      subpy.kill('SIGINT');
    });
  };

  var startUp = function() {
    rq(mainAddr)
      .then(function(htmlString) {
        console.log('server started');
        openWindow();
      })
      .catch(function(err) {
        startUp();
      });
  };

  startUp();
});