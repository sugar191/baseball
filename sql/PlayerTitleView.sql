CREATE OR REPLACE VIEW player_title_view AS
SELECT
	player_titles.id AS id,
	titles.id AS title_id,
	positions.id AS position_id,
	seasons.year AS year,
	seasons.label AS season_label,
	teams.logo AS team_logo,
	players.id AS player_id,
	player_common_records.registered_name AS player_name,
	CASE titles.name
		WHEN '首位打者' THEN player_batting_records.batting_average
	END AS batting_average,
	CASE titles.name
		WHEN '本塁打王' THEN player_batting_records.home_runs
	END AS home_runs,
	CASE titles.name
		WHEN '打点王' THEN player_batting_records.runs_batted_in
	END AS runs_batted_in,
	CASE titles.name
		WHEN '盗塁王' THEN player_batting_records.stolen_bases
	END AS stolen_bases,
	CASE titles.name
		WHEN '最高出塁率' THEN player_batting_records.on_base_percentage
	END AS on_base_percentage,
	CASE titles.name
		WHEN '最多安打' THEN player_batting_records.hits
	END AS hits,
	CASE titles.name
		WHEN '最多勝' THEN player_pitching_records.wins
	END AS wins,
	CASE titles.name
		WHEN '最優秀防御率' THEN player_pitching_records.earned_run_average
	END AS earned_run_average,
	CASE titles.name
		WHEN '最高勝率' THEN player_pitching_records.wins / (player_pitching_records.wins + player_pitching_records.loses)
	END AS win_average,
	CASE titles.name
		WHEN '最多奪三振' THEN player_pitching_records.strike_outs
	END AS strike_outs,
	CASE titles.name
		WHEN 'セーブ王' THEN player_pitching_records.saves
	END AS saves,
	CASE titles.name
		WHEN '最優秀中継ぎ' THEN player_pitching_records.holds
	END AS holds
FROM
	player_titles
INNER JOIN
	players
ON
	player_titles.player_id = players.id
LEFT JOIN
	positions
ON
	player_titles.position_id = positions.id
INNER JOIN
	titles
ON
	player_titles.title_id = titles.id
INNER JOIN
	player_common_records
ON
	player_titles.player_id = player_common_records.player_id
	AND
	player_titles.season_id = player_common_records.season_id
LEFT JOIN
	player_batting_records
ON
	player_titles.player_id = player_batting_records.player_id
	AND
	player_titles.season_id = player_batting_records.season_id
LEFT JOIN
	player_pitching_records
ON
	player_titles.player_id = player_pitching_records.player_id
	AND
	player_titles.season_id = player_pitching_records.season_id
INNER JOIN
	teams
ON
	player_common_records.team_id = teams.id
INNER JOIN
	leagues
ON
	teams.league_id = leagues.id
INNER JOIN
	seasons
ON
	player_titles.season_id = seasons.id
ORDER BY
	titles.sort_order,
	seasons.sort_order DESC,
	leagues.sort_order,
	positions.sort_order
;