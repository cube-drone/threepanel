
App.Router.reopen({
  rootURL: '/s/'
});

App.Router.map(function() {
    this.resource('accounts', {path: '/accounts'}, function(){
        // implicit "index"
        this.route('new', {path: '/new'}); 
    });
    this.resource('account', {path: '/account/:account_id'})
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
        return this.store.find('account', params.account_id);
    }, 
    setupController: function(controller, account){
        controller.set('model', account);
        controller.set('alerts', []);
    },
    actions:{
        willTransition: function(transition){
            console.info("transitioning out of account, rolling back changes.");
            this.controller.get('model').rollback();
        }
    }
});

App.AccountController = Ember.ObjectController.extend(AlertsMixin, {
    actions:{
        saveAccount: function(){
            var that = this;
            var success = function(){
                that.success("Account saved!");
            };
            var failure = function(){
                that.error("This account couldn't be saved!");

            };
            this.get('model').save().then(success).catch(failure);
        },
        rollbackAccount: function(){
            this.get('model').rollback();
        }
    }
});
