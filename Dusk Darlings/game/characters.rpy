################################################################################
## characters.rpy  -  dialogue Character() definitions for the whole cast
##
## Colors match each character's hair color in their menu art, so their name
## tag and their portrait feel like they belong to the same person.
##
## Use these in your script like:
##     riel "That's an inefficient way to word this sentence."
##     mary "No rush. We've got all afternoon."
##     blaire "Wait, WHAT?! Nobody told me that!"
##     skit "...Um. Hi."
################################################################################

define riel   = Character("Riel",   color="#e8759f")   # smart, stoic
define mary   = Character("Mary",   color="#8a6cff")   # laidback, calm, friendly
define blaire = Character("Blaire", color="#f2a03d")   # outgoing, tomboyish, quick to anger
define skit   = Character("Skit",   color="#2fbfa5")   # shy, kind, helpful

## Riel, Mary and Blaire are meant to be met for the first time somewhere in
## the ordinary flow of a school day - see core/day_loop.rpy's placeholder
## locations for where those first-meeting scenes belong. Skit is already an
## established friend by the time the game starts (intro.rpy), so there's no
## "first meeting" scene to write for them, and no reason to hide their name
## behind a "???" - the player already knows who they are.
