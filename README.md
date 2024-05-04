# insalan.fr infrastructure

This repository is here to hold the langate infrastructure. It is composed of
the frontend, the backend, and the nginx server.

# Contributing

Please read carefully[the CONTRIBUTING.md file](CONTRIBUTING.md) before any
contribution.

## Installing and running insalan.fr in local

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
