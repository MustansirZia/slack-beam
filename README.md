# SlackBeam

SlackBeam is a slack bot that helps teams generate social media content for X (formerly Twitter) directly from Slack. The bot uses AI-powered text generation to create post suggestions and provides an interactive interface for managing and publishing content.

[![Publish Docker image](https://github.com/MustansirZia/slack-beam/actions/workflows/publish.yml/badge.svg?branch=main)](https://github.com/MustansirZia/slack-beam/actions/workflows/publish.yml)
![Docker Image Version](https://img.shields.io/docker/v/mustansirzia/slack-beam)
![Docker Image Size](https://img.shields.io/docker/image-size/mustansirzia/slack-beam)

## Start
1. Install **[Docker](https://www.docker.com)**.
2. Run the following script:
```bash
# Download the prompt file.
wget https://github.com/MustansirZia/slack-beam/raw/refs/heads/main/x_prompts.json 2>/dev/null

# Make changes to the prompt file.
# vi x_prompts.json

# Start the app.
sudo docker run \
     -p 80:8000 \
     -e 'SLACK_BOT_TOKEN=<SLACK_BOT_TOKEN>' \
     -e 'SLACK_SIGNING_SECRET=<SLACK_SIGNING_SECRET>' \
     -e 'ANTHROPIC_API_KEY=<ANTHROPIC_API_KEY>' \
     -e 'X_CONSUMER_KEY=<X_CONSUMER_KEY>' \
     -e 'X_CONSUMER_SECRET=<X_CONSUMER_SECRET>' \
     -e 'X_ACCESS_TOKEN=<X_ACCESS_TOKEN>' \
     -e 'X_ACCESS_TOKEN_SECRET=<X_ACCESS_TOKEN_SECRET>' \
     -d \
     --restart unless-stopped \
     -v $(pwd)/x_prompts.json:/app/x_prompts.json \
     mustansirzia/slack-beam:latest
```

## Technical Stack
- [Python 3.12](https://www.python.org) - Runtime.
- [Claude Sonnet 3.5](https://www.anthropic.com/news/claude-3-5-sonnet) - Gen AI Model. 
- [Langchain](https://python.langchain.com) - LLM Tooling.
- [SQLite](https://www.sqlite.org) - Persistent Storage for Suggestions and Conversations.
- [SQLAlchemy](https://www.sqlalchemy.org) - ORM for Storage.
- [Flask](https://flask.palletsprojects.com) - HTTP Framework.
- [Gunicorn](https://gunicorn.org) - WSGI HTTP Server. 
- [Bolt](https://api.slack.com/bolt) - Slack Integration Framework.

## Features

- Generate suggestions for X via a Slack command.
- Multiple post type templates available that are driven by configurable prompts.
- Batch generation of post suggestions.
- Post a suggestion you like to X directly via Slack.

## Environment Variables

1. **Slack Credentials**
   - `SLACK_BOT_TOKEN`: OAuth token for your Slack bot
   - `SLACK_SIGNING_SECRET`: Verification secret for Slack API
   
   To obtain these:
   1. Go to [Slack API Dashboard](https://api.slack.com/apps)
   2. Create a new app or select existing app
   3. Under "OAuth & Permissions", install app to workspace and copy the "Bot User OAuth Token"
   4. Find the "Signing Secret" under "Basic Information"

2. **Anthropic API Access**
   - `ANTHROPIC_API_KEY`: Authentication key for Claude API
   - `ANTHROPIC_MODEL_NAME`: Anthropic model name. _If not provided defaults to_ `claude-3-5-sonnet-20241022`.

   To obtain API key:
   1. Visit [Anthropic Console](https://console.anthropic.com/)
   2. Create an account or sign in
   3. Navigate to API Keys section
   4. Generate a new API key

3. **X (Twitter) API Credentials**
   - `X_CONSUMER_KEY`: API Key for X application
   - `X_CONSUMER_SECRET`: API Secret for X application
   - `X_ACCESS_TOKEN`: OAuth 1.0a access token
   - `X_ACCESS_TOKEN_SECRET`: OAuth 1.0a access token secret
   
   To obtain these:
   1. Go to [X Developer Portal](https://developer.twitter.com/en/portal/dashboard)
   2. Create a developer account if you haven't already
   3. Create a new project and app (select "OAuth 1.0a" type)
   4. Under "Keys and Tokens":
      - Find "API Key and Secret" for consumer credentials
      - Generate "Access Token and Secret" under User authentication tokens
   5. Ensure your app has "Read and Write" permissions

## License
MIT.