# Langate 3000 infrastructure

This repository is here to hold the langate infrastructure. It is composed of
the frontend, the backend, netcontrol, and the nginx server.

## Documentation

Technical documentation is available [here](docs/manuel/src/SUMMARY.md) (in french).

## Contributing

Please read carefully [the CONTRIBUTING.md file](CONTRIBUTING.md) before any
contribution.

## Installing and running the langate locally

- Installation:
```sh
git clone git@github.com:InsaLan/langate-3000.git
cp .env.dist .env
# edit your .env with your local settings, then:
chmod 0600 .env
```
- To start the containers:
```sh
docker compose -f docker-compose-beta.yml up --build
```
You can also pass the `-d` argument to "detach" the container from the terminal, or run it in the background.

- Then to stop the containers:
```sh
docker compose -f docker-compose-beta.yml down
```

The website is available at the value of `WEBSITE_HOST` which should be `gate.insalan.fr` or `gate.localhost` depending on where it's running. Its API backend is available at `api.WEBSITE_HOST`.

The "beta" environment is available at `beta.WEBSITE_HOST` and it's own API at `api.beta.WEBSITE_HOST`.

There is hotreload for the front (with vite), back (with django runserver), and nginx (thanks to a custom script)

## Running the prod environment

- Put 0 in the .env file for the `DEV` variable.

- Build the images:
```sh
docker compose -f docker-compose build
```
- Run the following command :
```sh
docker compose -f docker-compose.yml up
```
- To stop the prod environment :
```sh
docker compose -f docker-compose.yml down
```

The dev frontend is available at `WEBSITE_HOST` and its API at `api.WEBSITE_HOST`.

## Cleanup

Docker can take a lot of disk space with all the images.
You have a few options to clean it up:

- To remove all the containers and images:
  
	`docker compose -f docker-compose.yml down --rmi all && docker compose -f docker-compose-beta.yml down --rmi all`
- To remove all the custom images (the ones we build and not the ones we pull from docker hub):
	`docker compose -f docker-compose.yml down --rmi local && docker compose -f docker-compose-beta.yml down --rmi local`