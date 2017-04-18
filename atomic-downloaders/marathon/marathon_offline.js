
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

    var url = 'https://www.marathonbet.com/en/popular/Football/?menu=11';
    console.log('Loading page');
    driver.
        get('https://www.marathonbet.com/').
        then(function () {
            console.log('Set cookies...');
            return driver.executeScript("document.cookie = 'panbet.oddstype=Decimal; path=/'; document.cookie = 'panbet.sitestyle=MULTIMARKETS; path=/';");
        }).
        // Football
        then(function () {
            return driver.get('https://www.marathonbet.com/en/popular/Football/?menu=11');
        }).
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            var date = (new Date()).toISOString().substr(0, 10);
            fsExtra.outputFile('tmp/marathon_html/football_offline/' + date + '.html', html);
        }).
        // Tennis
        then(function () {
            return driver.get('https://www.marathonbet.com/en/popular/Tennis/?menu=2398');
        }).
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            var date = (new Date()).toISOString().substr(0, 10);
            fsExtra.outputFile('tmp/marathon_html/tennis_offline/' + date + '.html', html);
        }).
        // Basketball
        then(function () {
            return driver.get('https://www.marathonbet.com/en/popular/Basketball/?menu=6');
        }).
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            var date = (new Date()).toISOString().substr(0, 10);
            fsExtra.outputFile('tmp/marathon_html/basketball_offline/' + date + '.html', html);
        }).
        // Hockey
        then(function () {
            return driver.get('https://www.marathonbet.com/en/betting/Ice+Hockey/?menu=537');
        }).
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            var date = (new Date()).toISOString().substr(0, 10);
            fsExtra.outputFile('tmp/marathon_html/hockey_offline/' + date + '.html', html);
        }).
        // Volleyball
        then(function () {
            return driver.get('https://www.marathonbet.com/en/betting/Volleyball/?menu=22712');
        }).
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            var date = (new Date()).toISOString().substr(0, 10);
            fsExtra.outputFile('tmp/marathon_html/volleyball_offline/' + date + '.html', html);
        }).
        // Done!
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
