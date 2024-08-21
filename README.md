Python-based chess game made from scratch.
==========================================

CURRENT GOAL:
- Functional chess game for two-player local play.

CURRENT TASKS:
- Load position from FEN (Forsyth-Edwards Notation)
- Write moves to console in chess annotation
- Record game in PGN (Portable Game Notation)
- Add option to reset board without ending script

CURRENT BUGS:
- 17/08/2024 Noticed a bug when trying to capture pinned knight. Bishop/queen move to knight's square but knight stays on board on same square. Turn changes like normal. Unable to reproduce consistently. 19/08/2024 Bug not presented again yet.

COMPLETED TASKS:
- Draw board
- Define pieces
- Draw pieces
- Move pieces
- Restrict to legal moves
- Remove ghosting
- Add checks
- Add castling
- Add checkmate check
- Add board square numbers to chess board
- En passant
- Add stalemate
- Add draw by repetition
- Add function to generate first field of FEN
- Fixed check/checkmate bug
- Fixed stalemate bug

FUTURE IDEAS:
- Opening trainer
- Menu select
- Improve graphics
- Multiplayer online
- Chess bot (possibly using lichess API)
