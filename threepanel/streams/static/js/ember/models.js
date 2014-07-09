var attr = DS.attr;

App.User = DS.Model.extend({
    username: attr('string'),
    accounts: DS.hasMany('account'),
    streams: DS.hasMany('stream'),
    articles: DS.hasMany('article'),
    contents: DS.hasMany('content'),
});

App.Account = DS.Model.extend({
    user: DS.belongsTo('user'), 
    streams: DS.hasMany('stream'),
    slug: attr('string'), 
    title: attr('string'),
    preferences: attr(),
});

App.Stream = DS.Model.extend({
    user: DS.belongsTo('user'),
    account: DS.belongsTo('account'),
    articles: DS.hasMany('article'),
    slug: attr('string'),
    title: attr('string'),
    description: attr('string'),
    preferences: attr(),
});

App.Article = DS.Model.extend({
    user: DS.belongsTo('user'),
    stream: DS.belongsTo('stream'),
    contents: DS.hasMany('content'),
    status: attr(),
    datetime: attr('date'),
    slug: attr('string'),
    title: attr('string'),
    preferences: attr(),
});

App.Content = DS.Model.extend({
    user: DS.belongsTo('user'),
    article: DS.belongsTo('article'),
    order: attr('number'),
    content_type: attr('string'),
    content: attr(),
    preferences: attr(),
});
