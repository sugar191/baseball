CREATE OR REPLACE VIEW player_careers_view AS
SELECT
	player_careers.id AS player_career_id,
	career_versions.career_id AS career_id,
	players.id AS player_id,
	players.name AS player_name,
	players.furigana AS player_furigana,
	players.birthday AS player_birthday,
	after_career_versions.career_id AS after_career_id,
	after_career_versions.name AS after_career_name,
	drafts.year AS draft_year,
	teams.logo AS team_logo,
	draft_categories.name AS draft_category_name,
	player_drafts.rank AS player_draft_rank,
	player_drafts.miss_count AS player_draft_miss_count
FROM
	player_careers
LEFT JOIN
	career_versions
ON
	player_careers.career_version_id = career_versions.id
LEFT JOIN
	players
ON
	player_careers.player_id = players.id
LEFT JOIN
	player_careers after_player_careers
ON
	player_careers.player_id = after_player_careers.player_id
	and
	player_careers.sort_order + 1 = after_player_careers.sort_order
LEFT JOIN
	career_versions after_career_versions
ON
	after_player_careers.career_version_id = after_career_versions.id
LEFT JOIN
	player_drafts
ON
	player_careers.player_id = player_drafts.player_id
	AND
	player_drafts.is_joined = TRUE
LEFT JOIN
	teams
ON
	player_drafts.team_id = teams.id
LEFT JOIN
	drafts
ON
	player_drafts.draft_id = drafts.id
LEFT JOIN
	draft_categories
ON
	drafts.draft_category_id = draft_categories.id