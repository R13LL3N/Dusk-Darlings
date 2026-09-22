################################################################################
## intro.rpy  -  Day 1 opening: ordinary morning routine + walk to school.
##
## No club, no group introduction. Skit is the protagonist's neighbor and
## childhood friend, encountered here because that's an ordinary part of the
## morning - not because the plot needs to introduce a cast in one scene.
## Riel, Mary and Blaire are NOT in this file. Per the design rule in
## Anti_DDLC.txt, they should be encountered separately, on separate days,
## through separate ordinary situations (class, the library, lunch, the gym,
## walking home, weekend events...) - see core/day_loop.rpy, where the actual
## school day (School/Lunch/Afternoon/Evening/Night) plays out and where
## those encounters belong once they're written.
##
## The story opening that plays after "New Game" (menu lives in main_menu.rpy).
## Placeholder art and audio are in game/images and game/audio - overwrite them
## with your own files (same filenames) and nothing else needs to change.
################################################################################

################################################################################
## Characters
## Riel, Mary, Blaire and Skit are defined once for the whole game in
## characters.rpy. This file only defines the people specific to this scene.
################################################################################

default player = "Alex"

define mc  = Character("[player]", color="#ffffff")
define mom = Character("Mom", color="#d9c7a3")

################################################################################
## Images
## Backgrounds and sprites are auto-loaded from game/images/ by filename:
##   "bg street.png"      ->  scene bg street
##   "skit happy.png"     ->  show skit happy
## Just overwrite the placeholder PNGs with your own art (keep the filenames).
################################################################################

image bg black = Solid("#000000")

################################################################################
## Game start
################################################################################

label start:

    stop music fadeout 1.5
    play sound "audio/sfx_start.ogg"

    ## ---- Name entry ------------------------------------------------------
    scene bg black
    with dissolve

    python:
        entered = renpy.input("Please enter your name.", length=12)
        entered = entered.strip()
        if entered:
            player = entered

    ## ---- Opening: bedroom -------------------------------------------------
    ## "play music" loops the whole file automatically until you stop it
    play music "audio/ambient_loop.ogg" fadein 1.5
    scene bg bedroom
    with fade

    "The alarm goes off three times before I actually get up."

    mom "[player]! You're going to be late again!"

    mc "I'm up, I'm up!"

    "I throw on my uniform and grab my bag."
    "Another school year. Nothing about this morning feels any different from the last one."

    ## ---- Walk to school ---------------------------------------------------
    scene bg street
    with fade

    "The walk to school takes about fifteen minutes if I don't stop for anything."
    "I've done it enough times that I could probably do it with my eyes closed."

    show skit neutral at center
    with dissolve

    "Skit is waiting by the corner where our street meets the main road, same as most mornings."
    "She's lived two houses down since we were kids. At some point our walks to school just... merged, and neither of us ever said anything about it."

    skit "...Morning."

    mc "Morning."

    "She falls into step beside me without really looking up."

    show skit worried
    skit "You forgot your umbrella again, didn't you."

    mc "It's not even cloudy."

    show skit neutral
    skit "That's what you said last week too."

    "She digs a folding umbrella out of her bag and holds it out to me."

    skit "Here. You can give it back whenever."

    mc "You don't have to keep doing this."

    show skit happy
    skit "I know."

    "I take it anyway. It's easier than arguing, and she's usually right about the weather."

    "We don't talk much for the rest of the walk. It's a comfortable kind of quiet - the sort you only get with someone you've known long enough to run out of things you need to say."

    ## ---- Arrival at school -------------------------------------------------
    scene bg school
    with dissolve
    show skit neutral at center

    "The school gate is its usual mess of noise by the time we get there - underclassmen comparing homework, upperclassmen pretending not to be tired."

    show skit worried
    skit "I have the early shift in the library today. I should go."

    mc "The library, huh. You basically live there."

    show skit happy
    skit "Someone has to."

    "She gives a small wave and heads off toward the building before I can say anything else."

    "I check the time. Homeroom starts in ten minutes."

    "Just an ordinary morning, then. Nothing about it feels like it's going to be any different from the last one."

    ## Hand off to the core day loop (core/day_loop.rpy). Day 1's morning and
    ## walk to school are already covered above, so gameplay proper picks up
    ## right where the school day itself begins.
    jump day_loop_start
