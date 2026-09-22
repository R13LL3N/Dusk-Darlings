################################################################################
## intro.rpy  -  DDLC-style opening for Ren'Py
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
default agreed_to_visit = False
default club_name = "Literature Club"   # change to whatever your club is called

define mc  = Character("[player]", color="#ffffff")
define mom = Character("Mom", color="#d9c7a3")
define unk = Character("???", color="#c9a0ff")   # unknown speaker

################################################################################
## Images
## Backgrounds and sprites are auto-loaded from game/images/ by filename:
##   "bg street.png"      ->  scene bg street
##   "skit happy.png"     ->  show skit happy
## Just overwrite the placeholder PNGs with your own art (keep the filenames).
################################################################################

image bg black = Solid("#000000")

## White flash for the "something is off" moments
define flash = Fade(0.1, 0.0, 0.5, color="#ffffff")

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

    "..."
    "The sound of my alarm drags me out of a dream I can't quite remember."
    "Something about a long hallway. And a door at the end of it."
    "I shake my head. Whatever it was, it's already gone."

    mom "[player]! You're going to be late again!"

    mc "I'm up, I'm up!"

    "I throw on my uniform and grab my bag."
    "Another school year. Another chance to finally do something with my life."
    "That's what I keep telling myself, anyway."

    ## ---- Walk to school ---------------------------------------------------
    scene bg street
    with fade

    "The morning air is cool and quiet. The kind of quiet that makes your own footsteps feel too loud."
    "I've walked this road so many times that my feet do it without me."
    "Which gives my brain plenty of time to wander."

    "I've never really belonged to anything. No clubs, no teams."
    "I go to school, I go home, I play games until my eyes hurt."
    "It isn't a bad life. It just feels... unfinished."

    skit "{b}[player]!!{/b}"

    "I don't even have to turn around to know who it is."

    show skit happy at center
    with dissolve

    skit "Hey! I've been calling you for like a whole block!"

    mc "Sorry. I was zoned out."

    show skit teasing
    skit "You're always zoned out. It's kind of your thing."

    mc "Good morning to you too."

    show skit happy
    skit "Good morning!"

    "This is my childhood friend. We've lived a few houses apart for as long as I can remember."
    "She has this way of walking into a bad mood and making it leave."
    "I've never told her that."

    show skit neutral
    skit "Hey, wait. You're not going to run off after school again, are you?"

    mc "I wasn't planning on it."

    skit "Good. Because I have a favor to ask."

    mc "Uh oh."

    show skit teasing
    skit "It's a {i}good{/i} favor! Probably!"

    ## ---- The invitation ---------------------------------------------------
    scene bg school
    with dissolve
    show skit neutral at center

    "We reach the school gates just as the bell starts to ring."
    "The courtyard is already packed with students, and every wall is covered in club posters."

    skit "So, the festival is coming up, right?"

    mc "Yeah. I saw the banners."

    skit "I joined the [club_name] over the summer, and we're really short on members."
    skit "If we can't get enough people, they'll shut us down before it even starts."

    mc "And you want me to join."

    show skit worried
    skit "...Kind of, yeah."

    "She looks away for a second. It's a very small thing."
    "But it's the first time in years I've seen her look unsure."

    menu:
        "What do I do?"

        "Sure. I'll at least check it out.":
            $ agreed_to_visit = True

            show skit happy
            skit "Really?! You mean it?"

            mc "I said I'd {i}check it out{/i}. I'm not promising anything."

            skit "That's basically a yes in [player] language!"

            mc "It absolutely isn't."

        "I'm not really a club person...":
            $ agreed_to_visit = False

            show skit worried
            skit "Oh. Yeah. I figured you'd say that."

            "She tries to smile. It doesn't quite reach her eyes."

            show skit teasing
            skit "But you're coming anyway."

            mc "That wasn't a question, was it?"

            skit "Nope!"

            "Of course it wasn't."

    ## ---- A small wrong note ----------------------------------------------
    "She grabs my sleeve and starts pulling me toward the building."

    skit "Come on, everyone's really nice. You'll love it."
    skit "I promise you'll never want to leave."

    "For a moment, the noise of the courtyard cuts out completely."

    scene bg black with flash
    with Pause(0.5)
    scene bg school
    show skit happy at center
    with Pause(0.3)

    "...The noise comes rushing back."
    "I must have imagined it."

    mc "Did you say something just now?"

    skit "Hm? No? I was just saying we should hurry!"

    "I look at her. She's smiling the same smile she always has."
    "Still, my hands feel a little cold."

    ## ---- Clubroom ---------------------------------------------------------
    scene bg clubroom
    with fade

    "The clubroom is small and warm, with tall windows and bookshelves crammed against every wall."
    "A few desks have been pushed together in the middle of the room."
    "Sunlight falls across them in long, lazy stripes."

    show skit happy at center
    $ skit_name = "Skit"

    skit "Okay! Formal introductions! I'm Skit. We've known each other since forever, but I figured I'd do it properly."

    mc "You're being weird."

    skit "I'm being {i}welcoming{/i}."

    "I laugh, and for the first time this morning it feels genuine."

    skit "Welcome to the [club_name], [player]."

    unk "...You brought someone."

    "A voice from the back of the room. Soft, but clear."
    "I turn toward it."

    ## Hand off to chapter one
    jump ch1_start

################################################################################
## Hand-off to the core day loop (core/day_loop.rpy)
################################################################################

label ch1_start:
    jump day_loop_start
