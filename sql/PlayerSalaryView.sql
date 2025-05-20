CREATE OR REPLACE VIEW player_salary_view AS
SELECT
	player_common_records.id AS id,
	seasons.year AS year,
	players.id AS player_id,
	IF(player_common_records.registered_name IS NULL OR player_common_records.registered_name = '', players.name, player_common_records.registered_name) AS player_name,
	teams.logo AS team_logo,
	player_common_records.salary * IFNULL(exchange_rates.rate, 1) AS salary,
	RANK() OVER (ORDER BY player_common_records.salary * IFNULL(exchange_rates.rate, 1) DESC) AS 'rank'
FROM
	players
INNER JOIN
	player_common_records
ON
	players.id = player_common_records.player_id
LEFT JOIN
	teams
ON
	player_common_records.team_id = teams.id
INNER JOIN
	seasons
ON
	player_common_records.season_id = seasons.id
LEFT JOIN
	exchange_rates
ON
	player_common_records.currency_id = exchange_rates.currency_id
	AND
	seasons.year = exchange_rates.year
WHERE
	player_common_records.salary > 0
;