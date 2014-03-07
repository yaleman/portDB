App.define([{
        id: 'jquery',
        name: 'jQuery',
        path: App.jqueryPath('jquery-2.0.3.min.js')
    }, {
        id: 'easing',
        name: 'Easing',
        dependencies: 'jquery',
        path: App.jqueryPath('jquery.easing.js')
    }, {
        id: 'flot',
        name: 'Flot',
        dependencies: 'jquery',
        path: App.jqueryPath('flot/jquery.flot.js')
    }, {
        id: 'cascade',
        name: 'Cascade',
        dependencies: ['jquery', 'easing'],
        path: App.jqueryPath('cascade/core.js')
    }, {
        id: 'charts',
        name: 'Charts',
        dependencies: ['cascade', 'flot'],
        path: App.jqueryPath('cascade/chart.js')
    }, {
        id: 'chartcategories',
        name: 'Chart Categories',
        dependencies: 'charts',
        path: App.jqueryPath('flot/jquery.flot.categories.js')
    }, {
        id: 'parsley',
        name: 'Parsley',
        dependencies: 'jquery',
        path: App.jqueryPath('parsley/parsley.min.js')
    }]);