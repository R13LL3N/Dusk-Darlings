################################################################################
## characters.rpy  -  dialogue Character() definitions for the whole cast
##
## Colors match each character's hair color in their menu art, so their name
## tag and their portrait feel like they belong to the same person.
##
## Use these in your script like:
##     riel "That's an inefficient way to word this sentence."
##     mary "No rush. We've got all afternoon."
##
## Skit is defined differently (see below) because they're the character the
## player meets in intro.rpy, where their name is hidden as "???" until they
## introduce themselves - the classic DDLC-style reveal.
################################################################################

define riel   = Character("Riel",   color="#fcf2f6")   # smart, stoic
define mary   = Character("Mary",   color="#76747e4b")   # laidback, calm, friendly
define blaire = Character("Blaire", color="#241515")   # outgoing, tomboyish, quick to anger

## Skit's display name is a variable, not a fixed string, so it can show "???"
## before the reveal and "Skit" after. intro.rpy sets skit_name to "Skit" the
## moment they introduce themselves. If you want the same hidden-name trick
## for Riel, Mary or Blaire later, copy this pattern for them too.
default skit_name = "???"
define skit = Character("[skit_name]", color="#7cb4aa")   # shy, kind, helpful
