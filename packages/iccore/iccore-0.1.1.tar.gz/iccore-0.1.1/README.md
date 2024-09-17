# iccore

This project has a collection of common data structures and utilities used in other ICHEC tools.

# Install  #

It is available on PyPI:

``` sh
pip install iccore
```

# Features #

The idea of this project is to provide some common, tested utilities for use in other ICHEC projects.

This includes wrapping basic Python utilities that interact with system resources, for example:

* external processes
* the filesystem
* network 

with stubs that can be mocked for tests or executed in 'dry run' mode. By using the `filesystem`, `process` and `network` utils provided here instead of the low-level Python libraries directly you get these extra features and help to standarize our tooling.

A basic CLI is included, mostly for testing, but it may be useful for getting ideas on what features the package can be used to support.

## Filesystem ##

You can replace all occurences of a string with another recursively in files with:

``` shell
iccore filesystem replace_in_files --target $REPLACE_DIR --search $FILE_WITH_SEARCH_TERM --replace $FILE_WITH_REPLACE_TERM 
```

The `search` and `replace` terms are, perhaps unusually, read from files. This can be handy to avoid shell escape sequences - as might be used in `sed`.

## Networking ##

You can download a file with:

``` shell
iccore network download --url $RESOURCE_URL --download_dir $WHERE_TO_PUT_DOWNLOAD
```

## Version Control ##

You can get Gitlab Milestones given a project id and access token with:

``` shell
iccore gitlab --token $GITLAB_TOKEN milestone $PROJECT_ID
```

You can get the version number of the most recent project release with:

``` shell
iccore gitlab --token $GITLAB_TOKEN latest_release $PROJECT_ID
```

# License #

This project is licensed under the GPLv3+. See the incluced `LICENSE.txt` file for details.
