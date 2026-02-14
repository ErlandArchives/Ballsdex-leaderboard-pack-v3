# Ballsdex-leaderboard-pack-v3


1. Put this into extra.toml
   ```toml
   [[ballsdex.packages]]
   location = "git+https://github.com/ErlandArchives/Ballsdex-leaderboard-pack-v3.git"
   path = "leaderboard"
   enabled = true
   editable = false
   ```
2. Rebuild the bot.
   do:
   ```
docker compose build
docker compose up
   ```
