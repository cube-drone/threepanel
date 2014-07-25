
App.Router.reopen({
  rootURL: '/s/'
});

App.Router.map(function() {
    this.resource('accounts', {path: '/accounts'}, function(){
        // implicit "index"
        this.route('new', {path: '/new'}); 
    });
    this.resource('account', {path: '/account/:account_slug'})
});

App.ApplicationRoute = Ember.Route.extend({
    setupController: function(controller) {
        controller.set('username', USERNAME);
        controller.set('accounts', this.store.find('account'))
    },
    redirect: function(){
        //var accounts = controller.get('accounts');
        //if(accounts.length > 0){
        //    this.transitionTo('/a/'+accounts[0].slug)
        //}
    }
});

App.ApplicationController = Ember.Controller.extend({
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


App.AccountsRoute = Ember.Route.extend({

});

App.AccountsIndexRoute = Ember.Route.extend({
    model: function(params){
        return this.store.find('account')
    }
});

// Account
App.AccountRoute = Ember.Route.extend({
    model: function(params){
        return this.store.find('account', params.account_slug)
    }
});

App.AccountController = Ember.ObjectController.extend({
    actions:{
        saveAccount: function(){
            this.get('model').save();
        },
        rollbackAccount: function(){
            this.get('model').rollback();
        },
    }
});
