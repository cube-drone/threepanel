var attr = DS.attr;

App.User = DS.Model.extend({
    username: attr('string'),
    accounts: DS.hasMany('account', {'async':true}),
    streams: DS.hasMany('stream', {'async':true}),
    articles: DS.hasMany('article', {'async':true}),
});

App.Account = DS.Model.extend({
    user: DS.belongsTo('user'), 
    streams: DS.hasMany('stream', {'async':true}),
    slug: attr('string'), 
    title: attr('string'),
    preferences: attr(),
});

App.Stream = DS.Model.extend({
    user: DS.belongsTo('user'),
    account: DS.belongsTo('account'),
    articles: DS.hasMany('article', {'async':true}),
    slug: attr('string'),
    title: attr('string'),
    description: attr('string'),
    preferences: attr(),
});

App.Article = DS.Model.extend({
    user: DS.belongsTo('user'),
    stream: DS.belongsTo('stream'),
    contents: DS.hasMany('content', {'async':true}),
    status: attr('string'),
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
