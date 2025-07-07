CREATE OR REPLACE VIEW player_record_view AS
SELECT
	players.id AS player_id,
	case when player_common_records.registered_name is null or player_common_records.registered_name = '' then players.name else player_common_records.registered_name end as player_name,
	player_common_records.team_id as team_id,
	player_common_records.season_id as season_id,
	seasons.`year`  - players.birth_year as age,
	position_categories.name AS position_category_name,
	position_categories.sort_order AS position_order,
	player_common_records.number as common_record_number,
	LENGTH(player_common_records.number) >= 3 AS is_training,
	player_pitching_records.games AS pitching_games,
	player_pitching_records.wins AS pitching_wins,
	player_pitching_records.loses AS pitching_loses,
	player_pitching_records.saves AS pitching_saves,
	player_pitching_records.holds AS pitching_holds,
	player_pitching_records.strike_outs AS pitching_strike_outs,
	player_pitching_records.earned_run_average AS pitching_earned_run_average,
	player_batting_records.plate_appearances AS batting_plate_appearances,
	player_batting_records.home_runs AS batting_home_runs,
	player_batting_records.runs_batted_in AS batting_runs_batted_in,
	player_batting_records.stolen_bases AS batting_stolen_bases,
	player_batting_records.batting_average AS batting_average
FROM
   players
LEFT JOIN
	player_categories
ON
	players.player_category_id = player_categories.id
LEFT JOIN
	position_categories
ON
	players.main_position_category_id = position_categories.id
LEFT JOIN
	player_common_records
ON
	players.id = player_common_records.player_id
LEFT JOIN
	seasons
ON
	player_common_records.season_id = seasons.id
LEFT JOIN 
	player_pitching_records
ON
	player_common_records.player_id = player_pitching_records.player_id
	and
	player_common_records.season_id = player_pitching_records.season_id
LEFT JOIN 
	player_batting_records
ON
	player_common_records.player_id = player_batting_records.player_id
	and
	player_common_records.season_id = player_batting_records.season_id
;