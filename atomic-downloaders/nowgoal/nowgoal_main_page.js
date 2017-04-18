
console.log('\n\n\n======================================');
console.log('Start downloader', new Date());
console.log('======================================\n');

const fs = require('fs');
const webdriver = require('selenium-webdriver');
const fsExtra = require('fs-extra');

var LOCAL_WD_URL = 'http://localhost:4444/wd/hub';
var page_html = '';

function run () {
    var driver = new webdriver.Builder()
        .forBrowser('phantomjs')
        .usingServer(LOCAL_WD_URL)
        .build();

    console.log('Loading page');
    driver.
        get('http://www.nowgoal.com/').
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            var date = (new Date()).toISOString().substr(0, 10);
            fsExtra.outputFile('tmp/nowgoal_main_page/' + date + '.html', html);
        }).
        then(function () {
            console.log('Done!');
        }).
        catch(function (error) {
            console.error('Error:', error);
        });
}

function terminateAll (code) {
    process.exit(code);
}

process.on('exit', (code) => {
    console.log('Handle onExit');
    terminateAll(code);
});

process.on('SIGTERM', function() {
    console.log('Got SIGTERM');
    terminateAll();
});

process.on('uncaughtException', (err) => {
    console.log('Uncaught exception:', err);
    terminateAll();
});

process.on('unhandledRejection', (reason, p) => {
    console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
    terminateAll();
});

run();
