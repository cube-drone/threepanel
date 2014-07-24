
window.App = Ember.Application.create({
    LOG_TRANSITIONS: true
});

App.ApplicationAdapter = DS.DjangoTastypieAdapter.extend({
    serverDomain: "http://localhost:8000",
    namespace: "s/api/0.0.1"
});
App.ApplicationSerializer = DS.DjangoTastypieSerializer.extend({});
