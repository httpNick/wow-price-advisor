# WoW Price Advisor

Clone the repo and use the following commands to get it working.

```bash
source ~/.zshrc
python -m venv venv
source venv/bin/activate
pip install -e .
wowpriceadvise
```

Note:
A `.env` file MUST be created at the root of the project if you want to supply a TSM (TradeSkillMaster) API key. Otherwise only the supplied item_data.csv file will be used.
See more here about TSM API keys and how to get one: https://support.tradeskillmaster.com/en_US/api-documentation/tsm-public-web-api

Example `.env` file:

```
TSM_API_KEY=abc-123-def-456-ghjkl
```

An OpenAI access key is also required to be loaded AI client to instantiate.
See more here: https://platform.openai.com/docs/quickstart