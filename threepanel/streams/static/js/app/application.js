
window.App = Ember.Application.create({
    LOG_TRANSITIONS: true
});

// Load Threep Components
Threep.load(App);

App.ApplicationAdapter = DS.DjangoTastypieAdapter.extend({
    serverDomain: "http://localhost:8000",
    namespace: "s/api/0.0.1"
});
App.ApplicationSerializer = DS.DjangoTastypieSerializer.extend({});

App.ApplicationRoute = Ember.Route.extend({
    setupController: function(controller) {
        controller.set('username', USERNAME);
    },
});

App.ApplicationController = Ember.Controller.extend({
    init: function(controller){
        var that = this;
        this.currentlySelectedAccountPromise = new Promise(function(resolve, reject){
            var csa = that.get('currentlySelectedAccount');
            if(csa == undefined){
                that.store.find('account').then(function(accounts){
                    that.set('accounts', accounts);
                    if( accounts.get('length') > 0 ){
                        that.set('currentlySelectedAccount', accounts.objectAt(0));
                        resolve(accounts.objectAt(0));
                    }
                    else{
                        that.set('currentlySelectedAccount', "new");
                        resolve("new")
                    }
                }, function(rejectReason){
                    reject(rejectReason);   
                });
            }
            else
            {
                resolve(csa);
            }
        });
    },
});

App.ApplicationView = Ember.View.extend({
    templateName: "application",
    didInsertElement: function(){
        this.$().foundation('topbar');
        this.$().foundation('clearing');
    },
    willDestroyElement: function(){
        this.$().foundation('topbar', 'off');
        this.$().foundation('clearing', 'off');
    }
});

App.IndexRoute = Ember.Route.extend({
    redirect: function(){
        var appController = this.controllerFor('application')
        var that = this;
        appController.currentlySelectedAccountPromise.then(function(account){
            if(account == undefined){
                console.error("IndexRoute: this shouldn't happen.");
            }
            if(account != 'new'){
                that.transitionTo('/account/'+account.id);
            }
            else{
                that.transitionTo('/accounts/new');
            }
        });
    }
});
