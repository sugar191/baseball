CREATE OR REPLACE VIEW player_latest_summary AS
SELECT
	players.id AS player_id,
	players.name AS player_name,
	players.furigana AS player_furigana,
	players.nickname AS player_nickname,
	players.birthday AS player_birthday,
	players.birth_year AS player_birth_year,
	players.is_dead AS player_is_dead,
	players.death_date AS player_death_date,
	players.height AS player_height,
	players.weight AS player_weight,
	players.is_married AS player_is_married,
	players.partner AS player_partner,
	players.hobby AS player_hobby,
	players.specialty AS player_specialty,
	players.wikipedia_parameter AS player_wikipedia_parameter,
	players.usukoi_parameter AS player_usukoi_parameter,
	players.youtube_parameter AS player_youtube_parameter,
	players.remarks AS player_remarks,
	player_categories.id AS player_category_id,
	player_categories.name AS player_category_name,
	player_categories.sort_order AS player_category_order,
	places.id AS place_id,
	places.name AS place_name,
	hands_throwing.id AS throwing_id,
	hands_throwing.name AS throwing_name,
	hands_batting.id AS batting_id,
	hands_batting.name AS batting_name,
	position_categories.id AS position_category_id,
	position_categories.name AS position_category_name,
	position_categories.sort_order AS position_order,
	player_careers.remarks AS player_career_remarks,
	career_versions.id AS career_version_id,
	career_versions.name AS career_version_name,
	careers.id AS career_id,
	career_categories.id AS career_category_id,
	career_categories.label AS career_category_label,
	player_drafts.rank AS player_draft_rank,
	player_drafts.team_id AS player_draft_team,
	player_drafts.miss_count AS player_draft_miss_count,
	drafts.year AS draft_year,
	draft_categories.name AS draft_category_name,
	player_common_records.year AS common_record_year,
	player_common_records.number AS common_record_number,
	LENGTH(player_common_records.number) >= 3 AS is_training,
	player_common_records.registered_name AS common_record_registered_name,
	player_common_records.salary AS common_record_salary,
	currencies.name AS currency_name,
	teams.id AS team_id,
	teams.name AS team_name,
	teams.logo AS team_logo,
	teams.sort_order AS team_order,
	teams.color AS team_color,
	leagues.sort_order AS league_order,
	organizations.id AS organization_order,
	player_pitching_records.year AS pitching_year,
	player_pitching_records.games AS pitching_games,
	player_pitching_records.wins AS pitching_wins,
	player_pitching_records.loses AS pitching_loses,
	player_pitching_records.saves AS pitching_saves,
	player_pitching_records.holds AS pitching_holds,
	player_pitching_records.strike_outs AS pitching_strike_outs,
	player_pitching_records.earned_run_average AS pitching_earned_run_average,
	player_batting_records.year AS batting_year,
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
	places
ON
	players.place_id = places.id
LEFT JOIN
	hands_throwing
ON
	players.throwing_hand_id = hands_throwing.id
LEFT JOIN
	hands_batting
ON
	players.batting_hand_id = hands_batting.id
LEFT JOIN
	position_categories
ON
	players.main_position_category_id = position_categories.id
LEFT JOIN (
   SELECT
		player_id,
		MAX(sort_order) AS latest_sort_order
   FROM
		player_careers
   GROUP BY
		player_id
) AS latest_career
ON
	players.id = latest_career.player_id
LEFT JOIN
	player_careers
ON
	players.id = player_careers.player_id
   AND
	player_careers.sort_order = latest_career.latest_sort_order
LEFT JOIN
	career_versions
ON
	player_careers.career_version_id = career_versions.id
LEFT JOIN
	careers
ON
	career_versions.career_id = careers.id
LEFT JOIN
	career_categories
ON
	careers.career_category_id = career_categories.id
LEFT JOIN
	player_drafts
ON
	players.id = player_drafts.player_id
   AND
	player_drafts.is_joined
LEFT JOIN
	drafts
ON
	player_drafts.draft_id = drafts.id
LEFT JOIN
	draft_categories
ON
	drafts.draft_category_id = draft_categories.id
LEFT JOIN (
	SELECT
		player_common_records.player_id,
		MAX(seasons.sort_order) max_season_order
	FROM
		player_common_records
	LEFT JOIN
		seasons
	ON
		player_common_records.season_id = seasons.id
	WHERE
		seasons.year = (SELECT MAX(YEAR) FROM seasons)
	GROUP BY
		player_common_records.player_id
) latest_common_record
ON
	players.id = latest_common_record.player_id
LEFT JOIN (
	SELECT
		player_common_records.player_id,
		player_common_records.team_id,
		player_common_records.number,
		player_common_records.registered_name,
		player_common_records.salary,
		player_common_records.currency_id,
		seasons.year,
		seasons.label,
		seasons.sort_order
	FROM
		player_common_records
	LEFT JOIN
		seasons
	ON
		player_common_records.season_id = seasons.id
) player_common_records
ON
	latest_common_record.player_id = player_common_records.player_id
	AND
	latest_common_record.max_season_order = player_common_records.sort_order
LEFT JOIN
	currencies
ON
	player_common_records.currency_id = currencies.id
LEFT JOIN
	teams
ON
	player_common_records.team_id = teams.id
LEFT JOIN
	leagues
ON
	teams.league_id = leagues.id
LEFT JOIN
	organizations
ON
	leagues.organization_id = organizations.id
LEFT JOIN (
	SELECT
		player_pitching_records.player_id,
		MAX(seasons.sort_order) max_season_order
	FROM
		player_pitching_records
	LEFT JOIN
		seasons
	ON
		player_pitching_records.season_id = seasons.id
   WHERE
		seasons.year = (SELECT MAX(YEAR) FROM seasons) - 1
	GROUP BY
		player_pitching_records.player_id
) latest_pitching_record
ON
	players.id = latest_pitching_record.player_id
LEFT JOIN (
	SELECT
		player_pitching_records.player_id,
		player_pitching_records.games,
		player_pitching_records.wins,
		player_pitching_records.loses,
		player_pitching_records.saves,
		player_pitching_records.holds,
		player_pitching_records.strike_outs,
		player_pitching_records.earned_run_average,
		seasons.year,
		seasons.label,
		seasons.sort_order
	FROM
		player_pitching_records
	LEFT JOIN
		seasons
	ON
		player_pitching_records.season_id = seasons.id
) player_pitching_records
ON
	latest_pitching_record.player_id = player_pitching_records.player_id
	AND
	latest_pitching_record.max_season_order = player_pitching_records.sort_order
LEFT JOIN (
	SELECT
		player_batting_records.player_id,
		MAX(seasons.sort_order) max_season_order
	FROM
		player_batting_records
	LEFT JOIN
		seasons
	ON
		player_batting_records.season_id = seasons.id
   WHERE
		seasons.year = (SELECT MAX(YEAR) FROM seasons) - 1
	GROUP BY
		player_batting_records.player_id
) latest_batting_record
ON
	players.id = latest_batting_record.player_id
LEFT JOIN (
	SELECT
		player_batting_records.player_id,
		player_batting_records.plate_appearances,
		player_batting_records.home_runs,
		player_batting_records.runs_batted_in,
		player_batting_records.stolen_bases,
		player_batting_records.batting_average,
		seasons.year,
		seasons.label,
		seasons.sort_order
	FROM
		player_batting_records
	LEFT JOIN
		seasons
	ON
		player_batting_records.season_id = seasons.id
) player_batting_records
ON
	latest_batting_record.player_id = player_batting_records.player_id
	AND
	latest_batting_record.max_season_order = player_batting_records.sort_order
;