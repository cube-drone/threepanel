
// Alerts

var Threep = Threep || {}

Threep.load = function(application){
    application.XAlertsComponent = Threep.XAlertsComponent
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
