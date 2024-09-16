# Archon Discord Bot

[![PyPI version](https://badge.fury.io/py/archon-bot.svg)](https://badge.fury.io/py/archon-bot)
[![Validation](https://github.com/lionel-panhaleux/archon-bot/workflows/Validation/badge.svg)](https://github.com/lionel-panhaleux/archon-bot/actions)
[![Python version](https://img.shields.io/badge/python-3.8-blue)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-blue)](https://opensource.org/licenses/MIT)
[![Code Style](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)

Discord bot for V:TES tournament management.
[Add it to your server](https://discordapp.com/oauth2/authorize?client_id=862326826193518622&scope=bot%20applications.commands&permissions=401730896)

The bot requires quite a few permissions to create roles and channels properly.
Please do not tinker with the list of required permissions and grant them all
if you want the bot to run properly on your server.

## Cheatsheet

**At any step, use `/announce` in the main channel to display helpful guidance messages for the players and judges both.**

The announce message changes and depends on the step of the tournament you're at
(registration, playing, in-between rounds, ...).

Players:

- Register: `/register [vekn] [name]`
- Upload deck list: `/upload-deck [url] [file]`
- Check in: `/check-in `
- Report your result: `/report [vp]`
- Drop out: `/drop`
- Check your status: `/status`

Judges:

A number of commands target a specific player. In those cases, you can always use either
the player's ID in the tournament (VEKN) _or_ the Discord user. The Discord user might
be more practical for online tournaments, where using the VEKN might be easier in some
cases, and indispensible for offline tournaments.

For players who do not have a _real_ VEKN, the bot delivers a temporary number
prefixed with "P" instead, like `P195730`, to serve as vekn for the tournament.
You can use this identifier (prefix included) as the VEKN number in all commands

- Opening the tournament:
    * Open a new tournament: `/open-tournament`
    * Set a maximum number of rounds (league): `/set-max-round [rounds_count]`
    * Define a limited format: `/define-format [vdb_format] [ban_list] [single_clan] [single_vampire]`
    * Announcement (help and guidance messages for both players and judges): `/announce`
    * Appoint judges and bots: `/appoint [role] [user]`
    * Configure the tournament: `/configure-tournament`
    * Make a staggerred tournament: `/stagger [rounds_count]`
    * Come back from staggered to standard: `/un-stagger`
    * Open check-in (confirm players presence): `/open-check-in`
- Player management:
    * Register a player (offline or missing VEKN): `/register-player [vekn] [name] [user]`
    * Upload a registration list (CSV): `/batch-register [file]`
    * Upload a player's deck list: `/upload-deck-for [vekn] [user] [file] [url]`
    * Add a note, caution or warning to a player: `/note [level] [note] [user] [vekn]`
    * Get a player's info, including notes and warnings: `/player-info [user] [vekn] `
    * Drop a player: `/drop-player [user] [vekn]`
    * Disqualify a player: `/disqualify [user] [vekn] [note]`
    * Full players list: `/players-list [public]`
- Rounds management:
    * Start a new round: `/round start`
    * Check round results: `/results [round] [public]`
    * Fix a player's VP count: `/fix-report [vp] [user] [vekn] [round]`
    * End a round: `/round finish [keep_checkin]`
    * Current standings (only finished rounds count): `/standings`
    * Begin finals: `/finals`
    * Reset the newly created round: `/round reset`
    * Add a player to a 4 players table (if play has not begun): `/round add [table]`
    * Remove a player from a 5 players table (if play has not begun): `/round remove [user] [vekn]`
    * Validate an odd score situation (eg. because of a Judge ruling): `/validate-score`
- Misc:
    * Make a raffle amoung players `/raffle [count]`
- Ending the tournament:
    * Download the reports: `/download-reports`
    * Close the tournament (make sure you downloaded the reports first): `/close-tournament`

Admins:
- Reset channels and roles with `/reset-channels-and-roles`.
  This can fix things if you have messed up (eg. deleted a tournament role or channel).

## Quickstart: Simple Usage

The archon bot can be used in a variety of tournament settings.
The archon bot can only run **one tournament per category** in a Discord server.

Simply choose a category (ie. a folder) in your discord server
(or ask an admin to open one for you), and use the `/open-tournament` command.

**The channel in which you use the `/open-tournament` command becomes the main tournament channel.**

The bot will then proceed to guide you in creating your tournament and using its commands.

If you're unsure what to do, **at any stage use the `/announce` command in the main tournament channel**.
It will display help and guidance messages in the main and judges channel.

## Command Permissions

As soon as you open your first tournament with the Archon bot, it will create a long standing role called
`Archon Judge` on your server. This role will be assigned to all judges for all tournaments.
You can use it to set the commands permissions so as to limit clutter for normal players.

Go to `Server Settings > Integrations > Archon`

![Integrations](images/integrations.png)

And change the permissions for all judge commands to make them available exclusively to the `Archon Judge` role

![Permissions](images/permissions.png)

## Detailed guide

The cheatsheet and quickstart are enough to use the bot:
just use `/announce` whenever you want to know what to do next, and the bot will guide you.
However, if you want to know more or encounter a tricky case, the rest of this documentation can, hopefully, help.

### Running a tournament

Just open a tournament:

```
/open-tournament name: My Tournament
```

The bot will then guide you in configuring your tournament

As organiser, you automatically get the Judge role and access to the `#Judges` channels.
You can appoint some additional judges to help you:

```
/appoint role: Judge user: @your_friendly_judge
```

Do not forget to **appoint the bots** you want to make available
to the players in the table channels (timer bot, krcg):

```
/appoint role: Bot user: @timer
```

You can also optionally add some spectators, they will have acces to all tables.
It is useful if you like to give streamers access to the vocal channels:

```
/appoint role: Spectator user: @some_guest
```

#### Tournament options

##### Number of rounds

You can indicate the maximum number of rounds a player can play with `/set-max-round`.
It is only relevant if you are planning some kind of league or championship where there are more time slots for rounds
than the maximum number of rounds you expect each player to play.
For example, if you are planning 1 "rounds slots" every Saturday for six weeks (6 possible dates),
but only want each of your players to play 3 rounds. In that case use the rounds limit

```
/set-max-round rounds: 3
```

This will prevent players to be able to play more than this number of rounds,
even if you're running more "rounds slots".

In most tournaments, this parameter is useless because you expect players to play all the rounds you are running
if they can.

##### Limited format

You can define a limited format with the `/define-limited` command. You can provide a list of banned cards,
or activate some common Storyline rules list "single clan" (75% of the crypt being the same clan) or "single vampire".
You can also use a [VDB format file](https://vdb.im/documentation) to define the format, and that file will be made
available to the players in the `/announce` message, to make it easy for them to build their decks with VDB.

```
/define-format vdb_format: my_storyline.txt single_clan: True
```

You can use the same command with no parameter to revert back to the Standard VEKN format:

```
/define-format
```

##### VEKN ID requirement

In official tournaments, a VEKN ID is required. The bot will check the existence of the VEKN ID against the
VEKN registry, although it cannot verify the player is actually the right person
(we trust the players to provide the _right_ id). Different players cannot have the same VEKN ID so if a player makes
a mistake (wrong VEKN), the can simply use `/register` again with the right one. If someone else has their VEKN,
they need to ask a judge to use `/drop-player` and `/register-player` to remedy the issue.

**You need to use this requirement for sanctionned tournaments.**

If VEKN ID are required, the bot will issue archon-compatible reports files
at the end of the tournament, facilitating reporting.

##### Decklist requirement

If decklists are required, players wil need to submit them before checking in.
The players can use `upload-deck` and the judges `upload-deck-for`. They work the same,
except the judges have to select a player to upload the deck to. You can either provide
a `url` or a `file`. If you provide none, the bot displays a model for you to write
(or copy/paste) your deck in.
The decklist is saved upon submission: subsequent changes in VDB or Amaranth will
need for the player to submit their decklist again to be recorded.
Judges will have access to the decklists, but only after the first round has started.

##### Check-in (once or on each round)

If you're running a live event or an event spanning a single day, a single
check-in is enough. Otherwise and especially online, opt for a check-in each round
to make sure the players are actually connected and ready to play before each round.
If you have two rounds back to back, you will have the option to keep the
checkin information after the first when you use `/round finish`.

##### Multideck

Normally a single deck is allowed, with this option, players can submit a new decklist
each round.

##### Late joiners

Normally players are not allowed to register anymore once the first round has started,
although a Judge can always bypass this with `/register-player`. But if you are running
a league, you might want players to be able to register freely in between rounds.
In that case, that's the option you want.

##### Staggered tournament (6, 7 & 11 players)

A V:TES seating can accomodate any number of players,
except if you have 6, 7 or 11 players. In this situation, the `/round start`
command will yield an error because it cannot get a table for everyone.
You should either have some players drop out or additional players check in.

In case you want to run a tournament with 6, 7, or 11 players, you can setup a staggered
tournament. In this case, you need to use `/stagger` and indicate the number
of rounds each player will play, so that the bot can compute a full staggered-rounds
seating structure for you.

#### Registration

The tournament registrations are open as soon as you created the tournament.
Players can use the `/register` command to register themselves.
Depending on the tournament configuration, they might need to provide their VEKN ID
or their deck list. The bot will guide them in providing the required information.

Use the `/announce` command to provide guidance to everyone for the registration:

```
/announce
```

Players can then register easily with the `/register` command:

```
/register vekn: 1000123 decklist: https://vdb.im/decks/12e26be1ade44d3a938c0a5984a70230
```

- `vekn`: If the player has none and the tournament requires it, only a Judge can register them (see below)
- `name`: The name the player would like to use for the tournament.
  Optional if the VEKN is provided, since the name will then be fetched from the VEKN registry.

If a VEKN ID is required and a player does not have one,
or if a player is struggling with the commands, any Judge (including you) can register
a player in their stead:

```
/register-player [vekn] [name] [decklist] [user]
```

- `vekn:` If the player has one. In that case, you do not need to fill in the name,
  it will be fetched from the VEKN registry.
- `name:` If the player has no VEKN or you're not using them. In that case, no need to fill the VEKN
- `user:` The Discord user (optional, but without it they will not be able to check in themselves)

If decklists are required, players can submit them directly:
```
/upload-deck url: https://vdb.im/decks/12e26be1ade44d3a938c0a5984a70230
```

The decklist is _copied and saved_ by the bot when the command is issued.
If the decklist is modified by the player in VDB or Amaranth, it will not be taken into account by the bot.
They need to issue the command _again_ with a decklist URL (even if it's the same)
to update the deck list in the bot registry.
For a standard (non-league) tournament, the bot will prevent a player to modify their decklist
once the first round has started.

Judges can also upload a decklist on behalf of a player:

```
/upload-deck-for vekn: 1000123 url: https://vdb.im/decks/12e26be1ade44d3a938c0a5984a70230
```

You can display the list of registered players at any time

```
/players-list
```

Any **subsequent use of registration commands** on the same user/id will _update_ that player's registration with
the additional information, overwriting the existing registration with the new information you provide.
It will keep any information that was already there (vekn, name, deck list)
if you do not provide a newer information for this field.

Note that registering players in advance before the tournament is an option for convenience, it's not a requirement.
Once the tournament begins, you should issue the `/open-check-in` command to let the bot know, you will still be able to
proceed with registrations until you decide it's time for the first round (see below).

#### Tournament day

When the tournament is about to begin, open the check-in:

```
/open-check-in
```

Use the `/announce` command to provide guidance to everyone for the check-in:

```
/announce
```

Registered players can now check-in to the tournament by issuing simply:

```
/check-in
```

Note that only works if they have already registered in advance and the registration is linked to their Discord account.
If not, they need to use the `/register` command as explained previously

```
/register vekn: 1000123
```

Since the check-in is open, this will also check them in directly
(they do not need to issue a `/check-in` command after registration).

You and other Judges can also register _and_ check-in players yourselves
using the `/register-player` command as explained above:

```
/register-player [vekn] [name] [decklist] [user]
```

You can display the list of checked-in players at any time

```
/players-list
```

And display a reminder on how the check-in works for your players regularily:

```
/announce
```

Once everyone has checked in, you can start the first round

#### Round management

```
/round start
```

This command is the heart of the archon bot, it does multiple thing:

-   Check if the previous round is finished and all results reported and consistent
-   Randomise and optimise the seating according to the
    [official guidelines [LSJ 20020323]](https://groups.google.com/g/rec.games.trading-cards.jyhad/c/4YivYLDVYQc/m/CCH-ZBU5UiUJ)
-   Display and pin the seating in the channel you issued the command
-   Create text and voice channels for each table
-   Display the seating in each table channel
-   Assign roles to the players so they get access to their respective table
-   The archon bot and theappointed bots and judges have access to all channels
-   Spectators have access to all channels but cannot read or write in them

At any point during the tournament, you can take notes on players
(to share issues or remarks with other Judges will easily) and deliver cautions, warnings and disqualifications:

```
/note @target_player level: Caution note: Spurious draw of cards (on a do not replace card)
```

Once the round is finished, players should report their result (VPs):

```
/report 3
```

Players report only _their_ victory points, not those of their opponents.
The bot computes game wins automatically.
You and other judges can check the round results:

```
/results
```

If some results are not correct, any judge can fix them:

```
/fix-report @mistaken_player 2
```

Once everything is OK, you can close the round, no more VP report will be accepted.
This step is optional: you can also proceed to the next round directly.

```
/round finish
```

A judge can display the standings at any time:

```
/standings
```

You can _decide_ to share the standings publicly between rounds,
although it is a decision you should debate with the Head Judge:

```
/standings public: True
```

Some judges feel displaying the standings between rounds can incite the players in
taking them into account during their game (eg. purposefuly hindering a leading player),
which is a violation of Tournament Rules. Others feel it's exciting and levels the playfield
(reduces the impact of scouting).

#### Finals and closing the tournament

When all rounds have been played and reported, you can launch the finals:

```
/finals
```

The bot will do a "toss" to choose between runner-ups if necessary: it is random.
Channels are created and the seeding order will be displayed.
On a finals table, last seed chooses their seat first.
Once the finals is finished, have the players report their results as usual
or do it yourself with the `/fix-report` command (see above).
Once the report is done, you can download the tournament reports:

```
/download-reports
```

Tt will provide you a full tournament report as a CSV file, as well as archon-compatible
CSV files if your were running a standard tournament with mandaotry VEKN IDs.

You can then close the tournament:

```
/close-tournament
```

**Note the channels and roles created by the bot will be deleted**,
including the `#Judges` channels. Make sure you have downloaded the reports first.

### Corner cases

There are a few corner cases you might hit when handling a tournament.

#### Late check-in

Some players might want to check in after the first round has already begun.
They can always just check in for the next round, provided you kept the check-in open.
Alternatively, if the other players haven't started to play yet,
you can add the late comer to a 4 players table after they've registered:

```
/register-player vekn: 1000234 user: @late_player
/round add table: 3 user: @late_player
```

#### Player dropping out

Players can easily drop out of the tournament between rounds:

```
/drop
```

They can check in again later to participate in future rounds.
The archon bot will take their absence into account when optimising the seating.
Judges can also forcibly drop a player if they've just disappeared without warning:

```
/drop-player user: @late_player
```

- `vekn` or `user`: you can refer to the player by its Discord handle or tournament ID.

But beware that this does not count as a disqualification: the player can come back
and check in again in a later round. If you want to disqualify a player, use:

```
/disqualify user: @late_player note: Aggressive conduct
```

#### Reset a round

If players are missing or new players are arriving late, it might be better to
cancel the round you just started and start a new one:

```
/round reset
[... fix registrations, drop absentees, etc.]
/round start
```

Note you can also use `/round reset` to reset the finals if you have a missing finalist.
In that case though, the toss is _not_ rerolled.

#### Cautions, warnings, disqualification

Judges can issue cautions, warnings and disqualify players:

```
/note user: @problematic_player level:caution note: drew an additional card
/note user: @problematic_player level:warning note: additional cards again
/note user: @problematic_player level:warning note: misrepresented the rules
```

- `vekn` or `user`: you can refer to the player by it's Discord handle or tournament ID.

If any caution or warning has been previously issued, the bot will display
the previous issues and ask you if you want to upgrade the level of your penalty
or disqualify the player (in case of a second warning).

#### Fix a round result

You cannot close a round and start a new one if the score is incorrect,
but this does not mean mistakes cannot happen. To fix a mistake in a round,
a judge can use the `/fix-result` command to modify reported results.
It can be used for previous rounds too:

```
/fix-result user: @player_1 vp: 1
/fix-result user: @player_2 round: 1 vp: 2
```

- `vekn` or `user`: you can refer to the player by it's Discord handle or tournament ID.
- `round`: current round by default, but you can fix a previous round by giving its number.

#### Validate odd VP situations

In some situations, a judge might decide to change the available VP total on a table.
For example if a player drops out of a round at the very beginning, he might decide
to award only 0.5 VP to its predator, or no VP at all. In that case, the archon bot
will see the total result as invalid because the total does not match.
A judge can force an odd VP result to be accepted:

```
/validate-score table: 4 note: Disqualified John but awared only 0.5 VP to his predator, Alice
```

- `table`: The table for which the odd score is to be validated
- `note`: Explain why this odd scoring happened
- `round`: current round by default, but you can fix a previous round by giving its number.

### Offline tournament

Although the archon bot is primarily intended for online play, you can
use it to run an offline tournament too.

You can take pre-registrations as usual:

```
/register-player vekn: 1000123
```

Or upload a file of all registered players:

```
/batch-register my-players.csv
```

And on tournament day, open the check-in:

```
/open-check-in
```

**Once you have opened the check-in, any registration also checks the player in**

You can then register the player as they come as usual:

```
/register-player vekn: 1000123
```

Just register them by name if they don't have a VEKN yet,
but make sure to note down their email and domain (country, city) for VEKN registration:

```
/register-player name: Alice Allister
```

The bot will issue a temporary ID (with a `P` prefix) that you can use
as the VEKN ID for further commands (eg. `P305729`).

You can optionally **let your players check in in Discord** if they like,
they can link their Discord account to a registered VEKN using the `/register` command:

```
/register vekn: 1000123
```

This way, they can see their table and seating automatically and directly.
Moreover, they will be able to report their result for each round with the `/report` command:

```
/report 2
```

With or without your players logged in on Discord, you can run your rounds normally:

```
/round start
```

Any judge can register the results using the `/fix-result` command over VEKN IDs:

```
/fix-result vekn: 1000123 2
```

If a player checks in between rounds, you can register them and check them in:

```
/register-player vekn: 1000234
```

And if a player drops in between rounds, just drop them:

```
/drop-player vekn: 1000234
```

## Contribute

This is an Open Source software under MIT license. Contributions are welcome,
feel free to [open an issue](https://github.com/lionel-panhaleux/archon-bot/issues)
if you encounter a bug or have a feature request, and we will try to accomodate.
If you are up for it, pull requests are welcome and will be merged if they pass the tests.
