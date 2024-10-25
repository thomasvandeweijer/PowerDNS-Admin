# PowerDNS-Admin
Based on the **dev** branch of [PowerDNS-Admin](https://github.com/PowerDNS-Admin/PowerDNS-Admin/) for added catalog zones support and session bug fixes. If you don't need these options please use the latest stable build from PowerDNS-Admin themselves, you can find that one here: https://hub.docker.com/r/powerdnsadmin/pda-legacy

## Why?
The last dev build from PowerDNS-Admin has a few bugs that needed to be fixed for the application to be stable enough to use. The development of the current implementation of PowerDNS-Admin seemed to have stopped ([project update](https://github.com/PowerDNS-Admin/PowerDNS-Admin/discussions/1708)) and there's no date as of yet for a version based on the new codebase.

## Bug? What bug?
The dev version introduces a new [/healthcheck page](https://github.com/PowerDNS-Admin/PowerDNS-Admin/commit/a0495dfc7dbba9b5eecd75127c2baa2d3a52e0f4) (which is used as healthcheck in the Docker container), this /healthcheck page was meant to create a session with a lifetime of 0 minutes, unfortunately it seems like it sets the global lifetime of sessions to 0 minutes for a short moment as the /healthcheck page is loaded. This bug can affect people browsing through the admin interface if they load a new page at the same time as the healthcheck is called. Since the healthcheck was called every 5 seconds with Docker, this would happen quite often.

The catalog zone implementation also contained a bug where accounts who aren't admin couldn't create zones anymore because the list of catalog zones refused to load for them.

#### Features:

- Provides forward and reverse zone management
- Provides zone templating features
- Provides user management with role based access control
- Provides zone specific access control
- Provides activity logging
- Authentication:
  - Local User Support
  - SAML Support
  - LDAP Support: OpenLDAP / Active Directory
  - OAuth Support: Google / GitHub / Azure / OpenID
- Two-factor authentication support (TOTP)
- PDNS Service Configuration & Statistics Monitoring
- DynDNS 2 protocol support
- Easy IPv6 PTR record editing
- Provides an API for zone and record management among other features
- Provides full IDN/Punycode support
- Provides catalog zones support

## Running PowerDNS-Admin

There are several ways to run PowerDNS-Admin. The quickest way is to use Docker.

### Docker

Here are two options to run PowerDNS-Admin using Docker.
To get started as quickly as possible, try option 1. If you want to make modifications to the configuration option 2 may
be cleaner.

#### Option 1: From Docker Hub

To run the application using the latest stable release on Docker Hub, run the following command:

```
$ docker run -d \
    -e SECRET_KEY='a-very-secret-key' \
    -v pda-data:/data \
    -p 9191:80 \
    thomasvandeweijer/powerdns-admin:latest
```

This creates a volume named `pda-data` to persist the default SQLite database with app configuration.

#### Option 2: Using docker-compose

1. Update the configuration   
   Edit the `docker-compose.yml` file to update the database connection string in `SQLALCHEMY_DATABASE_URI`.
   Other environment variables are mentioned in
   the [AppSettings.defaults](https://github.com/thomasvandeweijer/PowerDNS-Admin/blob/main/powerdnsadmin/lib/settings.py) dictionary.
   To use a Docker-style secrets convention, one may append `_FILE` to the environment variables with a path to a file
   containing the intended value of the variable (e.g. `SQLALCHEMY_DATABASE_URI_FILE=/run/secrets/db_uri`).   
   Make sure to set the environment variable `SECRET_KEY` to a long, random
   string (https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY)

2. Start docker container
   ```
   $ docker-compose up
   ```

You can then access PowerDNS-Admin by pointing your browser to http://localhost:9191.

## Screenshots

![dashboard](docs/screenshots/dashboard.png)
