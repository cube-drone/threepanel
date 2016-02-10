# -*- mode: ruby -*-
# vi: set ft=ruby :

# vagrant plugin install vagrant-digitalocean
# vagrant up --provider=digital_ocean
# vagrant up --provider=virtualbox

# All Vagrant configuration is done below. The "2" in Vagrant.configure
# configures the configuration version (we support older styles for
# backwards compatibility). Please don't change it unless you know what
# you're doing.
Vagrant.configure(2) do |config|
  config.vm.hostname = Time.now.to_i.to_s
  # The most common configuration options are documented and commented below.
  # For a complete reference, please see the online documentation at
  # https://docs.vagrantup.com.

  # Every Vagrant development environment requires a box. You can search for
  # boxes at https://atlas.hashicorp.com/search.
  config.vm.box = "ubuntu/vivid32"

  # Disable automatic box update checking. If you disable this, then
  # boxes will only be checked for updates when the user runs
  # `vagrant box outdated`. This is not recommended.
  # config.vm.box_check_update = false

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Django Dev
  config.vm.network "forwarded_port", guest: 8080, host: 18080
  # Redis
  config.vm.network "forwarded_port", guest: 6379, host: 16379
  # Nginx
  config.vm.network "forwarded_port", guest: 80, host: 10080
  # Postgres
  config.vm.network "forwarded_port", guest: 5432, host: 15432

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"
  config.vm.synced_folder ".", "/home/vagrant/vagrant_django"

  config.vm.provision "shell" do |s|
    s.inline = "/bin/su - vagrant -c 'chmod +x /home/vagrant/vagrant_django/configuration/provision.sh' && /bin/su - vagrant -c '/home/vagrant/vagrant_django/configuration/provision.sh'"
    s.keep_color = true
  end

  config.vm.provision "shell" do |s|
    s.inline = '/bin/su - vagrant -c '\
                    'python3 /home/vagrant/vagrant_django/configuration/install.py'
  end

  config.vm.provider :digital_ocean do |provider, override|
    config.ssh.username = 'vagrant'
    override.ssh.private_key_path = '~/.ssh/id_rsa'
    override.vm.box = 'digital_ocean'
    #override.vm.box_url = "https://github.com/smdahlen/vagrant-digitalocean/raw/master/box/digital_ocean.box"
    provider.token = ENV["DIGITALOCEAN_API_TOKEN"]
    provider.image = 'ubuntu-15-10-x64'
    provider.region = 'nyc2'
    provider.size = '512mb'
  end

end
