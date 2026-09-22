################################################################################
## core/day_loop.rpy  -  PHASE 1: the basic day loop
##
## This is the part of Phase 1 the master instruction calls "the player should
## be able to move through a basic day." It is deliberately bare: every scene
## is a one-line placeholder marked {i}like this{/i} so it's obvious what's a
## stand-in versus real writing. Replace the placeholder lines with your own
## content - the surrounding structure (menus, flags, period advancement)
## doesn't need to change to support that.
##
## Flow:
##   day_loop_start  (entered once, from intro.rpy)
##       -> day_hub  (routes to the right hub_<period> label)
##           -> hub_<period>  (narration + a menu of that period's locations)
##               -> loc_<name>  (placeholder scene)
##                   -> advance_period_do  (consumes the period, loops back)
################################################################################

################################################################################
## Status bar  -  shown throughout the day loop. Uses the game's default font
## (not the menu's custom font) so it doesn't depend on fonts/ being present.
################################################################################

screen status_bar():
    zorder 100
    frame:
        xalign 1.0
        yalign 0.0
        xoffset -20
        yoffset 20
        padding (18, 10)
        background "#00000090"

        text "Day [game_day]  -  [period_name()]\n₱[player_money]":
            size 26
            color "#ffffff"
            text_align 1.0
            line_spacing 4

################################################################################
## Entry point (called from intro.rpy once the prologue ends)
################################################################################

label day_loop_start:

    ## Fold in what already happened during the prologue in intro.rpy.
    $ set_flag("met_skit")
    $ cast["skit"].met = True
    if agreed_to_visit:
        $ set_flag("joined_club")

    ## The prologue covers Day 1's morning and school day itself, so gameplay
    ## proper picks up that same afternoon rather than repeating it.
    $ game_period = GAME_PERIODS.index("Afternoon")

    show screen status_bar

    jump day_hub

################################################################################
## Hub: routes to the correct period. Re-entered after every location and
## every period advance, so this is the "center" of the whole day loop.
################################################################################

label day_hub:

    if is_period("Morning"):
        jump hub_morning
    elif is_period("School"):
        jump hub_school
    elif is_period("Lunch"):
        jump hub_lunch
    elif is_period("Afternoon"):
        jump hub_afternoon
    elif is_period("Evening"):
        jump hub_evening
    else:
        jump hub_night

label advance_period_do:
    $ advance_period()
    jump day_hub

################################################################################
## Morning
################################################################################

label hub_morning:
    scene bg bedroom with dissolve
    "Morning, Day [game_day]. {i}(placeholder - describe the morning routine here.){/i}"

    menu:
        "Head to school.":
            jump loc_school_morning

label loc_school_morning:
    scene bg street with dissolve
    "{i}(placeholder - the walk to school goes here.){/i}"
    jump advance_period_do

################################################################################
## School
################################################################################

label hub_school:
    scene bg school with dissolve
    "School, Day [game_day]. {i}(placeholder - describe the class here.){/i}"

    menu:
        "Pay attention.":
            $ player_reputation["intelligent"] += 1
            "{i}(placeholder - paying attention nudges your Intelligent reputation up.){/i}"
            jump advance_period_do

        "Space out.":
            $ player_reputation["quiet"] += 1
            "{i}(placeholder - spacing out nudges your Quiet reputation up.){/i}"
            jump advance_period_do

################################################################################
## Lunch
################################################################################

label hub_lunch:
    scene bg school with dissolve
    "Lunch, Day [game_day]. {i}(placeholder - describe the lunch period here.){/i}"

    menu:
        "Eat in the cafeteria.":
            jump loc_cafeteria

        "Go to the clubroom." if flag("joined_club"):
            jump loc_clubroom

label loc_cafeteria:
    "{i}(placeholder - the cafeteria scene goes here.){/i}"
    jump advance_period_do

################################################################################
## Afternoon
################################################################################

label hub_afternoon:
    if flag("joined_club"):
        scene bg clubroom with dissolve
    else:
        scene bg street with dissolve
    "Afternoon, Day [game_day]. {i}(placeholder - describe the afternoon here.){/i}"

    menu:
        "Go to the clubroom." if flag("joined_club"):
            jump loc_clubroom

        "Go into town.":
            jump loc_street

label loc_clubroom:
    scene bg clubroom with dissolve
    "{i}(placeholder - clubroom scene goes here. This is where Riel, Mary and Blaire's\nintroductions will go.){/i}"
    jump advance_period_do

################################################################################
## Evening
################################################################################

label hub_evening:
    scene bg street with dissolve
    "Evening, Day [game_day]. {i}(placeholder - describe the evening here.){/i}"

    menu:
        "Go into town.":
            jump loc_street

        "Head home.":
            jump loc_home_evening

label loc_street:
    scene bg street with dissolve
    "{i}(placeholder - town/street scene goes here. The part-time job will live here\nonce it's implemented.){/i}"
    jump advance_period_do

label loc_home_evening:
    scene bg bedroom with dissolve
    "{i}(placeholder - evening-at-home scene goes here.){/i}"
    jump advance_period_do

################################################################################
## Night
################################################################################

label hub_night:
    scene bg bedroom with dissolve
    "Night, Day [game_day]. {i}(placeholder - any night-time events would trigger here,\nbefore the player sleeps.){/i}"

    menu:
        "Go to sleep.":
            jump loc_sleep

label loc_sleep:
    "{i}(placeholder - fade to black, day summary, etc. could go here.){/i}"
    jump advance_period_do
