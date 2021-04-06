# HTTP Analysis with Raspberry PI

Even today there are still a lot of websites that only use HTTP. That is very good, because you can analyze this traffic with the simplest possible means.

## Objective

The aim is to analyze the HTTP traffic from connected STA's.

## Install needed and/or optional packages

Install (_or ensure they are installed_) following packages.

```shell
# update system (optional)
$ sudo apt update -y && sudo apt upgrade -y

# install needed packages
$ sudo apt install -y tcpdump httpry
```

## tcpdump

As in a previous tutorial, you can use `tcpdump` to analyze the current HTTP traffic.

```shell
# show HTTP User Agent and Hosts
$ tcpdump -i wlan1 -nn -l -A -s1500 | egrep -i 'User-Agent:|Host:'
...
Host: example.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15
...

# show HTTP requests and Hosts
$ sudo tcpdump -i wlan1 -nn -l -s 0 -v | egrep -i "POST /|GET /|Host:"
...
GET / HTTP/1.1
Host: example.com
GET /gts1o1core/MFcwVaADAgEAME4wTDBKMAkGBSsOAwIaBQAEFEJGMMInGdvecPCP%2FHPlpl9mOBe8BBSY0fhuEOvPm%2BxgnxiQG6DrfQn9KwIRANrCtsUde0x1AwAAAADLz9k%3D HTTP/1.1
Host: ocsp.pki.goog
GET / HTTP/1.1
Host: r3.i.lencr.org
GET /MFgwVqADAgEAME8wTTBLMAkGBSsOAwIaBQAEFEjayaD7K9MtT%2FDeaNL1Z7c1%2BbPEBBQULrMXt1hWy65QCUDmH6%2BdixTCxgISBKX89wJrmK3LIUVLVeFRKYPH HTTP/1.1
Host: r3.o.lencr.org
```

## httpry

It works even easier and clearer with `httpry`.

```shell
# start httpry on interface wlan1
$ sudo httpry -i wlan1
...
----------------------------
Hash buckets:       64
Nodes inserted:     10
Buckets in use:     9
Hash collisions:    1
Longest hash chain: 2
----------------------------
Starting capture on wlan1 interface
2021-04-03 10:30:05	192.168.0.183	93.184.216.34	>	GET	example.com	/	HTTP/1.1	-	-
2021-04-03 10:30:05	93.184.216.34	192.168.0.183	<	-	-	-	HTTP/1.1	304	Not Modified
2021-04-03 10:31:35	192.168.0.183	172.217.168.67	>	GET	ocsp.pki.goog	/gts1o1core/MFcwVaADAgEAME4wTDBKMAkGBSsOAwIaBQAEFEJGMMInGdvecPCP%2FHPlpl9mOBe8BBSY0fhuEOvPm%2BxgnxiQG6DrfQn9KwIRANWlliAM60mFBQAAAACHo2Y%3D	HTTP/1.1	-	-
2021-04-03 10:31:35	172.217.168.67	192.168.0.183	<	-	-	-	HTTP/1.1	200	OK
2021-04-03 10:31:39	192.168.0.183	13.224.89.198	>	GET	neverssl.com	/	HTTP/1.1	-	-
2021-04-03 10:31:39	192.168.0.183	172.217.168.67	>	GET	ocsp.pki.goog	/gts1o1core/MFYwVKADAgEAME0wSzBJMAkGBSsOAwIaBQAEFEJGMMInGdvecPCP%2FHPlpl9mOBe8BBSY0fhuEOvPm%2BxgnxiQG6DrfQn9KwIQG%2FLvCsEmgsUDAAAAAMvPVg%3D%3D	HTTP/1.1	-	-
2021-04-03 10:31:39	13.224.89.198	192.168.0.183	<	-	-	-	HTTP/1.1	200	OK
2021-04-03 10:31:39	172.217.168.67	192.168.0.183	<	-	-	-	HTTP/1.1	200	OK
...
```

_Note: read this [manual page](https://linux.die.net/man/1/httpry) for more information's._

[Go Back](../readme.md)
