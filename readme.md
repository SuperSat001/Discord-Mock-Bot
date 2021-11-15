# Physics Brawl Mock Bot

Author - Delta0001#1968 (550683461376278530)

[Invite the Bot](https://discord.com/api/oauth2/authorize?client_id=753144721915772940&permissions=8&scope=bot)

Code hosted on GitHub at [Discord Mock Bot](https://github.com/SuperSat001/Discord-Mock-Bot)

## Usage Instructions

0. **Important note**. Do not type anything other than the answer in the round channels. Use a different channel for discussion. Don't write answers in scientific notation and use SI units **wherever not mentioned**.

1. **Create channels**. The following channels need to be created:
	- Points Tally
	- Major
	- Hurry-Up Mech
	- Hurry-Up EM
	- Hurry-Up X
 
2. **Create roles**. This case-sensitive role should be given to the user hosting the mock (anyone can write answers, but only they can use commands)
	- mock

3. **Set Output channel**. This will be the channel where the bot records your points (Points Tally). The host should copy the `channel ID` and set it up by
	- `?out [channel ID]`

4. **Start Major Contest**. Host should write this command in the `Major` channel
	- `?major`

5. **Start Hurry-Up contests**. After 1h from start of Major contest, host should write the following commands in respective channels
	- Hurry-Up Mech `?hm`
	- Hurry-Up EM `?he`
	- Hurry-Up X `?hx`

6. **Add bonous points**. As I am too lazy to implement time, you have to calculate the bonous points for Hurry-Up rounds yourself. Then do:
	- `?add [Bonous Points]`

7. **End the rounds**. The rounds will automatically end when all problems are done. To end them before that, write `exit` in the channel of the round which you want to end.
Time limits for the rounds are:
	- Major : 3h
	- Hurry-Up : 1h
	- Bonus Time for Hurry-Up : 30 mins

8. **Skip a question**. You can skip a question by writing `skip` in the relevant channel.

## Help me with the development
Please help me by creating image folder for other years Physics Brawls like `images`, their solutions file like `ans.txt` and points file like `pts.txt` under `pb2019` folder. By doing this, not only can you mock other Physics Brawls, but you also help other users do the same.

Check [making mock.md](https://github.com/SuperSat001/Discord-Mock-Bot/blob/master/making%20mock.md) for further info.

## Bugs and Glitches
Report any bug or glitch you encounter while using to me on discord, `Delta0001#1968`.

## Credits
The bot is developed solely by me, and fair use of the code is allowed. Enjoy.

### Acknowledgements
Thanks to my friends on the [Physics Olympiad Discord Server](https://discord.gg/wyGAa49) for using this bot and for this emoji.


![Yaw](https://i.imgur.com/ww1snsg.png)
