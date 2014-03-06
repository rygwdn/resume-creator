Vagrant.configure("2") do |config|
  config.vm.define :latex do |latex|
    latex.vm.box = 'saucy'
    latex.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/saucy/current/saucy-server-cloudimg-amd64-vagrant-disk1.box"
    latex.vm.hostname = 'latex.vagrant.dev'
    pkg_cmd = "
      echo update
      apt-get update -qq
      apt-get -q -y install texlive texlive-xetex texlive-latex-extra pandoc wget zip unzip fontconfig
      apt-get -q -y install python-setuptools build-essential python-dev libxml2-dev libxslt-dev zlib1g-dev
      easy_install pip
      pip install -r /vagrant/requirements.txt

      # install fontin
      rm -f /tmp/fontin2_pc.zip
      wget http://www.exljbris.com/dl/fontin2_pc.zip -O /tmp/fontin2_pc.zip
      unzip /tmp/fontin2_pc.zip -d /usr/local/share/fonts '*.ttf'
      fc-cache -f
    "
    latex.vm.provision :shell, :inline => pkg_cmd

    if Vagrant.has_plugin?("vagrant-vbguest")
      config.vbguest.auto_update = true
    end

    latex.vm.provider "virtualbox" do |vb|
      vb.customize [
        'modifyvm', :id,
        '--memory', 1024,
        '--cpus', "1",
        '--ioapic', 'on',
        # '--cpuexecutioncap', '50'
      ]
    end

    if Vagrant.has_plugin?("vagrant-cachier")
      # Configure cached packages to be shared between instances of the same base box.
      # More info on http://fgrehm.viewdocs.io/vagrant-cachier/usage
      config.cache.scope = :box
    end
  end
end

# vim: ft=ruby sts=2 sw=2
