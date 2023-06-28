# gopher-wp-bridge

Python gopher server using [https://github.com/dotcomboom/Pituophis/](https://github.com/dotcomboom/Pituophis/) and Wordpress's API to expose your wordpress site to the phlogosphere.

## How

Pass your desired wordpress site's URL and port with environment variables like so:

`HOST=gopher.example.com URL='http://wordpress.example.com' PORT='7070' python server.py`

Connect like this:

`lynx gopher://localhost:7070`

## Why

Because I'm not just a luddite, I'm an incredibly lazy luddite.

## Project status

Experimental. Just shows posts and pages. Could do a lot more cleanup, maybe adding a menu within each page to extract all of the links or something.
