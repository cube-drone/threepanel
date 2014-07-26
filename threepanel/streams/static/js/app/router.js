
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

