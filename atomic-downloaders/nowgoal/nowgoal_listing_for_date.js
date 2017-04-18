
console.log('\n\n\n======================================');
console.log('Start downloader', new Date());
console.log('======================================\n');

const fs = require('fs');
const webdriver = require('selenium-webdriver');
const commander = require('commander');
const fsExtra = require('fs-extra');

commander
  .option('-d, --date [date]', 'date of list page', parseArgvDate)
  .option('-r, --rewrite', 'rewrite output file if it exists')
  .parse(process.argv);

if (!commander.date) {
    throw new Error('date is not specified');
}

var outputFileName = 'tmp/nowgoal_listing_for_date/' + commander.date + '.html';
var isFileExists = fs.existsSync(outputFileName);
if (isFileExists && !commander.rewrite) {
    process.exit(0);  // the file is already exists and rewrite is not forced
}

var LOCAL_WD_URL = 'http://localhost:4444/wd/hub';
var page_html = '';

function run () {
    var driver = new webdriver.Builder()
        .forBrowser('phantomjs')
        .usingServer(LOCAL_WD_URL)
        .build();

    console.log('Loading page');
    driver.
        get('http://www.nowgoal.com/schedule.htm?f=ft&date=' + commander.date).
        then(function () {
            return driver.executeScript("return document.body.innerHTML;");
        }).
        then(function (html) {
            console.log('html.length', html.length);
            fsExtra.outputFile(outputFileName, html);
        }).
        then(function () {
            console.log('Done!');
        }).
        catch(function (error) {
            console.error('Error:', error);
        });
}

function parseArgvDate (date) {
    if (date === 'yesterday') {
        yesterday = new Date(Date.now() - 24 * 3600 * 1000);
        date = yesterday.toISOString().substr(0, 10);
    }

    var shift = parseInt(date, 10);
    var validator = /^(\d\d\d\d\-\d\d-\d\d)$/i;
    if (validator.test(date)) {
        console.log('date = %s', date);
        return date;
    }
    else if (!isNaN(shift) && shift >= 0) {
        theDay = new Date(Date.now() - shift * 24 * 3600 * 1000);
        date = theDay.toISOString().substr(0, 10);
        console.log('date = %s', date);
        return date;
    }
    else {
        throw new Error('date is invalid');
    }
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
