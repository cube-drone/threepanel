
// Alerts

var Threep = Threep || {}

Threep.load = function(application){
    application.XAlertsComponent = Threep.XAlertsComponent
    application.XTextFieldComponent = Threep.XTextFieldComponent
    application.XValidateFieldComponent = Threep.XValidateFieldComponent
}

Threep.XAlertsComponent = Ember.Component.extend({
    actions:{
        clear:function(){
            console.log('clearing');
            this.sendAction();
        }
    }
});

Threep.AlertsMixin = Ember.Mixin.create({
    init: function(){
        this._super();
        this.set("alerts", []);
    },
    error: function(error){
        this.set('alerts', []);
        this.get('alerts').pushObject({'type':'warning', 'message':error});
        console.error(error);
    }, 
    info: function(message){
        this.set('alerts', []);
        this.get('alerts').pushObject({'type':'info', 'message':message});
        console.info(message);
    }, 
    success: function(message){
        this.set('alerts', []);
        this.get('alerts').pushObject({'type':'success', 'message':message});
        console.info(message);
    }, 
    clear: function(){
        this.set('alerts', []);
        console.info('clearing alerts');
    }, 
    actions: {
        clearAlerts: function(){
            console.info('clearAlerts action handler');
            this.clear();
        }
    }
});

Threep.XTextFieldComponent = Ember.Component.extend({
    init: function(){
        this._super();
        this.set('elid', 'textfield-'+Math.floor((Math.random()*1000) +1))
    }
});

Threep.XValidateFieldComponent = Ember.Component.extend({
    init: function(){
        this._super();
        this.set('elid', 'validatedfield-'+Math.floor((Math.random()*1000) +1))
    },
    actions:{
        clear:function(){
            console.log('clearing');
            this.sendAction();
        }
    }
});

Threep.SlugMixin = Ember.Mixin.create({
    slugUpdate: function(){
        var slugged = this.get('slug').toLowerCase().replace(/[^a-z0-9- ]/g, "_").replace(/ /g, "-");
        this.set('slug', slugged);
    }.observes('slug'),
    slugChanged: function(){
        return (this.get('isDirty') && 'slug' in this.get('model').changedAttributes());
    }.property('slug'),
});
