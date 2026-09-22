################################################################################
## main_menu.rpy  -  DDLC-style splash + animated main menu   (v2)
##
##   - content-warning splash (first launch only) -> studio logo -> white flash
##   - scrolling checkerboard, falling petals, twinkling sparkles
##   - a group of 4 characters that pop up one by one, then gently "breathe"
##   - custom font, hover arrow + highlight + text nudge on every button
##   - looping menu music (intro + loop) and an optional "dark" menu stage
##
## Designed at 1920x1080. Auto-scales to other resolutions (e.g. 1280x720).
################################################################################

## Makes this file's screen override screens.rpy's. If Ren'Py complains about a
## duplicate, delete the original "screen main_menu():" block in screens.rpy.
init offset = 1

################################################################################
## THINGS YOU'LL WANT TO EDIT
################################################################################

## Fonts. Drop any .ttf/.otf into game/fonts/ and change these two lines.
## (Bundled: Poppins, SIL Open Font License.)
define MENU_FONT       = "fonts/Poppins-Bold.ttf"      # buttons
define MENU_FONT_LIGHT = "fonts/Poppins-Medium.ttf"    # version text, disclaimer

init python:

    MENU_AUDIO_EXT  = "ogg"    # "ogg" loops cleanly; "mp3" may leave a tiny gap
    MENU_LOOP_START = 5.0      # seconds: where the track jumps back to when it ends

    ## The group photo. One row per character:
    ##   (art name,  x center,  zoom,  pop delay (s),  breathing period (s),  layer)
    ## - art name  -> images/mainmenu/menu_art_<name>.png
    ## - pop delay -> when they appear; increase for a slower reveal
    ## - layer     -> draw order, back to front (higher = in front)
    MENU_GROUP = [
        ("riel",    905, 0.70, 0.9, 3.9, 0),
        ("mary",   1160, 0.82, 1.5, 3.4, 2),
        ("blaire", 1420, 0.82, 2.1, 4.1, 3),
        ("skit",   1675, 0.70, 2.7, 3.6, 1),
    ]
    MENU_DRAW_ORDER = sorted(MENU_GROUP, key=lambda c: c[5])

    def play_menu_music():
        track = "menu_theme_dark" if persistent.menu_stage >= 1 else "menu_theme"
        renpy.music.play(
            "<loop %s>audio/%s.%s" % (MENU_LOOP_START, track, MENU_AUDIO_EXT),
            channel="music", fadein=1.0, if_changed=True)

## Persistent data (survives between playthroughs, like DDLC's menu changes)
default persistent.seen_disclaimer = False
default persistent.menu_stage  = 0      # 0 = normal menu, 1 = dark menu
default persistent.menu_hidden = []     # names of characters removed from the menu

## Flash between the splash and the menu
define config.end_splash_transition = Fade(0.3, 0.1, 0.9, color="#ffffff")

################################################################################
## Splash sequence
################################################################################

image splash_studio = "images/splash/studio_logo.png"

label splashscreen:

    scene black
    with Pause(0.8)

    if not persistent.seen_disclaimer:
        show text "{font=fonts/Poppins-Medium.ttf}{size=30}{color=#ffffff}This game is a fan-made psychological horror experience.\n\nIt contains disturbing themes and is not suitable for children\nor anyone who may be easily disturbed.\n\nPlayer discretion is advised.{/color}{/size}{/font}" with dissolve
        $ renpy.pause(5.0, hard=True)
        hide text with dissolve
        with Pause(0.8)
        $ persistent.seen_disclaimer = True

    show splash_studio at truecenter with dissolve
    $ renpy.pause(2.2, hard=True)
    hide splash_studio with dissolve
    with Pause(0.6)

    return

################################################################################
## Backgrounds and particles
################################################################################

## Checkerboard scrolls diagonally. 120 = the pattern's repeat distance, so the
## loop has no visible jump (see README if you swap in your own tile).
image menu_bg:
    "images/mainmenu/checker.png"
    subpixel True
    topleft
    parallel:
        xoffset 0
        linear 4.0 xoffset -120
        repeat
    parallel:
        yoffset 0
        linear 4.0 yoffset -120
        repeat

image menu_bg_dark:
    "images/mainmenu/checker_dark.png"
    subpixel True
    topleft
    parallel:
        xoffset 0
        linear 7.0 xoffset -120
        repeat
    parallel:
        yoffset 0
        linear 7.0 yoffset -120
        repeat

## Falling petals (normal) / drifting ash (dark stage)
image menu_petals = SnowBlossom("images/mainmenu/petal.png", count=22, border=60,
                                xspeed=(10, 60), yspeed=(70, 140), start=1)
image menu_ash    = SnowBlossom("images/mainmenu/petal_dark.png", count=16, border=60,
                                xspeed=(-20, 20), yspeed=(40, 100), start=1)

################################################################################
## Transforms
################################################################################

## Scales the whole 1920x1080 layout to the game's actual resolution
transform menu_scale:
    zoom (config.screen_width / 1920.0)

## Logo: slides in from the left, then floats gently forever
transform menu_logo_pop(x, y, delay=0.2):
    xpos x ypos y
    alpha 0.0 xoffset -60
    pause delay
    easein 0.8 alpha 1.0 xoffset 0
    block:
        ease 2.6 yoffset -8
        ease 2.6 yoffset 0
        repeat

## Each character: rises from below with a little overshoot, then breathes.
## Anchored bottom-center, so x = center of the character and 1092 = feet
## (slightly below the screen edge so breathing never shows a gap).
transform menu_char_pop(x, z, delay=0.0, period=3.6):
    xanchor 0.5 yanchor 1.0
    xpos x ypos 1092
    zoom (z * 0.9) alpha 0.0 yoffset 380
    pause delay
    block:
        parallel:
            easeout 0.55 yoffset -28
            easein 0.30 yoffset 0
        parallel:
            easeout 0.45 alpha 1.0
        parallel:
            easeout 0.55 zoom (z * 1.04)
            easein 0.30 zoom z
    block:
        ease (period / 2.0) yoffset -8
        ease (period / 2.0) yoffset 0
        repeat

## Same entrance, but with an occasional glitch flicker (dark stage)
transform menu_char_pop_dark(x, z, delay=0.0, period=3.6):
    xanchor 0.5 yanchor 1.0
    xpos x ypos 1092
    zoom (z * 0.9) alpha 0.0 yoffset 380
    pause delay
    block:
        parallel:
            easeout 0.55 yoffset -28
            easein 0.30 yoffset 0
        parallel:
            easeout 0.45 alpha 1.0
        parallel:
            easeout 0.55 zoom (z * 1.04)
            easein 0.30 zoom z
    parallel:
        ease (period / 2.0) yoffset -8
        ease (period / 2.0) yoffset 0
        repeat
    parallel:
        pause (period + 1.5)
        xoffset 9 alpha 0.6
        pause 0.06
        xoffset -6 alpha 1.0
        pause 0.06
        xoffset 0
        pause (period * 0.8)
        repeat

## Twinkling sparkle: appears at a random spot, grows, spins, fades, repeats
transform menu_sparkle(delay=0.0):
    anchor (0.5, 0.5)
    alpha 0.0 zoom 0.4
    pause (delay + 2.5)
    block:
        pos (renpy.random.randint(560, 1880), renpy.random.randint(80, 980))
        alpha 0.0 zoom 0.4 rotate 0
        parallel:
            easein 0.5 alpha 1.0
            easeout 0.9 alpha 0.0
        parallel:
            linear 1.4 zoom 1.1 rotate 90
        pause (renpy.random.random() * 2.0)
        repeat

## Buttons slide in one after another
transform menu_btn_in(delay=0.0):
    alpha 0.0 xoffset -90
    pause delay
    parallel:
        easeout 0.55 xoffset 0
    parallel:
        easeout 0.40 alpha 1.0

## Hover arrow: slides in and wiggles while the button is hovered
transform menu_arrow:
    alpha 0.0 xoffset -26
    on hover:
        parallel:
            easeout 0.18 alpha 1.0
        parallel:
            easeout 0.18 xoffset 0
        block:
            ease 0.35 xoffset 9
            ease 0.35 xoffset 0
            repeat
    on idle:
        easeout 0.12 alpha 0.0 xoffset -26

## Button text nudges right on hover
transform menu_btn_text:
    on hover:
        easeout 0.15 xoffset 12
    on idle:
        easeout 0.15 xoffset 0

################################################################################
## The main menu screen
################################################################################

screen main_menu():

    tag menu

    on "show" action Function(play_menu_music)

    $ dark = persistent.menu_stage >= 1

    python:
        menu_items = [
            (0, _("New Game"),  Start()),
            (1, _("Load Game"), ShowMenu("load")),
            (2, _("Settings"),  ShowMenu("preferences")),
            (3, _("Help"),      ShowMenu("help")),
        ]
        if renpy.variant("pc"):
            menu_items.append((4, _("Quit"), Quit(confirm=not main_menu)))

    fixed:
        xysize (1920, 1080)
        at menu_scale

        ## --- background layers ---------------------------------------------
        if dark:
            add "menu_bg_dark"
        else:
            add "menu_bg"

        add "images/mainmenu/menu_fade.png"

        if dark:
            add "menu_ash"
        else:
            add "menu_petals"

        ## --- the group photo: characters pop up one by one ------------------
        for name, cx, z, delay, period, layer in MENU_DRAW_ORDER:
            if name not in persistent.menu_hidden:
                $ art = "images/mainmenu/menu_art_%s.png" % name
                if dark:
                    add art at menu_char_pop_dark(cx, z, delay, period)
                else:
                    add art at menu_char_pop(cx, z, delay, period)
                timer (delay + 0.2) action Play("sound", "audio/sfx_pop.ogg")

        ## --- sparkles (normal stage only) -----------------------------------
        if not dark:
            for i in range(10):
                add "images/mainmenu/sparkle.png" at menu_sparkle(i * 0.45)

        ## --- logo -----------------------------------------------------------
        if dark:
            add "images/mainmenu/logo_dark.png" at menu_logo_pop(80, 50, 0.2)
        else:
            add "images/mainmenu/logo.png" at menu_logo_pop(80, 50, 0.2)

        ## --- buttons ----------------------------------------------------------
        vbox:
            xpos 70
            ypos 545
            spacing 4

            for i, btn_label, act in menu_items:
                button:
                    style "ddlc_menu_button"
                    action act
                    at menu_btn_in(0.55 + i * 0.12)

                    hbox:
                        spacing 8
                        add "images/mainmenu/arrow.png" at menu_arrow
                        text btn_label style "ddlc_menu_button_text" at menu_btn_text

        ## --- version ----------------------------------------------------------
        text "v[config.version]":
            xpos 30
            yalign 0.985
            font MENU_FONT_LIGHT
            size 24
            color "#ffffff"
            outlines [ (2, "#6b2f57", 0, 0) ]

################################################################################
## Button styles
################################################################################

style ddlc_menu_button is default:
    xminimum 560
    left_padding 24
    right_padding 60
    top_padding 2
    bottom_padding 2
    background None
    hover_background Frame("images/mainmenu/btn_hover.png", 30, 0)
    hover_sound "audio/sfx_hover.ogg"
    activate_sound "audio/sfx_click.ogg"

style ddlc_menu_button_text is default:
    font MENU_FONT
    size 48
    color "#6b2f57"
    hover_color "#ff4f9a"
    outlines [ (5, "#ffffff", 0, 0) ]
    kerning 1.5
