
const processStartTime = new Date();
console.log(`\n\n
============================================
Start downloader at ${processStartTime.toISOString()}
============================================
`);

const fs = require('fs');
const fsExtra = require('fs-extra');
const exitHandler = require('../../data_lib/exit-handler');
const phantomDownloader = require('../helpers/phantom-downloader');
const getDynamicPageHtml = phantomDownloader.getDynamicPageHtml;

exitHandler.init();
var LOCAL_WD_URL = 'http://localhost:4444/wd/hub';
var page_html = '';

async function saveScreenshotAs (driver, filename) {
    var screenshot = await driver.takeScreenshot();
    var base64Data = screenshot.replace(/^data:image\/png;base64,/, '')
    fs.writeFileSync(filename, base64Data, 'base64');
}

async function run () {
    var driver = phantomDownloader.buildChromeSimulationDriver(LOCAL_WD_URL);

    var date_str = (new Date()).toISOString().substr(0, 10);
    var url = 'http://www.betexplorer.com/soccer/argentina/primera-division-2015/quilmes-olimpo-bahia-blanca/S0NOtD3i/';

    var htmlWin = await getDynamicPageHtml(driver, url + '#1x2');
    fsExtra.outputFile('tmp/betexp_html/football_offline/' + date_str + '-win.html', htmlWin);
    console.log('length = ' + htmlWin.length);
//    await saveScreenshotAs(driver, 'win.png');

    var htmlUO = await getDynamicPageHtml(driver, url + '#ou');
    fsExtra.outputFile('tmp/betexp_html/football_offline/' + date_str + '-uo.html', htmlUO);
    console.log('length = ' + htmlUO.length);
//    await saveScreenshotAs(driver, 'uo.png');


    var htmlHC = await getDynamicPageHtml(driver, url + '#ah');
    fsExtra.outputFile('tmp/betexp_html/football_offline/' + date_str + '-hc.html', htmlHC);
    console.log('length = ' + htmlHC.length);
//    await saveScreenshotAs(driver, 'hc.png');

    console.log('Done!');
}

run();
