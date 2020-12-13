# Mail sender written in Python

## Instructions

### Building

```bash
make build
```

### Running

```bash
make run
```

### Testing

First you need to startup local SMTP server. There are plenty of those, I prefer to use [this one](https://github.com/dddpaul/docker-exim-sender). Use `test-prep` command to create docker network and run Exim container.

```bash
make test-prep
```

Then just run:

```bash
make test
```



### Configuration

Options are passed by command line:

```bash
make help
```
