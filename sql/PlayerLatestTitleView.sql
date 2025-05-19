CREATE OR REPLACE VIEW player_latest_title_view AS
SELECT
	player_titles.id AS id,
	latest_title.team_id AS team_id,
	latest_title.title_id AS title_id,
	latest_title.max_year AS year,
	player_common_records.player_id AS player_id,
	player_common_records.registered_name AS player_name
FROM (
	SELECT
		player_common_records.team_id,
		player_titles.title_id,
		MAX(player_titles.sort_order) AS max_sort_order
	FROM
		player_titles
	INNER JOIN
		player_common_records
	ON
		player_titles.season_id = player_common_records.season_id
		AND
		player_titles.player_id = player_common_records.player_id
	INNER JOIN
		seasons
	ON
		player_titles.season_id = seasons.id
	GROUP BY
		player_common_records.team_id,
		player_titles.title_id
) latest_title
INNER JOIN
	player_titles
ON
	latest_title.title_id = player_titles.title_id
	AND
	latest_title.max_sort_order = player_titles.sort_order
INNER JOIN
	player_common_records
ON
	player_titles.season_id = player_common_records.season_id
	AND
	player_titles.player_id = player_common_records.player_id
	AND
	latest_title.team_id = player_common_records.team_id