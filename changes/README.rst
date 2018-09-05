changes
=======

``changes`` aims to be a CLI tool for finding and retrieving changelogs for any
package. That means:
- system packages (``apt``, ``zypper``, ``pacman``, ``brew``, ...)
- language packages (``pip``, ``gem``, ``cargo``, ...)
- ad-hoc scripts (``curl https://foo.bar > /bin/foobar``, ...)

Its also a convenient excuse for me to properly learn Rust / wrestle with the
borrow-checker.

This project is a Work In-Progress! Expect very little for now and avoid the
disappointment.

If you're looking to contribute -- that's fantastic, I'm always open to getting
some helping hands! Feel free to dive right in.

Usage
-----

The rough end goal is to have::

    $ changes [-sSOURCE] [--from FROM_VERSION] [--to TO_VERSION] NAME

where::

    OPTIONS:
        <NAME>                   Sets the name (of package / command) to search.
        -s, --source <SOURCE>    Provides a source language restriction/hint.
        -f, --from <FROM>        Outputs the Changelog beginning with this version.
        -t, --to <FROM>          Outputs the Changelog ending with this version.

Plan
----

My plan is to start by requiring source hints, which will let me build up a
library of package-source-parsers::

    $ changes -spy coveralls  # parses https://pypi.org/project/coveralls/
                              # finds https://github.com/coveralls-clients/coveralls-python/blob/master/CHANGELOG.md
    $ changes -sbrew ripgrep  # parses https://github.com/Homebrew/homebrew-core/blob/master/Formula/awscli.rb
                              # finds https://github.com/aws/aws-cli
                              # locates https://github.com/aws/aws-cli/blob/develop/CHANGELOG.rst

I'll also want to expand this to cover packages whose names do not match their
cli commands, eg. so utilities can be looked up directly::

    $ changes -sbrew rg  # determines rg -> ripgrep
                         # parses https://github.com/Homebrew/homebrew-core/blob/master/Formula/ripgrep.rb
                         # finds https://github.com/BurntSushi/ripgrep
                         # locates https://github.com/BurntSushi/ripgrep/blob/master/CHANGELOG.md

Once that has some coverage, I'll expand the "Changelog locator" chunk::

    $ changes -spy coverage  # parses https://pypi.org/project/coverage/
                             # finds https://bitbucket.org/ned/coveragepy
                             # links to https://github.com/nedbat/coveragepy
                             # locates https://github.com/nedbat/coveragepy/blob/master/CHANGES.rst
    $ changes -sgem mailchimp-api  # parses https://rubygems.org/gems/mailchimp-api
                                   # finds https://bitbucket.org/mailchimp/mailchimp-api-ruby/
                                   # locates https://bitbucket.org/mailchimp/mailchimp-api-ruby/compare/2.0.6..2.0.5

By now, it will probably be obvious that some projects will simply refuse to be
easy to work with, so I'll probably try to come up with a decently
straightforward way to drop-in overrides. Hopefully, I'll have been keeping the
various pieces separate enough to avoid letting this step turn into too much of
a headache.

At that point, I can work on changelog parsers -- I realize there are infinite
possible options here, but a bit of best-effort parsing of ``.md``, ``.rst``,
``NEWS``, GitHub releases, and commit logs should be a decent 80% -- especially
if I focus on various "standards" such as `conventional changelogs`_.

This will allow me to add version range flags with a reasonable chance of
working::

    $ changes -srust clap --from v2.31.2  # parses https://github.com/clap-rs/clap/blob/master/CHANGELOG.md

And, finally, a more general search function can get played with until I end up
with my rough end goal::

    $ changes hub --from 2.4.0 --to 2.5.1  # parses https://github.com/github/hub/releases

.. _conventional changelogs: https://github.com/conventional-changelog/conventional-changelog
