How to use
==========

After installation, you can use command line :command:`ebookhomebrew` ::


Show help
---------

Command option :command:`-h` shows helps. ::

    $ ebookhomebrew -h


ebookhomebrew command line interfaces provides subcommand. ::

     Choose subcommands. Usually choose "auto"

     {auto,api,makezip}
      auto      Make only digit file name, convert e-book file such as PDF
      api               Provides Rest API interfaces
      makezip           Make zip file for adding specify extension files.

Also provides Options auto. ::

      -h, --help            show this help message and exit
      -s SRC_DIR, --src_dir SRC_DIR
                            Source directory which put original image files.
      --dst_dir DST_DIR     Destination directory which put e-book file.
      -d N,N, --digit N,N   Serial number digits you remain file name
      -e EXT, --extension EXT
                            Destination directory which put e-book file.
      -f FILENAME, --filename FILENAME
                            Destination directory which put e-book file.
      -m, --manual          Duplicate file name, solving manually.
      -r, --remove          Remove original image file.
      -y, --assume_yes      no verify users.

Also provides Options api. ::

      -h, --help            show this help message and exit
      -p PORT, --port PORT  API Server Port


Auto command
------------

Rename image file to only digit and Create PDF file. ::

    $ ebookhomebrew auto -s ./tests -d 3,4 -e jpg -f test.pdf


API command
-----------

Run API Server. ::

    $ ebookhomebrew api -p 8080



