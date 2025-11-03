// Eel.js - Official Eel JavaScript bridge
// https://github.com/python-eel/Eel/blob/master/eel.js

(function() {
    var _eel = window.eel = {};
    var _callbacks = {};
    var _id = 0;

    function _gen_id() {
        return ++_id;
    }

    _eel.expose = function(func, name) {
        name = name || func.name;
        window[name] = func;
    };

    _eel._call = function(name, args, kwargs, cb) {
        var call_id = _gen_id();
        if (cb) _callbacks[call_id] = cb;
        window.external.invoke(JSON.stringify({
            name: name,
            args: args,
            kwargs: kwargs,
            call: call_id
        }));
    };

    _eel._handle_response = function(call_id, value) {
        if (_callbacks[call_id]) {
            _callbacks[call_id](value);
            delete _callbacks[call_id];
        }
    };

    // Proxy for exposed Python functions
    _eel._proxy = function(name) {
        return function() {
            var args = Array.prototype.slice.call(arguments);
            var cb = null;
            if (typeof args[args.length - 1] === 'function') {
                cb = args.pop();
            }
            _eel._call(name, args, {}, cb);
        };
    };

    // Add exposed Python functions to eel object
    _eel.expose_python = function(names) {
        names.forEach(function(name) {
            _eel[name] = _eel._proxy(name);
        });
    };

    // Listen for messages from Python
    window.addEventListener('message', function(e) {
        var msg = e.data;
        if (msg && msg.hasOwnProperty('call') && msg.hasOwnProperty('value')) {
            _eel._handle_response(msg.call, msg.value);
        }
    });
})();
