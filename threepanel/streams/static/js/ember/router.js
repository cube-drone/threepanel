
App.Router.map(function() {
    this.resource('app',{path: '/'});
});

App.ApplicationRoute = Ember.Route.extend({
    setupController: function(controller) {
        // hey that controller is ApplicationController
        controller.set('username', 'classam');
    }
});

App.ApplicationController = Ember.Controller.extend({
    username: 'classam',
});
