# Mail sender written in Python

### Building

```bash
make build
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

### Usage

This script expects CSV data to standard input (STDIN). CSV format is `email,placeholder1`. 
Then `$placeholder1` in the template will be substituted with `placeholder1` value from CSV.

```bash
echo "dddpaul@gmail.com,greeting" | \
docker run --rm -i --name mailblaster \
    -v ${PWD}/template.txt:/app/template.txt \
    dddpaul/mailblaster:latest \
	--verbose \
	--server 127.0.0.1:25 \
	--from "Pavel Derendyaev <dddpaul@gmail.com>" \
	--subject "Hi!" \
	--template /app/template.txt
```

### Configuration

Options are passed by command line:

```
Usage: mailblaster.py [options]

Options:
  -h, --help            show this help message and exit
  --server=SMTP_SERVER  SMTP server with port, colon delimited (required)
  --auth=SMTP_AUTH      SMTP auth user and password, colon delimited
  --from=MAIL_FROM      Sender address e.g. "John Smith <john@smith.com>"
                        (required)
  --subject=SUBJECT     Message subject (required)
  --template=TEMPLATE   Message template filename (required)
  --delimiter=DELIMITER
                        CSV delimeter, default is ","
  --ssl                 Turns on TLS/SSL mode, default is off
  -v, --verbose         Turns on verbose mode, default is off
```

Great articles used to write this code:
* [Sending Emails With Python](https://realpython.com/python-send-email/)
* [How to send simple UTF-8 email in Python 3.x](https://petermolnar.net/article/not-mime-email-python-3/)
