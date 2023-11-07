# grafana-container


## Generate SSL certyificate into `certs/` directory

Run the following command to generate a 2048-bit RSA private key, which is used to decrypt traffic:

```
openssl genrsa -out certs/server.key 2048
```
Run the following command to generate a certificate, using the private key from the previous step.
```
openssl req -new -key certs/server.key -out certs/server.csr
```

Run the following command to self-sign the certificate with the private key, for a period of validity of 365 days:
```
openssl x509 -req -days 365 -in certs/server.csr -signkey certs/server.key -out certs/server.crt
```
