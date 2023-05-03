## A simple GitHub oauth lambda function

To deploy it, use [sam](https://aws.amazon.com/serverless/sam/):

```
sam build
sam deploy --guided
```

This will ask for your github secret to put then in the environment variables of
the lambda function.

It comes with two secrets:

* GITHUB_CLIENT_SECRET_DEV - for the dev stage - use it in your local development
* GITHUB_CLIENT_SECRET_PROD - for the production stage - use it in your production

If you want to use it for your own needs, you might want to change the client ids in the [app.py](app.py) file as well:

```
GITHUB_CLIENT_ID_DEV = "your_dev_client_id" 
GITHUB_CLIENT_ID_PROD = "your_prod_client_id"
```

Once deployed, you can use it to get a token for your app:

``` js
fetch('https://your_api_id.execute-api.us-east-1.amazonaws.com/Prod/github-oauth/?client=' + clientId + '&code=' + code)
  .then(response => response.json())
  .then(data => console.log(data));
```
