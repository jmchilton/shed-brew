Shed Brew
=============

Shed Brew is a small set of Homebrew/linuxbrew [external
commands](https://github.com/Homebrew/homebrew/wiki/External-Commands)
implemented on top [platform
brew](https://github.com/platform-brew/platform-brew) that eases
leveraging [Galaxy](http://galaxyproject.org/) [Tool
Shed](http://toolshed.g2.bx.psu.edu/) that have been translated to a
Homebrew tap (see [galaxyproject/homebrew-toolshed] for instance).

To install Shed Brew once you have installed Homebrew or linuxbrew -
simply execute `brew tap galaxyproject/tap` and then `brew install
shed-brew`.

     % brew tap galaxyproject/tap
     % brew tap platform-brew/tap
     % brew install shed-brew
     % brew shed-install devteam package_bowtie_0_12_7
     % . <(brew shed-env devteam package_bowtie_0_12_7)
     % which bowtie
     /home/john/.linuxbrew/Cellar/devteam_packagebowtie0127/1.0/bowtie

**Warning** This is all experimental and there are *many* known issues
with the Tool Shed to Homebrew conversion process that we are working
through. None of these CLIs should be considered stable yet.
