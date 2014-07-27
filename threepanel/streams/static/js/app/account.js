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

App.AccountController = Ember.ObjectController.extend(Threep.AlertsMixin, Threep.SlugMixin, {
    slugValid: function(){
        return !Bloom.account_exists(this.get('slug'));
    }.property('slug'),
    viewUrl: function(){
        return SETTINGS.SITE_ROOT + "r/" + this.get('slug');
    }.property('slug'),
    canEdit:function(){
        return ((this.get('isDirty') && !this.slugChanged) || 
                (this.slugChanged && this.slugValid))
    }.property('slug', 'title'),
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
