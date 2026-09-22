# Dusk Darlings — Development Log

**Current phase:** Phase 1 complete (core day loop). Ready to begin Phase 2 (Riel
vertical slice) whenever you've written her introduction content.

**Engine:** Ren'Py, project built for 1920x1080 (`gui.init(1920, 1080)` in `gui.rpy`).

---

## How to read this file

This is the project's persistent memory, per the master instruction. If you're
picking this project back up in a new session (or handing it to me in a new
conversation), read this file and `TODO.md` first — they should tell you
everything needed to reconstruct where things stand without re-reading every
script.

---

## Phase 0 — Project audit (findings)

Audited the uploaded project against the master instruction before writing any
gameplay code.

**What already existed:**
- A full custom main menu (`main_menu.rpy`): splash → studio logo → white
  flash → animated menu with a scrolling background, a 4-character "group
  photo" that pops in, hover arrow/highlight, particles, and looping music.
- A prologue (`intro.rpy`): name entry → morning → walk to school → club
  invitation choice → clubroom, ending at a `ch1_start` stub.
- Shared `Character()` definitions for the cast (`characters.rpy`).
- Standard Ren'Py save/load, preferences, and quick-menu screens, untouched,
  in `screens.rpy`.

**What this audit changed, and why:**
1. **Merged forward to the latest agreed menu version.** The uploaded
   `game.zip` still had the *first* version of the menu (single character
   named "Mika", no custom font, no particle effects) — it predated the two
   follow-up updates already agreed on earlier in this project (the 4-character
   group-photo menu, and the Riel/Mary/Blaire/Skit rename). Rather than build
   Phase 1 on top of stale menu art, I brought `main_menu.rpy`, `intro.rpy`,
   `characters.rpy`, the fonts, and the character art up to that already-agreed
   state as part of this audit. **If you've made your own edits to those files
   since downloading the last update, re-upload before I touch this project
   again** — this merge would have overwritten local changes I don't know
   about.
2. **Deleted `script.rpy`.** It was still the vanilla Ren'Py template file
   (`label start: ... e "You've created a new Ren'Py game." ...`), and it
   defined its own `label start`, which collides with the one in `intro.rpy`.
   Ren'Py refuses to launch a project with two labels of the same name, so
   this was a launch-blocking bug. Nothing in the template file was worth
   keeping.
3. **Deleted stale `.rpyc` caches.** The uploaded project's compiled caches
   were built from the old `script.rpy`/menu files. Ren'Py regenerates these
   automatically on next launch, but stale ones can shadow edited `.rpy`
   source until deleted, so I cleared them rather than risk that.

No other architectural changes. The menu and prologue are otherwise untouched.

---

## Story direction correction (post-Phase-1)

**Problem:** the prologue I wrote in `intro.rpy` during Phase 0/1 directly
resembled DDLC's Literature Club opening — a club about to be shut down for
lack of members, the childhood friend pulling the protagonist in ("you're
coming anyway"), a "Welcome to the [club]" line, and another character
reacting to a newcomer ("...You brought someone."). This is exactly what
`Anti_DDLC.txt` rules out, and I didn't check my own draft against it closely
enough before building Phase 1 on top of it. Caught and corrected in the same
session, before any further phases were built on top of it.

**What changed:**
- **Removed the club premise entirely.** No Literature Club, no renamed
  equivalent, no recruitment plot, no "everyone's really nice, you'll love
  it" pressure. `club_name` and `agreed_to_visit` are gone from `intro.rpy`.
- **Rewrote the whole prologue.** It's now just an ordinary morning: waking
  up, a mundane exchange with Mom, the walk to school with Skit (who lends
  the player an umbrella — a small, ordinary "usually the one who helps you"
  beat instead of a stated trait), and arriving at the school gate. No white
  flash, no "I promise you'll never want to leave" foreshadowing — per
  `Anti_DDLC.txt`'s tone-progression rule, Day 1 should read as completely
  normal, with nothing supernatural hinted at yet.
- **Reworked Skit's characterization to actually match her profile.** The
  original draft wrote her as boisterous/teasing, which was closer to a
  Sayori-style dynamic and didn't match "shy, kind, usually helps you" as
  specified. She's now quieter and more practical (the umbrella, short
  sentences, doesn't quite make eye contact).
- **Removed the DDLC-style hidden-name reveal for Skit.** `skit_name`
  (`"???"` until an introduction scene) didn't make narrative sense anyway —
  Skit is an established childhood friend, so the player already knows her
  name from the first line. `characters.rpy` now defines her the same plain
  way as the other three.
- **Riel, Mary, and Blaire are not in the prologue at all**, and aren't
  introduced together anywhere. Per `Anti_DDLC.txt`'s instruction to let the
  player "gradually encounter them through normal circumstances," each of
  them gets their own separate first-meeting scene, on their own schedule,
  written later (Phase 2 onward) into the ordinary locations already sitting
  in `core/day_loop.rpy` — the library, the cafeteria, class, town, etc. —
  rather than through one artificial group scene.
- **Renamed the "clubroom" location to the library** (`bg clubroom.png` →
  `bg library.png`, background art regenerated to read clearly as a library
  rather than a generic room), and removed the `joined_club` flag that
  gated it. It's now just an ordinary, always-available Lunch/Afternoon
  location — and a natural first-meeting spot for Riel specifically, given
  her stated love of books and quiet environments, though that scene hasn't
  been written yet.

**What did NOT change:** the Phase 1 systems themselves — the day/time loop,
`GAME_PERIODS`, `CharacterData`, `story_flags`, the hub/location structure,
save data — none of that was DDLC-shaped to begin with, so none of it needed
to be rebuilt. Only the content sitting inside it (the prologue's scene, one
flag, one location's name/art) changed. This is also why the fix was cheap:
the architecture was already generic enough to not need touching.

The "Important variable/state names" and "Next recommended task" sections
below are updated to match the corrected version.

---

## Phase 1 — Core game framework (implemented this session)

New folder: `game/core/` — kept separate from the menu/prologue files so
they can keep evolving independently.

### `core/gamestate.rpy` — data
- **Time:** `GAME_PERIODS = ["Morning", "School", "Lunch", "Afternoon",
  "Evening", "Night"]`, plus `game_day` (int, starts at 1) and `game_period`
  (index into `GAME_PERIODS`).
- **Player state:** `player_money` (int, ₱ — starts at 150 as a placeholder
  allowance; Phase 4's job replaces this as the real income source) and
  `player_reputation` (dict of trait → int score, matches the trait list in
  the master instruction's Phase 3 section).
- **Character data:** a `CharacterData` class (met / affection / impression /
  memory / likes / dislikes) and a `cast` dict — `cast["riel"]`,
  `cast["mary"]`, `cast["blaire"]`, `cast["skit"]`. Phase 1 only needs the
  *shape* to exist; Phase 3 is what actually writes meaningful values into
  affection/impression/memory. `CharacterData.remember(note)` is a
  ready-to-use hook for that once it's wired up.
- **Event system skeleton:** `story_flags` (a plain `set()`), with
  `flag("x")` / `set_flag("x")` helpers.

### `core/day_loop.rpy` — the loop itself
- `day_loop_start` — entry point, jumped to directly from the end of
  `intro.rpy`.
- `day_hub` — routes to the current period's `hub_<period>` label. Re-entered
  after every location and every period advance; this is the loop's center.
- `hub_morning` / `hub_school` / `hub_lunch` / `hub_afternoon` /
  `hub_evening` / `hub_night` — one menu per period, offering that period's
  locations as choices.
- `loc_*` labels — one per placeholder location (school, cafeteria, library,
  street, home, sleep). Currently a single placeholder line each, wrapped in
  `{i}(...)/{i}` so they're obviously stand-ins. **This is where your story
  content goes** — the surrounding menu/flag/time-advance structure doesn't
  need to change to support real writing here.
- `advance_period_do` — the only place `game_period`/`game_day` actually
  change (via `advance_period()` in `gamestate.rpy`). Every location ends by
  jumping here, which consumes that period and loops back to `day_hub`.
- `status_bar` screen — top-right overlay showing Day / period / money.
  Shown once at `day_loop_start` and persists through the whole loop. Uses
  Ren'Py's default font (`DejaVuSans.ttf`, bundled with the engine), **not**
  the menu's custom Poppins font — confirmed DejaVu has a ₱ glyph and Poppins
  doesn't, so this was a deliberate choice, not an oversight.

### Integration with the prologue
`intro.rpy` now hands off straight into `day_loop_start` with no flags to
read (the `agreed_to_visit`/`joined_club` mechanic was removed along with the
club premise — see "Story direction correction" above). Day 1 starts at
**School**, not Morning — the prologue already covers that day's morning and
walk to school narratively, so the loop picks up right as the school day
itself begins. Every day after that starts at Morning normally.

### Save data structure
Everything above is declared with Ren'Py's `default` statement (never
`define`, except for the constant `GAME_PERIODS` list and the `CharacterData`
class itself, which don't change at runtime). `default`-declared values are
automatically included in saves and rollback — no custom save/load code was
needed for Phase 1. **Keep it this way**: if a later phase adds new player
state, declare it with `default` in `gamestate.rpy` alongside the existing
fields, not as a bare global or `define`.

---

## Testing performed this session

No Ren'Py engine is available in this environment, so nothing here was
launched and clicked through — everything below is static verification, not
a play-test. **Please actually launch the project and play through Day 1
before trusting this.**

- Wrote a small script to scan every `.rpy` file for: duplicate `label`
  definitions, duplicate `screen` definitions, `jump`/`call` targets that
  don't resolve to a real label, `call screen` targets that don't resolve to
  a real screen, and (after the rewrite) every `scene`/`show` of a `bg`/
  `skit` image resolving to a real file. Result: no unresolved targets, no
  duplicate labels, no missing images. (Two `quick_menu` screens and one UI
  `label _(message):` flagged initially — both are pre-existing, correct
  Ren'Py template code: the former is a touch-screen variant of the same
  screen, the latter is a screen-language `label` *widget*, not a script
  label. Not bugs.)
- Checked indentation (multiples of 4, no tabs) and bracket/quote balance in
  every new/edited file.
- Manually traced the full loop logic by hand: Morning → School → Lunch →
  Afternoon → Evening → Night → day rollover back to Morning, including the
  reputation-adjusting School choices.
- Grepped the whole project for leftover references to the old character
  names (`mika`, `char2`–`char4`, `m_name`) after the earlier merge, and
  again for `club`/`agreed_to_visit`/`skit_name` after this rewrite — none
  found outside explanatory comments.

---

## Known bugs

None found in this session's static review. Nothing has been played in a
real Ren'Py instance yet, so treat this as "nothing found by reading the
code," not "verified bug-free."

---

## Important variable/state names (quick reference)

| Name | Where | Purpose |
|---|---|---|
| `game_day` | gamestate.rpy | current day, 1-indexed |
| `game_period` | gamestate.rpy | index into `GAME_PERIODS` |
| `GAME_PERIODS` | gamestate.rpy | `["Morning","School","Lunch","Afternoon","Evening","Night"]` |
| `player_money` | gamestate.rpy | ₱, placeholder starting value 150 |
| `player_reputation` | gamestate.rpy | dict, trait → int |
| `cast` | gamestate.rpy | dict, `"riel"/"mary"/"blaire"/"skit"` → `CharacterData` |
| `story_flags` | gamestate.rpy | set of story flag strings |
| `persistent.menu_stage` | main_menu.rpy | 0 = normal menu, 1 = dark/glitch stage |
| `persistent.menu_hidden` | main_menu.rpy | list of character keys hidden from the menu art |

---

## Next recommended task

**Phase 2 — Riel vertical slice.** Per the master instruction, this should
happen before touching Mary, Blaire, or the tragedy/horror systems. Concretely,
that means writing Riel's first-meeting scene into `loc_library` (a natural
fit, given her stated love of books/chess/quiet environments) and building
her affection/impression/memory/gift/date/minigame/confession loop on top of
the `CharacterData` shape that already exists in `cast["riel"]`. Remember:
per `Anti_DDLC.txt`, this should be a standalone, ordinary first meeting —
not a scene that also introduces Mary or Blaire at the same time.

You mentioned you're handling the story/dialogue writing yourself and may
want help with Ren'Py syntax examples as you go — `loc_library` in
`core/day_loop.rpy` is the natural place to start once you're ready.
