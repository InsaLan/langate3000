# Langate 3000 infrastructure

This repository is here to hold the langate infrastructure. It is composed of
the frontend, the backend, and the nginx server.

## Documentation

Technical documentation is available [here](docs/manuel/src/SUMMARY.md) (in french).

## Contributing

Please read carefully [the CONTRIBUTING.md file](CONTRIBUTING.md) before any
contribution.

## Netcontrol

The netcontrol component is an interface between the langate web pages and
the kernel network components of the gateway used during the events.

Having this component in between is important because we don't want the web server
to have privileged access to kernel components as it is needed for this script.

Both the langate web server and this components communicate using UNIX sockets.
The messages exchanged begin with the size of the payload (as a 4 bytes int) followed by
the payload itself. The payload is always a pickle-encoded python dict.

launch command `make install` for the first setup of the langate on your computer, that will copy netcontrol.service in systemd.

## Installing and running the langate in local

```sh
git clone git@github.com:InsaLan/langate-3000.git
cp .env.dist .env # edit your .env with your local settings then:
chmod 0600 .env
docker compose -f docker-compose-beta.yml up
```

Then to stop the containers:
```sh
docker compose -f docker-compose-beta.yml down
```

The website is available at the value of `WEBSITE_HOST` which should be
`gate.insalan.fr` or `gate.localhost` depending on where it's running.  It's API
backend is available at `api.WEBSITE_HOST`.

The "beta" environment is available at `beta.WEBSITE_HOST` and it's own API at `api.beta.WEBSITE_HOST`.
There is hotreload for the front (with vite), back (with django runserver), and nginx (thanks to a custom script)

## Running the prod environment

Put 0 in the .env file for the `DEV` variable
Run the following command :
```sh
docker compose -f docker-compose.yml up
```

To stop the prod environment :
```sh

docker compose -f docker-compose.yml down
```

The dev frontend is available at `WEBSITE_HOST` and it's API at `api.WEBSITE_HOST`.

## Cleanup

Docker can take a lot of disk space with all the images.
You have a few options to clean it up:

- `make clean-all` will remove all the containers and images
- `make clean-custom` will remove all the custom images (the ones we build and not the ones we pull from docker hub)