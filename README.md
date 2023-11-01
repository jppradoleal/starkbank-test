# Starkbank Backend Test

This project consists in two async tasks:

1. **Send invoices**: Which runs once the server starts, and then, every 3 hours after that. It's job is to send 8 to 12 invoices to Starkbank Payment Gateway.
2. **Send transfer**: Which runs in batches of 15, or every 1 hour. It's job is to create a transfer transaction to Starkbank Bank Account using Starkbank Payment Gateway.

It also has a Webhook endpoint that receives Starkbank events.

## Running the project - Development mode

You're going to need a Starkbank ECDSA Key Pair in PEM format. In root folder execute:

```bash
openssl ecparam -name secp256k1 -genkey -noout -out stark-priv-key.pem
openssl ec -in stark-priv-key.pem -pubout > stark-pub-key.pem
```

Then, go to Integrations in your Starkbank Dashboard, and create a new project passing your `stark-pub-key.pem`.

Then create a `.env` file based on `.env.example` file. It's value are all prepared to run in our `docker-compose.yaml` specs.

```bash
cp .env.example .env
```

Lastly but not least, run the following command:

```bash
docker-compose up -d && docker-compose logs localtunnel
```

Copy the address and go back to your Starkbank Dashboard. Now, in the Integrations panel, create a webhook with the previous address with `/webhook/` prefix. Example:
`https://dull-trams-matter.loca.lt/webhook/`, for signatures, select `invoice`.

**Congratulations, your system is up and running.**

Execute the following command to see the invoices being generated and processed

```bash
docker-compose logs -f app celery_worker
```

## Running the project - Production Mode

I've left a Helm Chart in the [infrastructure folder](infrastructure/charts/starkbank/) that will set up your cluster with 3 Back-end pods, 3 Celery Workers pods, and 1 Celery Beat pod (It's enough, I swear). In the same folder, there is a terraform configuration to spin up a SQS Queue. Pass your Domain, your SQS URL, and the private key file content to the Chart values, and you're up and running!

```bash
# In the infrastructure/charts folder
helm install -f path/to/your/values.yaml unique-identifier ./starkbank
```

```yaml
# Sample values.yaml file
environment:
  secret_key: "YOUR_DJANGO_SECRET_KEY"
  broker_url: "sqs://{AWS_ACCESS_KEY_ID}:{SECRET_ACCESS_KEY}@"
  starkbank_private_key: |-
    -----BEGIN EC PRIVATE KEY-----
    {YOUR_PRIVATE KEY HASH}
    -----END EC PRIVATE KEY-----
  host: "{YOUR_DOMAIN}"
```
