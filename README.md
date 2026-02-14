# Ballsdex-leaderboard-pack-v3
This is my first package for ballsdex v3, so its pretty small. Its pretty handy tho :3
## Installation
1. Put this into `config/extra.toml`
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
