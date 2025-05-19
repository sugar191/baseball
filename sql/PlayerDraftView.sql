CREATE OR REPLACE VIEW player_drafts_view AS
SELECT
	player_drafts.id AS player_draft_id,
	player_drafts.rank AS player_draft_rank,
	player_drafts.is_reverse_nomination AS player_draft_is_reverse_nomination,
	player_drafts.is_hit AS player_draft_is_hit,
	player_drafts.miss_count AS player_draft_miss_count,
	player_drafts.is_joined AS player_draft_is_joined,
	drafts.id AS draft_id,
	drafts.year AS draft_year,
	draft_categories.name AS draft_category_name,
	draft_categories.sort_order AS draft_category_order,
	players.id AS player_id,
	players.name AS player_name,
	position_categories.name AS position_name,
	teams.name AS team_name,
	teams.logo AS team_logo,
	teams.sort_order AS team_order,
	leagues.sort_order AS league_order
FROM
	player_drafts
INNER JOIN
	drafts
ON
	player_drafts.draft_id = drafts.id
INNER JOIN
	draft_categories
ON
	drafts.draft_category_id = draft_categories.id
INNER JOIN
	players
ON
	player_drafts.player_id = players.id
INNER JOIN
	teams
ON
	player_drafts.team_id = teams.id
INNER JOIN
	leagues
ON
	teams.league_id = leagues.id
INNER JOIN
	position_categories
ON
	player_drafts.position_category_id = position_categories.id
;