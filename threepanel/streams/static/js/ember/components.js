
// Alerts

// To decorate a template with alerts, add
//     {{x-alerts alerts=alerts}}  
// then, call 
//     decorateWithAlerts(<TemplateController>)
// (where TemplateController is the controller for the template with x-alerts)
// TemplateController now has access to 
//     this.error(message)
//     this.info(message)
//     this.success(message)
//     this.clear()

App.XAlertsComponent = Ember.Component.extend({
    actions:{
        clear:function(){
            console.log('clearing');
            this.sendAction();
        }
    }
});

var AlertsMixin = Ember.Mixin.create({
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
