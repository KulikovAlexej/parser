
const webdriver = require('selenium-webdriver');


function buildSimplePhantomDriver (wdUrl) {
    var driver = new webdriver.Builder()
        .forBrowser('phantomjs')
        .usingServer(wdUrl)
        .build();
    return driver;
}
exports.buildSimplePhantomDriver = buildSimplePhantomDriver;


function buildChromeSimulationDriver (wdUrl) {
    var driver = new webdriver.Builder()
        .withCapabilities({
            browserName: 'phantomjs',
            'phantomjs.page.settings.userAgent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
        })
        .usingServer(wdUrl)
        .build();
    driver.manage().window().setSize(1366, 728);
    return driver;
}
exports.buildChromeSimulationDriver = buildChromeSimulationDriver;


async function getDynamicPageHtml (webDriver, url) {
    console.log('Loading page ' + url);
    await webDriver.get(url);
    await webDriver.executeScript('location.href = "' + url + '";');
    await new Promise(function (resolve, reject) {
        setTimeout(resolve, 1000);
    });
    console.log(await webDriver.executeScript('return location.href;'));
    return await webDriver.executeScript("return document.body.innerHTML;");
}
exports.getDynamicPageHtml = getDynamicPageHtml;
