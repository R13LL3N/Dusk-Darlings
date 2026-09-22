################################################################################
## core/gamestate.rpy  -  PHASE 1: core game state
##
## Everything here is plain Ren'Py "default" state, which is what makes it
## automatically save/load/rollback correctly - see DEVELOPMENT.md, "Save data
## structure", before changing how any of this is declared.
##
## This file defines DATA. The label that actually drives the player through a
## day (the hub menu, locations, etc.) is in core/day_loop.rpy.
################################################################################

################################################################################
## Time system
################################################################################

## The six periods of a day, in order. Index into this with game_period to get
## the current period's name.
define GAME_PERIODS = ["Morning", "School", "Lunch", "Afternoon", "Evening", "Night"]

default game_day    = 1   # 1-indexed, matches "Day 1" in player-facing text
default game_period = 0   # index into GAME_PERIODS

################################################################################
## Player state
################################################################################

default player_money = 150   # placeholder starting allowance (₱). Phase 4 adds
                              # the part-time job that becomes the real income.

## Reputation: general traits other characters can react to later (Phase 3).
## Kept as a plain dict of trait -> integer score so it's trivially saveable.
default player_reputation = {
    "friendly":   0,
    "reliable":   0,
    "intelligent": 0,
    "athletic":   0,
    "quiet":      0,
    "strange":    0,
    "unreliable": 0,
}

################################################################################
## Character data structure  (Phase 3 fills in real Affection/Impression/Memory
## logic; this is the shared shape every character's data will use)
################################################################################

init -1 python:

    class CharacterData(object):
        """
        One of these per love interest. Deliberately minimal right now:
        Phase 1 only needs the shape to exist so later phases (and the
        location/event code below) have somewhere to read from and write to.
        """

        def __init__(self, key, display_name):
            self.key = key                    # matches the Character() var name, e.g. "riel"
            self.display_name = display_name  # for UI that can't use [square bracket] text tags

            self.met = False                  # has the player met them yet?

            self.affection = 0                # hidden, -100..100 (Phase 3)
            self.impression = {}              # trait -> count, e.g. {"kind": 2} (Phase 3)
            self.memory = []                  # list of short strings logging meaningful
                                               # moments (gifts, dates, promises...) (Phase 3)

            self.likes = []                   # gift keys they love/like (Phase 5)
            self.dislikes = []

        def remember(self, note):
            """Append a memory note. Safe to call from anywhere once Phase 3 wires it up."""
            self.memory.append("Day %d (%s): %s" % (game_day, GAME_PERIODS[game_period], note))

## One CharacterData per love interest. Created once, at game start (not
## inside a label), so it exists from the very first frame and is saved
## automatically like everything else in the store.
default cast = {
    "riel":   CharacterData("riel",   "Riel"),
    "mary":   CharacterData("mary",   "Mary"),
    "blaire": CharacterData("blaire", "Blaire"),
    "skit":   CharacterData("skit",   "Skit"),
}

################################################################################
## Event system  (Phase 1 skeleton: a flag set + a place to hook per-period
## checks. Phase 9's adaptive prevention system and Phase 12's yandere route
## both build on top of this rather than replacing it.)
################################################################################

default story_flags = set()   # generic "this happened" markers, e.g. "met_skit",
                               # "met_riel". Check with:  "met_skit" in story_flags
                               # Set with:                   $ story_flags.add("met_skit")

init -1 python:

    def flag(name):
        """True/False - has this story flag been set?"""
        return name in story_flags

    def set_flag(name):
        if name not in story_flags:
            story_flags.add(name)

################################################################################
## Time helpers
################################################################################

init -1 python:

    def period_name():
        return GAME_PERIODS[game_period]

    def is_period(*names):
        return period_name() in names

    def advance_period():
        """Move to the next period, rolling over into the next day at Night."""
        global game_period, game_day
        game_period += 1
        if game_period >= len(GAME_PERIODS):
            game_period = 0
            game_day += 1
