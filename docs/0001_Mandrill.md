
# 0001 Mandrill

Today I got an e-mail from Mandrill.

> Going forward, all Mandrill users will be required to have a paid monthly
  MailChimp account and verify ownership of all sending domains.

I've already verified ownership of my sending domains, for the same of making
sure that my e-mail actually gets to where it is going, but a paid MailChimp account?
Paid monthly MailChimp accounts are pretty expensive. I don't want to do that.

To go into more detail, a [letter from the CEO](http://blog.mailchimp.com/important-changes-to-mandrill/)
explaining the move, but I can broad-strokes it for you:

* Some people want Mandrill to be simple e-mail infrastructure. Some people want it to be
  a deluxe service (like MailChimp) that offers a tonne of value add.
* Providing infrastructure is hard and not very profitable.
* Providing a deluxe service for people who have lots of money and want a deluxe
  service is much easier, and much more profitable.
* [Amazon SES](https://aws.amazon.com/ses/) is creaming Mandrill at providing email
  infrastructure.

I mean, from a business standpoint, I can see where they're coming from.
[My own company](https://saucelabs.com/)
has made some very similar decisions recently. I'm not even mad - I was getting
high-quality _completely free_ e-mail infrastructure from Mandrill for years!
I'm one of the people who wanted to treat Mandrill like simple e-mail infrastructure.
So I'm probably going to be parting ways with Mandrill over this.

Which gives me two major options, as far as I can tell.

* Run my own mail server. This costs nothing, but involves a lot of configuration
  and pain. Part of the problem with this strategy is that the internet is
  a constant flood of spam, and so convincing the Big Email Providers like
  Google and Yahoo that my e-mails are not _also_ spam can be a hard problem
  that requires a lot of [very careful engineering](http://sesblog.amazon.com/).
* Try using a different cloud mail provider. Fortunately, MailChimp's CEO was kind
  enough to name-drop Amazon SES, the product that is eating Mandrill's lunch,
  so that's a pretty compelling option.

The problem with using Amazon services is that they're very good, and there's a lot
of them, and they're all reasonably priced on their own, but expensive in aggregate.
An EC2 instance _and_ a block of S3 storage _and_ a database _and_ e-mail services
_and_ caching _and_ messaging all cost a lot more than just running the whole thing
off of one virtual machine.
I'll have to be careful not to get too
far down the Amazon rabbit hole, lest I end up with an extremely well-engineered
system for running Threepanel that costs me hundreds of dollars a month to actually run.

On the other hand, EC2 instances are about on par with DigitalOcean droplets in
terms of expense, and
I've been eyeing up [S3](https://aws.amazon.com/s3/) for image hosting...
