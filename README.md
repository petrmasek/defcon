# Defcon warning system notifier

It notifies about defcon level.

## How it works

It runs in infinite loop.

1. It downloads current defcon level from https://defconwarningsystem.com/code.dat
2. It compares the current defcon level with stored defcon level
3. If the stored level is not the same as the downloaded one it stores the current one and it notifies to a Telegram group

## How to run it

You can run it without parameters as command line tool or you can run it with parameter start as daemon:

**python defcon.py**

### Daemon parameters

- start - it starts and runs defcon notifier as daemon
- stop - it stops defcon notifier
- restart - it restarts defcon notifier

## Configuration

Configuration is in **config/defcon.config**

- defcon_check_period - how often it should check the current defcon level - in minutes
- telegram_bot_id - ID of your Telegram bot (you need to create one at first)
- telegram_trading_group_id - ID of Telegram group which will be receiving notification
- debug - for testing purposes

#### Debug mode

It logs debug messages and it sends notifications to:
- screen - if it runs withou parameter
- file - if it runs as daemon