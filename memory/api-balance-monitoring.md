# API Balance Monitoring

## Cron Job
- **Job ID:** 81c9f55e-2c86-47ea-81e3-0e4635bc212b
- **Name:** API Balance Dashboard Reminder
- **Schedule:** Daily at 9:00 AM Eastern (0 9 * * *)
- **Channel:** #mac-mini1 (1471933082297831545)

## Thresholds
- Reminder: < 25% remaining
- Critical: < 5% remaining

## APIs to Check
- xAI (Grok): https://console.x.ai
- Zhipu AI (GLM): https://open.bigmodel.cn
- OpenAI: https://platform.openai.com/usage
- DeepSeek: https://platform.deepseek.com/usage

## Notes
- xAI and Zhipu don't expose balance endpoints via API
- Using dashboard reminders as workaround
- Add more providers as keys become available
