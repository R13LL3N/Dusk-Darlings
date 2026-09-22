# Dusk Darlings — TODO

Checklist form of `DEVELOPMENT.md`. Phases follow the master instruction's
order — don't skip ahead to horror/tragedy systems while earlier phases are
unfinished.

## Phase 0 — Project audit
- [x] Inspect project structure, engine, entry point, menu, assets, save system
- [x] Document findings in DEVELOPMENT.md
- [x] Fix the launch-blocking duplicate-`label start` bug (deleted vanilla `script.rpy`)
- [x] Merge menu up to the latest agreed version (group photo, font, Riel/Mary/Blaire/Skit)

## Phase 1 — Core game framework
- [x] Game state manager (`core/gamestate.rpy`)
- [x] Day counter + time-of-day system (`game_day`, `game_period`, `GAME_PERIODS`)
- [x] Scene/location system (`hub_<period>` + `loc_<name>` labels)
- [x] Player state (money, reputation)
- [x] Activity/time consumption (`advance_period_do`)
- [x] Character data structure (`CharacterData`, `cast` dict)
- [x] Event system skeleton (`story_flags`, `flag()`/`set_flag()`)
- [x] Basic save/load architecture (confirmed: everything uses `default`, so
      Ren'Py's built-in save/load/rollback already covers it — no custom code needed)
- [x] Basic dialogue system (already covered by Ren'Py's built-in `Character()` +
      say screen, used throughout intro.rpy — nothing extra needed for Phase 1)
- [x] Player should be able to move through a basic day — **done, untested in-engine**
- [ ] **Play-test Day 1 → Day 2 rollover in the actual Ren'Py engine** (this
      environment has no Ren'Py runtime; everything so far is statically
      checked, not played)

## Story direction correction (done this session)
- [x] Identified DDLC-resembling structure in the prologue (club recruitment,
      "welcome to the club," a member reacting to a newcomer)
- [x] Removed the club premise entirely (`club_name`, `agreed_to_visit` gone)
- [x] Rewrote the prologue as an ordinary morning (wake up → walk to school
      with Skit → arrive at school), no foreshadowing, no club
- [x] Reworked Skit's dialogue to match her actual profile (shy/kind/helpful,
      not boisterous/teasing)
- [x] Removed the DDLC-style hidden-name reveal for Skit (didn't make sense
      for an established childhood friend anyway)
- [x] Renamed the clubroom location/art to the library, removed the
      `joined_club` flag gating it — it's now a plain, always-open location
- [x] Confirmed Riel/Mary/Blaire are not introduced anywhere yet, and won't
      be introduced together when they are
- [x] Re-ran the full static check (labels/jumps/screens/images) after the rewrite
- [x] Updated DEVELOPMENT.md with what changed and why

## Phase 2 — Riel vertical slice (NEXT)
- [ ] Riel character data (extend `cast["riel"]`)
- [ ] Riel's first-meeting scene — write it into `loc_library` (fits her
      profile: books, chess, quiet environments). Standalone scene, not a
      group introduction with Mary/Blaire.
- [ ] Riel-specific dialogue
- [ ] Affection / Impression / Memory actually wired up (not just the empty shape)
- [ ] Likes/dislikes (books, chess, coffee, quiet environments, per her profile)
- [ ] Basic school interactions
- [ ] Gift system (first pass, Riel only)
- [ ] One date
- [ ] One minigame (chess/tactical puzzle placeholder)
- [ ] Confession
- [ ] Relationship state

## Not started (later phases, listed for reference — do not jump ahead)
- [ ] Phase 3 — Player systems (Affection/Impression/Memory generalized to all 4, reputation reactions)
- [ ] Phase 4 — Economy and job
- [ ] Phase 5 — Gift and date system (generalized)
- [ ] Phase 6 — Character minigames (Mary/Blaire/Skit)
- [ ] Phase 7 — Complete cast (Mary, Blaire, Skit full routes — each their own
      standalone first-meeting scene, per the corrected direction above)
- [ ] Phase 8 — The curse
- [ ] Phase 9 — Adaptive death/prevention
- [ ] Phase 10 — Save/timeline system
- [ ] Phase 11 — Loner ending
- [ ] Phase 12 — Yandere route
- [ ] Phase 13 — Isekai easter egg
- [ ] Phase 14 — Good ending
- [ ] Phase 15 — Meta horror
- [ ] Phase 16 — Black sprite glitch
- [ ] Phase 17 — Diegetic audio horror
- [ ] Phase 18 — Menu/meta events
- [ ] Phase 19 — Phone system
- [ ] Phase 20 — Gallery/ending collection
- [ ] Phase 21 — True reset
- [ ] Phase 22 — Polish

## Known bugs
(none found in static review — see DEVELOPMENT.md's testing section for what
"tested" means right now)

## Open questions for you
- Starting `player_money` of ₱150 is a placeholder guess — change the default
  in `core/gamestate.rpy` if you have a real number in mind
- The library is set up as a likely first-meeting spot for Riel specifically
  (books/chess/quiet environments) — confirm that fits your plan for her, or
  tell me where you'd rather introduce each of the four instead
