
exports.terminateAll = function terminateAll (code) {
    code = code || 0;
    console.log('Terminate application with code ' + code);
    process.exit(code);
};

exports.init = function init () {
    process.on('exit', (code) => {
        console.log('Handle onExit');
        exports.terminateAll(code);
    });

    process.on('SIGTERM', function() {
        console.log('Got SIGTERM');
        exports.terminateAll();
    });

    process.on('uncaughtException', (err) => {
        console.log('Uncaught exception:', err);
        exports.terminateAll();
    });

    process.on('unhandledRejection', (reason, p) => {
        console.log('Unhandled Rejection at: Promise', p, 'reason:', reason);
        exports.terminateAll();
    });
};
