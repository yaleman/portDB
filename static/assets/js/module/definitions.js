App.define([{
        id: 'jquery',
        name: 'jQuery',
        path: App.jqueryPath('jquery-2.0.3.min.js')
    }, {
        id: 'cascade',
        name: 'Cascade',
        dependencies: ['jquery', 'easing'],
        path: App.jqueryPath('cascade/core.js')
    }, {
        id: 'parsley',
        name: 'Parsley',
        dependencies: 'jquery',
        path: App.jqueryPath('parsley/parsley.min.js')
    }, {
        id: 'analytics',
        name: 'Google Analytics',
        path: (document.location.protocol === 'https:' ? '//ssl' : 'http://www') + '.google-analytics.com/ga.js',
        callback: function() {
            _gaq.push(['_setAccount', App.trackingcode], ['_trackPageview']);
        }
    }]);