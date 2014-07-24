
App.Router.reopen({
  rootURL: '/s/'
});

App.Router.map(function() {
    this.resource('accounts', {path: '/accounts'}, function(){
        // implicit "index"
        this.route('new', {path: '/new'}); 
    });
    this.resource('account', {path: '/account/:account_slug'}, function(){
        this.route('edit', {path: '/edit'});        
    })
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

});


//AccountIndex
App.AccountIndexRoute = Ember.Route.extend({
});

App.AccountIndexController = Ember.ObjectController.extend({
    needs: ['account'], 
});

//AccountEdit
App.AccountEditRoute = Ember.Route.extend({
});

App.AccountEditController = Ember.ObjectController.extend({
    needs: ['account']
});
