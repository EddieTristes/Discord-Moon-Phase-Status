# Discord Moon Phase Status

Detects the moon phase and current illumination, and sets it as your Discord status using selfbot along with an accompanying phase emoji. 🌝

Here is an example of the status:

> 🌕 Tonight's phase is a Full Moon! The moon's illumination is 100%

You will need:

- A Discord User Token. You can fetch yours using [this guide.](https://github.com/Tyrrrz/DiscordChatExporter/blob/master/.docs/Token-and-IDs.md)
  
- A way to run Python 24/7. Keeping your computer online constantly is a hassle, and using things like linux servers or raspberry pies aren't practical for a selfbot this small. I use [Python Anywhere](https://www.pythonanywhere.com) to run this code safely. Let it be known, services like [Replit](https://replit.com/) are public unless you pay them, so if you opt for replit, you need to set up a secret to keep your token safe.
  
- Patience. The moon's full cycle takes roughly 29.53 days and is called a synodic month!

## Warning

**Abusing Discord's API can lead to your account being banned.** Use this code responsibly and at your own risk. It is recommended to run the code in moderation to avoid triggering Discord's rate limits. That being said, this bot only changes your status hourly once it successfully finds the on-the-dot hour. `(ex. 8:00, 9:00, etc.)`

## Note

**Always practice mindful internet habits.** This code utilizes your Discord token to change your status. Regardless of your trust in me, or lack therof, I highly encourage you to review the code thoroughly to ensure it aligns with your expectations and does not pose any security risks to yourself.
